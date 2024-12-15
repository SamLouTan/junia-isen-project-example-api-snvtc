import os
import json
import psycopg2
from flask import Flask, jsonify, request
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis le fichier .env
from db.connection import connect_to_db  # Import pour la connexion
import psycopg2
import json
from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException

# Charger le fichier .env situé à la racine du projet
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))


app = Flask(__name__)

# Fonction pour récupérer les variables d'environnement
def get_environment_variable(key, default=None):
    value = os.environ.get(key, default)
    if value is None:
        raise RuntimeError(f"{key} does not exist")
    return value


# Connexion à la base de données PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        host=get_environment_variable("DATABASE_HOST"),
        port=get_environment_variable("DATABASE_PORT", "5432"),
        database=get_environment_variable("DATABASE_NAME"),
        user=get_environment_variable("DATABASE_USER"),
        password=get_environment_variable("DATABASE_PASSWORD"),
        connect_timeout=1,
    )
    return conn

# Route pour créer les tables avec SQL pur
@app.route('/create_tables', methods=['GET'])
def create_tables():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Création des tables
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL
        );
        """
        cur.execute(create_users_table)

        create_items_table = """
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL
        );
        """
        cur.execute(create_items_table)

        create_baskets_table = """
        CREATE TABLE IF NOT EXISTS baskets (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            basket_content JSON NOT NULL
        );
        """
        cur.execute(create_baskets_table)

        # Insertion de données par défaut
        insert_data_users = """
        INSERT INTO users (username, email)
        SELECT 'testuser', 'testuser@example.com'
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE username = 'testuser'
        );
        """
        cur.execute(insert_data_users)

        insert_data_items = """
        INSERT INTO items (name, description)
        SELECT 'example_item', 'An example item description'
        WHERE NOT EXISTS (
            SELECT 1 FROM items WHERE name = 'example_item'
        );
        """
        cur.execute(insert_data_items)

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Tables créées et données insérées avec succès!"}), 200
    except psycopg2.Error as error:
        return jsonify({"error": f"Erreur lors de la création des tables: {str(error)}"}), 500

# Route de base
@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur l'API Flask!"})


# Route pour récupérer les items
@app.route('/items', methods=['GET'])
def get_items():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT item_id, name, description, price FROM items")
        items = cur.fetchall()
        items_list = [{"item_id": item[0], "name": item[1], "description": item[2], "price":item[3]} for item in items]
        return jsonify({"items": items_list})
    except psycopg2.OperationalError as error:
        return jsonify({"error": str(error)}), 500
    finally:
        cur.close()
        conn.close()

# Route pour récupérer le contenu des paniers
@app.route('/baskets', methods=['GET'])
def get_baskets():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT user_id, item_id, quantity, price FROM baskets group by user_id, item_id, quantity, price")
        baskets = cur.fetchall()
        baskets_list = [{"user_id": basket[0], "item_id":basket[1], "quantity":basket[2], "price":basket[3]} for basket in baskets]
        return jsonify({"baskets": baskets_list})
    except psycopg2.OperationalError as error:
        return jsonify({"error": str(error)}), 500
    finally:
        cur.close()
        conn.close()

# Route pour récupérer les utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, firstname, lastname, age FROM users")
        users = cur.fetchall()
        users_list = [{"id": user[0], "username": user[1], "email": user[2], "firstname":user[3], "lastname":user[4], "age":user[5]} for user in users]
        return jsonify({"users": users_list})
    except psycopg2.OperationalError as error:
        return jsonify({"error": str(error)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
