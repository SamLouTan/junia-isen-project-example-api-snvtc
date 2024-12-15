from connection import connect_to_db

def create_tables():
    """Création des tables et insertion des données par défaut."""
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Création des tables
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            price FLOAT NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS baskets (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            item_id INT REFERENCES items(item_id) ON DELETE CASCADE,
            quantity INT NOT NULL CHECK (quantity > 0),
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Insertion de données par défaut
        cur.execute("""
        INSERT INTO users (username, email)
        SELECT 'testuser', 'testuser@example.com'
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'testuser');
        """)

        cur.execute("""
        INSERT INTO items (name, description, price)
        SELECT 'example_item', 'An example item description', 10.0
        WHERE NOT EXISTS (SELECT 1 FROM items WHERE name = 'example_item');
        """)

        conn.commit()
        print("Tables créées et données insérées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création des tables: {e}")
        raise
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    create_tables()
