import sqlite3
import random

# Voivodeships with some cities visited
voivodeships = {
    'Lower Silesian': [('Wrocław', 51.1079, 17.0385), ('Legnica', 51.2070, 16.1555),
                       ('Jelenia Góra', 50.9045, 15.7389)],
    # ... (other voivodeships and cities)
}


def create_db():
    try:
        # Connect or create DB
        conn = sqlite3.connect('visits.db')
        conn.execute("PRAGMA foreign_keys = 1")  # Enable foreign key support
        cursor = conn.cursor()
        print("Connected to database.")

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            voivodeship TEXT NOT NULL
        )
        ''')
        print("Users table created.")

        # Create cities table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS visited_cities (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            city_name TEXT,
            latitude REAL,
            longitude REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        print("Visited cities table created.")

        # Insert users
        users = [(i + 1, f'User_{i + 1}', v) for i, v in enumerate(voivodeships.keys())]
        cursor.executemany('INSERT INTO users (id, name, voivodeship) VALUES (?, ?, ?)', users)
        print("Users inserted into the table.")

        # Insert cities per user
        for user_id, voivodeship in enumerate(voivodeships.keys(), start=1):
            cities = random.sample(voivodeships[voivodeship], min(10, len(voivodeships[voivodeship])))
            for city_name, lat, lon in cities:
                cursor.execute(
                    'INSERT INTO visited_cities (user_id, city_name, latitude, longitude) VALUES (?, ?, ?, ?)',
                    (user_id, city_name, lat, lon))
        print("Cities inserted into the table.")

        # Commit & close
        conn.commit()
        print("Database commit successful.")
        conn.close()
        print("Database connection closed.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


create_db()
