import sqlite3
import random

# Voivodeships with some cities visited
voivodeships = {
    'Lower Silesian': [('Wrocław', 51.1079, 17.0385), ('Legnica', 51.2070, 16.1555), ('Jelenia Góra', 50.9045, 15.7389)],
    'Kuyavian-Pomeranian': [('Bydgoszcz', 53.1235, 18.0084), ('Toruń', 53.0138, 18.5984), ('Włocławek', 52.6482, 19.0677)],
    'Lublin': [('Lublin', 51.2465, 22.5684), ('Zamość', 50.7214, 23.2516), ('Chełm', 51.1431, 23.4718)],
    'Lubusz': [('Zielona Góra', 51.9356, 15.5062), ('Gorzów Wielkopolski', 52.7368, 15.2288)],
    'Łódź': [('Łódź', 51.7592, 19.4550), ('Piotrków Trybunalski', 51.4056, 19.7038), ('Pabianice', 51.6643, 19.3542)],
    'Lesser Poland': [('Kraków', 50.0647, 19.9450), ('Tarnów', 50.0121, 20.9858), ('Nowy Sącz', 49.6217, 20.6970)],
    'Masovian': [('Warsaw', 52.2297, 21.0122), ('Radom', 51.4027, 21.1471), ('Płock', 52.5463, 19.7065)],
    'Opole': [('Opole', 50.6751, 17.9213), ('Nysa', 50.4746, 17.3325), ('Brzeg', 50.8600, 17.4672)],
    'Podkarpackie': [('Rzeszów', 50.0413, 21.9990), ('Przemyśl', 49.7840, 22.7675), ('Krosno', 49.6881, 21.7705)],
    'Podlaskie': [('Białystok', 53.1325, 23.1688), ('Łomża', 53.1780, 22.0593), ('Suwałki', 54.0996, 22.9332)],
    'Pomeranian': [('Gdańsk', 54.3520, 18.6466), ('Sopot', 54.4416, 18.5601), ('Gdynia', 54.5189, 18.5305)],
    'Silesian': [('Katowice', 50.2649, 19.0238), ('Gliwice', 50.2945, 18.6714), ('Częstochowa', 50.8115, 19.1203)],
    'Holy Cross': [('Kielce', 50.8661, 20.6286), ('Sandomierz', 50.6821, 21.7487)],
    'Warmian-Masurian': [('Olsztyn', 53.7784, 20.4801), ('Elbląg', 54.1524, 19.4082), ('Ełk', 53.8286, 22.3646)],
    'Greater Poland': [('Poznań', 52.4064, 16.9252), ('Kalisz', 51.7611, 18.0910), ('Konin', 52.2234, 18.2516)],
    'West Pomeranian': [('Szczecin', 53.4285, 14.5528), ('Koszalin', 54.1944, 16.1722), ('Stargard', 53.3365, 15.0496)]
}

# Connect or create DB
conn = sqlite3.connect('visits.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    voivodeship TEXT NOT NULL
)
''')

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

# Insert users
users = [(i + 1, f'User_{i + 1}', v) for i, v in enumerate(voivodeships.keys())]
cursor.executemany('INSERT INTO users (id, name, voivodeship) VALUES (?, ?, ?)', users)

# Insert cities per user
for user_id, voivodeship in enumerate(voivodeships.keys(), start=1):
    cities = random.sample(voivodeships[voivodeship], min(10, len(voivodeships[voivodeship])))
    for city_name, lat, lon in cities:
        cursor.execute('INSERT INTO visited_cities (user_id, city_name, latitude, longitude) VALUES (?, ?, ?, ?)',
                       (user_id, city_name, lat, lon))

# Commit & close
conn.commit()
conn.close()

print("Database 'visits.db' created with users and visited cities.")