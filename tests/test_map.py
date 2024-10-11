import folium
import sqlite3
import os
from create_db import create_db, voivodeships


def test_db_creation():
    # Check if DB already exists and remove if it is
    if os.path.exists('visits.db'):
        os.remove('visits.db')

    # Import and run create_db function
    create_db()
    assert os.path.exists('visits.db')

    # Connect to DB
    conn = sqlite3.connect('visits.db')
    cursor = conn.cursor()

    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    users_table = cursor.fetchone()
    assert users_table is not None

    # Check if visited_cities table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='visited_cities';")
    cities_table = cursor.fetchone()
    assert cities_table is not None

    # Verify if records are inserted in the users table
    cursor.execute("SELECT COUNT(*) FROM users;")
    users_count = cursor.fetchone()[0]
    assert users_count == len(voivodeships)

    # Verify if records are inserted in the visited_cities table
    cursor.execute("SELECT COUNT(*) FROM visited_cities;")
    cities_count = cursor.fetchone()[0]
    assert cities_count > 0

    # Clean up and remove DB
    conn.close()
    os.remove('visits.db')


def test_map_creation():
    # Create in-memory DB
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create a table called 'cities'
    cursor.execute('''CREATE TABLE cities (city_name TEXT, latitude REAL, longitude REAL, user_id INTEGER)''')
    cities = cursor.fetchall()

    # Insert sample data to the table
    cursor.executemany('''INSERT INTO cities (city_name, latitude, longitude, user_id) VALUES (?, ?, ?, ?)''',
                       [('Warsaw', 52.2297, 21.0122, 1), ('Krakow', 50.0647, 19.9450, 2),])
    conn.commit()

    # Initialize map centred to Poland
    m = folium.Map(location=[52.2297, 21.0122], zoom_start=6)

    # Loop to add markers to the map
    for city in cities:
        folium.CircleMarker(location=[city[1], city[2]], radius=5).add_to(m)

    # Save map to HTML file and check if success
    map_path = 'test_map.html'
    m.save(map_path)
    assert os.path.exists(map_path)

    # Clean up and remove map
    conn.close()
    os.remove(map_path)
