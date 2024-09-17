from sqlalchemy import text
from flask import jsonify
from .. import db
from ..config.config_functions import hash_password, password_config
from sqlalchemy.exc import SQLAlchemyError


def add_new_user(first_name, last_name, email, hashed_password, salt_hex):
    query = text(
        f"INSERT INTO users (first_name, last_name, email, hashed_password) VALUES ('{first_name}', '{last_name}', '{email}', '{hashed_password}')"
    )
    print(query)
    db.session.execute(query)
    db.session.commit()


# sqli # john', 'do123e', 'john123456@example123.com', 'password') # '


def add_user_salt(user_id, salt_hex):
    query = text(
        f"INSERT INTO user_salts (user_id, salt) VALUES ('{user_id}', '{salt_hex}')"
    )
    db.session.execute(query)
    db.session.commit()


def fetch_user_by_email(email):
    query = text(f"SELECT * FROM users WHERE email = '{email}'")
    result = db.session.execute(query).fetchone()
    return result


def get_user_by_id(user_id):
    query = text(f"SELECT * FROM users WHERE id = '{user_id}'")
    result = db.session.execute(query).fetchone()
    return result


def get_user_salt(user_id):
    query = text(f"SELECT salt FROM user_salts WHERE user_id = '{user_id}'")
    salt = db.session.execute(query).fetchone()
    return salt


def upsert_user_auth_code(user_id, auth_code):
    query = text(f"SELECT COUNT(*) FROM user_auth_codes WHERE user_id = '{user_id}'")
    result = db.session.execute(query).scalar()

    if result > 0:
        query = text(
            f"UPDATE user_auth_codes SET auth_code = '{auth_code}' WHERE user_id = '{user_id}'"
        )
        db.session.execute(query)
    else:
        query = text(
            f"INSERT INTO user_auth_codes (user_id, auth_code) VALUES ('{user_id}', '{auth_code}')"
        )
        db.session.execute(query)

    db.session.commit()


def get_auth_code(id):
    query = text(f"SELECT auth_code FROM user_auth_codes WHERE user_id = '{id}'")
    auth_code = db.session.execute(query).fetchone()
    return auth_code


def change_user_password_and_salt(user_id, new_hashed_password, new_salt):
    query = text(
        f"UPDATE users SET hashed_password = '{new_hashed_password}' WHERE id = '{user_id}'"
    )
    db.session.execute(query)
    db.session.commit()

    query = text(
        f"UPDATE user_salts SET salt = '{new_salt}' WHERE user_id = '{user_id}'"
    )
    db.session.execute(query)
    db.session.commit()


def add_new_client(email, first_name, last_name, address, phone_number, user_id):
    query = text(
        f"INSERT INTO clients (first_name, last_name, email, phone_number, address, user_id) VALUES ('{first_name}', '{last_name}', '{email}', '{phone_number}', '{address}', '{user_id}')"
    )
    print(query)
    db.session.execute(query)
    db.session.commit()


# sql# Robert', 'hazut', 'kobihazut8@gmail.com', '0503456747', 'belkind shimson 2', 56); DROP TABLE clients; --"
# sqli# john', 'doe', 'jon123456@example123.com', '1234567890', 'address', 56) #
# make sure to have a right user_id


def fetch_all_clients_by_user_id(user_id):
    query = text(f"SELECT * FROM clients WHERE user_id = '{user_id}'")
    clients = db.session.execute(query).fetchall()
    return clients


def check_password_history(user_id, new_password):
    query = text(
        f"SELECT hashed_password, salt FROM password_history WHERE user_id = '{user_id}'"
    )
    result = db.session.execute(query).fetchall()
    for row in result:
        stored_hashed_password = row[0]
        salt = row[1]
        salt_bytes = bytes.fromhex(salt)
        hashed_new_password = hash_password(new_password, salt_bytes)
        if hashed_new_password == stored_hashed_password:
            return False
    return True


def add_password_to_history(user_id, old_hashed_password, old_salt):
    query = text(f"SELECT COUNT(*) FROM password_history WHERE user_id = '{user_id}'")
    count_result = db.session.execute(query)
    password_count = count_result.scalar()
    config = password_config["password_requirements"]

    if password_count == config["history"]:
        query = text(
            f"DELETE FROM password_history WHERE user_id = '{user_id}' ORDER BY created_at ASC LIMIT 1"
        )
        db.session.execute(query)

    query = text(
        f"INSERT INTO password_history (user_id, hashed_password, salt) VALUES ('{user_id}', '{old_hashed_password}', '{old_salt}')"
    )
    db.session.execute(query)
    db.session.commit()


def fetch_user_login_status(email):
    query = text(
        f"SELECT login_attempts, block_until FROM user_login_status WHERE email = '{email}'"
    )
    result = db.session.execute(query).fetchone()

    if result:
        return {"attempts": result[0], "block_until": result[1]}
    else:
        return {"attempts": 0, "block_until": 0}


def update_user_login_status(email, attempts, block_until):
    query = text(
        """
        INSERT INTO user_login_status (email, login_attempts, block_until)
        VALUES (:email, :attempts, :block_until)
        ON DUPLICATE KEY UPDATE login_attempts = VALUES(login_attempts), block_until = VALUES(block_until)
        """
    )

    db.session.execute(
        query,
        {
            "email": email,
            "attempts": attempts,
            "block_until": block_until,
        },
    )
    db.session.commit()


def delete_client_by_id(client_id):
    query = text(f"DELETE FROM clients WHERE id = '{client_id}'")
    db.session.execute(query)
    db.session.commit()


def authenticate_user(email, hashed_password):
    query = text(
        f"SELECT * FROM users WHERE email = '{email}' AND hashed_password = '{hashed_password}' LIMIT 1"
    )
    result = db.session.execute(query).fetchone()
    return result
    # sqli# admin' OR 1=1#
