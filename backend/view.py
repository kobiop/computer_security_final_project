from flask import Blueprint, request, jsonify, session
from .database.queries import (
    add_new_client,
    fetch_all_clients_by_user_id,
    delete_client_by_id,
)

view = Blueprint("view", __name__)


@view.route("/add-client", methods=["POST"])
def add_client():
    data = request.json
    client_data = data.get("clientData")
    email = client_data.get("email")
    first_name = client_data.get("firstName")
    last_name = client_data.get("lastName")
    address = client_data.get("address")
    phone_number = client_data.get("phoneNumber")
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"message": "User not logged in!"}), 401

    if not all([email, first_name, last_name, address, phone_number]):
        return jsonify({"message": "All client fields are required!"}), 400

    try:
        print("1")
        add_new_client(email, first_name, last_name, address, phone_number, user_id)
        print("2")
        return jsonify({"message": "Client added successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to add client"}), 500


@view.route("/clients", methods=["GET"])
def clients():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "User not logged in!"}), 401

    try:
        all_clients = fetch_all_clients_by_user_id(user_id)

        clients_list = []
        for client in all_clients:
            client_dict = {
                "id": client.id,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "email": client.email,
                "phone_number": client.phone_number,
                "address": client.address,
                "user_id": client.user_id,
            }
            clients_list.append(client_dict)

        return jsonify({"clients": clients_list}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred while retrieving clients."}), 500


@view.route("/delete", methods=["POST"])
def delete_client():
    data = request.get_json()
    client_id = data.get("id")

    if not client_id:
        return jsonify({"message": "Client ID is required"}), 400

    try:
        delete_client_by_id(client_id)
        return jsonify({"message": "Client deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to delete client"}), 500
