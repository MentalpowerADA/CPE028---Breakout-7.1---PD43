import requests
import tkinter as tk
from tkinter import messagebox
from colorama import init

init(autoreset=True)

MAPQUEST_API_KEY = 'kGy1LxHWOWVrMDJcmvd6rDOeKznoT6AF'

def get_ip():
    response = requests.get('https://api.ipify.org?format=json').json()
    return response["ip"]

def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return {
        "IPv4 Address": ip_address,
        "City": response.get("city"),
        "Region": response.get("region"),
        "Country": response.get("country_name"),
        "Latitude": response.get("latitude"),
        "Longitude": response.get("longitude")
    }

def get_directions(from_location, to_location, use_metric):
    url = "http://www.mapquestapi.com/directions/v2/route"
    params = {
        "key": MAPQUEST_API_KEY,
        "from": from_location,
        "to": to_location,
        "unit": "k" if use_metric else "m"
    }
    response = requests.get(url, params=params).json()
    
    # Print the response for debugging purposes
    print("API Response:", response)
    
    if response.get("info").get("statuscode") != 0:
        messagebox.showerror("Error", "Could not retrieve directions. Please check your input.")
        return None

    route = response.get("route")
    maneuvers = route.get("legs")[0].get("maneuvers", [])
    
    directions_list = [
        f"Distance: {route['distance']} {'km' if use_metric else 'miles'}",
        f"Estimated Travel Time: {route['formattedTime']}",
        "\nTurn-by-Turn Directions:"
    ]
    
    for i, maneuver in enumerate(maneuvers, start=1):
        distance = maneuver['distance'] * 1000 if use_metric else maneuver['distance'] * 1609.34
        instructions = maneuver['narrative']
        directions_list.append(f"{i}. {instructions} ({round(distance, 2)} {'meters' if use_metric else 'feet'})")

    return "\n".join(directions_list)

def display_location_data(location_data):
    location_text = (
        f"IPv4 Address: {location_data['IPv4 Address']}\n"
        f"City: {location_data['City']}\n"
        f"Region: {location_data['Region']}\n"
        f"Country: {location_data['Country']}\n"
        f"Latitude: {location_data['Latitude']}\n"
        f"Longitude: {location_data['Longitude']}"
    )
    return location_text

def fetch_data():
    from_location = from_entry.get()
    to_location = to_entry.get()
    use_metric = metric_var.get() == 1

    ip_address = get_ip()
    location_data = get_location(ip_address)
    location_output.config(state="normal")
    location_output.delete(1.0, tk.END)
    location_output.insert(tk.END, display_location_data(location_data))
    location_output.config(state="disabled")

    # Fetch and display directions
    directions = get_directions(from_location, to_location, use_metric)
    if directions:
        directions_output.config(state="normal")
        directions_output.delete(1.0, tk.END)
        directions_output.insert(tk.END, directions)
        directions_output.config(state="disabled")

# Set up the main application window
app = tk.Tk()
app.title("MapQuest Directions")
app.geometry("600x600")

# Entry for "From" location
tk.Label(app, text="Starting Location (From):").pack(pady=5)
from_entry = tk.Entry(app, width=50)
from_entry.pack(pady=5)

# Entry for "To" location
tk.Label(app, text="Destination Location (To):").pack(pady=5)
to_entry = tk.Entry(app, width=50)
to_entry.pack(pady=5)

# Option for selecting metric or imperial system
metric_var = tk.IntVar(value=1)
tk.Label(app, text="Select Unit System:").pack(pady=5)
metric_radio = tk.Radiobutton(app, text="Metric (km, meters)", variable=metric_var, value=1)
metric_radio.pack()
imperial_radio = tk.Radiobutton(app, text="Imperial (miles, feet)", variable=metric_var, value=0)
imperial_radio.pack()

# Button to fetch directions
fetch_button = tk.Button(app, text="Get Directions", command=fetch_data)
fetch_button.pack(pady=10)

# Text box for location output
tk.Label(app, text="Current Location Information:").pack(pady=5)
location_output = tk.Text(app, width=60, height=7, wrap="word", state="disabled")
location_output.pack(pady=5)

# Text box for directions output
tk.Label(app, text="Directions Information:").pack(pady=5)
directions_output = tk.Text(app, width=60, height=15, wrap="word", state="disabled")
directions_output.pack(pady=5)

app.mainloop()
