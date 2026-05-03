import customtkinter as ctk
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
import threading

class Map:
    def __init__(self, app):
        self.app = app
        self.lat = None
        self.lon = None
        self.address = None
        self.map_window = None
        self.marker = None
        self.geolocator = Nominatim(user_agent="MAPS_eCycle_app")

    def get_map(self, callback):
        self.callback = callback
        self.map_window = ctk.CTkToplevel(self.app)
        self.map_window.title("Select Location")
        self.map_window.geometry("1200x800")


        self.map_widget = TkinterMapView(self.map_window, width=780, height=500, corner_radius=10)
        self.map_widget.pack(pady=20)


        self.map_widget.set_position(28.6139, 77.2090)
        self.map_widget.set_zoom(10)


        self.map_widget.add_left_click_map_command(self.get_clicked_position)


        self.address_label = ctk.CTkLabel(self.map_window, text="Click on the map to select location", wraplength=700)
        self.address_label.pack(pady=10)


        confirm_btn = ctk.CTkButton(self.map_window, text="Confirm Location", command=self.confirm_location)
        confirm_btn.pack(pady=10)

    def get_clicked_position(self, coords):
        self.lat, self.lon = coords

        self.address_label.configure(text="Fetching address...")


        threading.Thread(target=self.fetch_address, daemon=True).start()

    def fetch_address(self):
        try:
            if self.lat is None or self.lon is None:
                self.address_label.configure(text="Coordinates not set")
                return

            location = self.geolocator.reverse((self.lat, self.lon), language="en", exactly_one=True)
            if location and location.address:
                self.address = location.address
                self.address_label.configure(text=f"Address: {self.address}")
            else:
                self.address_label.configure(text="Address not found")
        except Exception as e:
            self.address_label.configure(text=f"Error: {str(e)}")

    def confirm_location(self):
        if self.callback and self.address:
            self.callback(self.address)
        self.map_window.destroy()