import folium
import sqlite3

# Define color per user
colors = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige',
    'darkblue', 'darkgreen', 'cadetblue', 'pink', 'lightblue', 'lightgreen',
    'gray', 'black'
]

# Connect to DB
conn = sqlite3.connect('visits.db')
cursor = conn.cursor()

# Query DB => cities with users
cursor.execute('''
SELECT users.name, visited_cities.city_name, visited_cities.latitude, visited_cities.longitude, users.id
FROM visited_cities
JOIN users ON visited_cities.user_id = users.id
''')
city_data = cursor.fetchall()

# Create map centred on PL
poland_map = folium.Map(location=[52.2297, 21.0122], zoom_start=6)

# Add city dot markers per user
for user_name, city, lat, lon, user_id in city_data:
    folium.CircleMarker(
        location=[lat, lon],
        radius=6,               # Size of the dot
        color=colors[user_id - 1],  # Color based on user ID
        fill=True,
        fill_color=colors[user_id - 1],  # Same color for the fill
        fill_opacity=0.6,
        popup=f'{city} - {user_name}'    # Show city and user info in the popup
    ).add_to(poland_map)

# Save map to HTML file
poland_map.save('visits_map.html')

# Close conn
conn.close()

print("Map with visited cities created and saved as 'visits_map.html'")