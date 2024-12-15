import os
import psycopg2
from psycopg2 import sql
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../var.env"))

def connect_to_db():
    print("ON RENTRE DANS LA BOUCLE DE CONNECTION")

    """Crée et retourne une connexion à la base de données PostgreSQL."""
    try:
        


        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            sslmode="verify-full",
            options='-c client_encoding=UTF8'  # Force l'encodage UTF-8
        )
        return conn
        
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        raise
