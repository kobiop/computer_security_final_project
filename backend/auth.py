from flask import Blueprint, request, jsonify, session
from . import db
import time
from .database.queries import (
    add_new_user,
    fetch_user_by_email,
    get_user_salt,
    upsert_user_auth_code,
    get_auth_code,
    change_user_password_and_salt,
    get_user_by_id,
    add_password_to_history,
    check_password_history,
    update_user_login_status,
    fetch_user_login_status,
    authenticate_user,
    add_user_salt,
)
from .config.config_functions import (
    validate_password,
    generate_salt,
    password_config,
    hash_password,
    send_email,
    is_password_common,
)

auth = Blueprint("auth", __name__)

MAX_ATTEMPTS = 3
BLOCK_TIME = 10


@auth.route("/logout", methods=["GET"])
def logout():
    session.clear()  # Clears all session data
    return jsonify({"message": "You have been logged out successfully!"}), 200


@auth.route("/check-auth", methods=["GET"])
def check_auth():
    user_id = session.get("user_id")
    if user_id:
        return jsonify({"isLoggedIn": True}), 200
    else:
        return jsonify({"isLoggedIn": False}), 401


@auth.route("/session", methods=["GET"])
def get_session_info():
    return jsonify({"session_info": dict(session)}), 200


@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not all([first_name, last_name, email, password]):
        return (
            jsonify(
                {
                    "message": "All fields (first name, last name, email, password) are required!"
                }
            ),
            400,
        )

    if not validate_password(password):
        return (
            jsonify({"message": "Password does not meet the required complexity!"}),
            400,
        )

    if is_password_common(password):
        return (
            jsonify(
                {
                    "message": "The chosen password is too common. Please choose a more secure password."
                }
            ),
            400,
        )

    try:
        salt = generate_salt(password_config["password_requirements"]["salt_len"])
        hashed_password = hash_password(password, salt)
        salt_hex = salt.hex()
        add_new_user(first_name, last_name, email, hashed_password, salt_hex)
        user = fetch_user_by_email(email)
        user_id = user[0]
        add_user_salt(user_id, salt_hex)
        return jsonify({"message": "Registration successful! You can now log in."}), 200

    except Exception as e:
        return (
            jsonify({"message": f"An error occurred during registration"}),
            500,
        )


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    print(email)
    print(password)
    try:
        user = fetch_user_by_email(email)
    except Exception as e:
        return jsonify({"message": f"Error fetching user data"}), 500

    if not user:
        return (
            jsonify(
                {
                    "message": "Invalid email or password. Please check your credentials and try again."
                }
            ),
            400,
        )

    user_id = user[0]
    salt = get_user_salt(user_id)
    salt_bytes = bytes.fromhex(salt[0])
    hashed_password = hash_password(password, salt_bytes)

    current_time = time.time()
    status = fetch_user_login_status(email)

    if status["block_until"] > current_time:
        remaining_time = status["block_until"] - current_time
        return (
            jsonify(
                {
                    "message": f"Too many login attempts. Please try again after {int(remaining_time)} seconds."
                }
            ),
            403,
        )

    if status["attempts"] == MAX_ATTEMPTS and status["block_until"] < current_time:
        status["attempts"] = 0
        status["block_until"] = 0
        update_user_login_status(email, 0, 0)

    if authenticate_user(email, hashed_password):

        update_user_login_status(email, 0, 0)
        session["user_id"] = user_id
        return jsonify({"message": "Login successful! Welcome back."}), 200
    else:
        status["attempts"] += 1
        if status["attempts"] >= MAX_ATTEMPTS:
            block_until = current_time + BLOCK_TIME
            update_user_login_status(email, status["attempts"], block_until)
            return (
                jsonify(
                    {
                        "message": "Too many login attempts. Your account is temporarily blocked. Try again later."
                    }
                ),
                403,
            )
        else:
            update_user_login_status(email, status["attempts"], 0)
        return jsonify({"message": "Invalid email or password. Please try again."}), 400


@auth.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")
    user = fetch_user_by_email(email)

    if not email:
        return jsonify({"message": "Email address is required!"}), 400

    if not user:
        return jsonify({"message": "No account found with this email address."}), 400

    random_value = generate_salt(8)
    random_value_hex = random_value.hex()
    upsert_user_auth_code(user[0], random_value_hex)

    subject = "Password Reset Request"
    send_email(subject, email, random_value_hex)
    return (
        jsonify({"message": "Password reset email sent. Please check your inbox."}),
        200,
    )


@auth.route("/verify-auth-code", methods=["POST"])
def verify_auth_code():
    data = request.json
    email = data.get("email")
    user_sent_auth_code = data.get("auth_code")

    user = fetch_user_by_email(email)
    if not user:
        return jsonify({"message": "No account found with this email address."}), 400

    user_auth_code = get_auth_code(user[0])
    if user_auth_code[0] == user_sent_auth_code:
        return jsonify({"message": "Authentication code verified successfully."}), 200
    else:
        return (
            jsonify({"message": "Invalid authentication code. Please try again."}),
            400,
        )


@auth.route("/reset-forgot-password", methods=["POST"])
def reset_password():
    data = request.json
    email = data.get("email")
    new_password = data.get("new_password")

    user = fetch_user_by_email(email)
    if not user:
        return jsonify({"message": "No account found with this email address."}), 400

    if not validate_password(new_password):
        return (
            jsonify({"message": "New password does not meet the required complexity!"}),
            400,
        )

    if is_password_common(new_password):
        return (
            jsonify(
                {
                    "message": "The new password is too common. Please choose a more secure password."
                }
            ),
            400,
        )

    try:
        salt = generate_salt(password_config["password_requirements"]["salt_len"])
        hashed_password = hash_password(new_password, salt)
        if not check_password_history(user[0], new_password):
            return (
                jsonify(
                    {
                        "message": "New password cannot be the same as previous passwords. Please choose a different password."
                    }
                ),
                400,
            )

        salt_hex = salt.hex()
        old_salt = get_user_salt(user[0])
        add_password_to_history(user[0], user[4], old_salt[0])
        change_user_password_and_salt(user[0], hashed_password, salt_hex)
        return (
            jsonify(
                {
                    "message": "Password reset successful. You can now log in with your new password."
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify({"message": f"An error occurred while resetting the password"}),
            500,
        )


@auth.route("/login-reset-password", methods=["POST"])
def login_reset_password():
    data = request.json
    new_password = data.get("new_password")
    old_password = data.get("old_password")
    user_id = session.get("user_id")

    if not user_id:
        return (
            jsonify({"message": "You need to be logged in to change your password."}),
            400,
        )

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found. Please log in again."}), 400

    old_salt = get_user_salt(user_id)
    if not old_salt:
        return (
            jsonify({"message": "Failed to retrieve user salt. Please try again."}),
            500,
        )

    salt_bytes = bytes.fromhex(old_salt[0])
    old_hashed_password = hash_password(old_password, salt_bytes)

    if not validate_password(new_password):
        return (
            jsonify({"message": "New password does not meet the required complexity!"}),
            400,
        )

    if is_password_common(new_password):
        return (
            jsonify(
                {
                    "message": "The new password is too common. Please choose a more secure password."
                }
            ),
            400,
        )

    if old_hashed_password != user[4]:
        return jsonify({"message": "Old password is incorrect. Please try again."}), 400

    try:
        salt = generate_salt(password_config["password_requirements"]["salt_len"])
        new_hashed_password = hash_password(new_password, salt)

        if not check_password_history(user_id, new_password):
            return (
                jsonify(
                    {
                        "message": "New password cannot be the same as previous passwords. Please choose a different password."
                    }
                ),
                400,
            )

        salt_hex = salt.hex()
        change_user_password_and_salt(user_id, new_hashed_password, salt_hex)
        add_password_to_history(user_id, old_hashed_password, old_salt[0])
        return jsonify({"message": "Password updated successfully."}), 200
    except Exception as e:
        return (
            jsonify({"message": f"An error occurred while updating the password"}),
            500,
        )
