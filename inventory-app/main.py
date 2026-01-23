"""
Cold Blooded Heartbeats - Inventory Manager
Main Application Entry Point
"""
import customtkinter as ctk
from ui.main_window import MainWindow


def main():
    """Launch the inventory manager application."""
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Create and run app
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
