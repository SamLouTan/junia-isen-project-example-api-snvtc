from flask import Flask, jsonify
from db.connection import connect_to_db  # Import pour la connexion
import psycopg2
import json
from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException

# Charger le fichier .env situé à la racine du projet
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))


app = Flask(__name__)

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
