"""
Main Window - Inventory Manager
"""
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage import Storage
from github_api import GitHubPublisher
from models import CATEGORIES, InventoryItem
from ui.item_dialog import ItemDialog


class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Cold Blooded Heartbeats - Inventory Manager")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Initialize storage and publisher
        self.storage = Storage()
        self.publisher = GitHubPublisher()
        
        # Current category filter
        self.current_category = "animals"
        
        # Build UI
        self._build_ui()
        self._refresh_list()
    
    def _build_ui(self):
        """Build the main UI layout."""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # === Left Sidebar ===
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🐍 CBH Inventory",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(pady=20, padx=10)
        
        # Category buttons
        self.category_buttons = {}
        for cat in CATEGORIES:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{cat['icon']} {cat['label']}",
                anchor="w",
                command=lambda c=cat['id']: self._select_category(c)
            )
            btn.pack(pady=5, padx=10, fill="x")
            self.category_buttons[cat['id']] = btn
        
        # Spacer
        ctk.CTkLabel(self.sidebar, text="").pack(expand=True)
        
        # Publish button
        self.publish_btn = ctk.CTkButton(
            self.sidebar,
            text="📤 Publish to Website",
            fg_color="#1A3C40",
            hover_color="#2A4C50",
            command=self._publish
        )
        self.publish_btn.pack(pady=10, padx=10, fill="x")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_label.pack(pady=10)
        
        # === Main Content Area ===
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)
        
        # Header with title and add button
        self.header = ctk.CTkFrame(self.content, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header.grid_columnconfigure(0, weight=1)
        
        self.category_title = ctk.CTkLabel(
            self.header,
            text="Live Animals",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.category_title.grid(row=0, column=0, sticky="w")
        
        self.add_btn = ctk.CTkButton(
            self.header,
            text="+ Add Item",
            width=120,
            command=self._add_item
        )
        self.add_btn.grid(row=0, column=1, sticky="e")
        
        # Search bar
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self._refresh_list())
        self.search_entry = ctk.CTkEntry(
            self.content,
            placeholder_text="Search items...",
            textvariable=self.search_var
        )
        self.search_entry.grid(row=1, column=0, sticky="ew", pady=(10, 10))
        
        # Scrollable item list
        self.item_list = ctk.CTkScrollableFrame(self.content)
        self.item_list.grid(row=2, column=0, sticky="nsew")
        self.item_list.grid_columnconfigure(0, weight=1)
        
        # Set initial category
        self._select_category("animals")
    
    def _select_category(self, category: str):
        """Switch to a different category."""
        self.current_category = category
        
        # Update button styles
        for cat_id, btn in self.category_buttons.items():
            if cat_id == category:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            else:
                btn.configure(fg_color="transparent")
        
        # Update title
        for cat in CATEGORIES:
            if cat['id'] == category:
                self.category_title.configure(text=f"{cat['icon']} {cat['label']}")
                break
        
        self._refresh_list()
    
    def _refresh_list(self):
        """Refresh the item list."""
        # Clear existing items
        for widget in self.item_list.winfo_children():
            widget.destroy()
        
        # Get filtered items
        items = self.storage.get_by_category(self.current_category)
        
        # Apply search filter
        search_term = self.search_var.get().lower()
        if search_term:
            items = [
                item for item in items
                if search_term in item.name.lower() or search_term in item.variant.lower()
            ]
        
        if not items:
            empty_label = ctk.CTkLabel(
                self.item_list,
                text="No items found. Click '+ Add Item' to get started.",
                text_color="gray"
            )
            empty_label.pack(pady=50)
            return
        
        # Create item cards
        for item in items:
            self._create_item_card(item)
    
    def _create_item_card(self, item: InventoryItem):
        """Create a card for an inventory item."""
        card = ctk.CTkFrame(self.item_list)
        card.pack(fill="x", pady=5, padx=5)
        card.grid_columnconfigure(1, weight=1)
        
        # Stock indicator
        stock_color = "#4CAF50" if item.quantity > 0 else "#F44336"
        stock_text = "In Stock" if item.quantity > 0 else "Out of Stock"
        
        # Info section
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{item.name} - {item.variant}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(anchor="w")
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=f"ID: {item.id} | ${item.price:.2f} | Qty: {item.quantity}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        details_label.pack(anchor="w")
        
        stock_label = ctk.CTkLabel(
            info_frame,
            text=stock_text,
            font=ctk.CTkFont(size=11),
            text_color=stock_color
        )
        stock_label.pack(anchor="w")
        
        # Action buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e", padx=10)
        
        edit_btn = ctk.CTkButton(
            btn_frame,
            text="Edit",
            width=70,
            command=lambda i=item: self._edit_item(i)
        )
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=70,
            fg_color="#C62828",
            hover_color="#B71C1C",
            command=lambda i=item: self._delete_item(i)
        )
        delete_btn.pack(side="left", padx=5)
    
    def _add_item(self):
        """Open dialog to add a new item."""
        dialog = ItemDialog(self, category=self.current_category)
        self.wait_window(dialog)
        
        if dialog.result:
            self.storage.add(dialog.result)
            self._refresh_list()
            self.status_label.configure(text="Item added")
    
    def _edit_item(self, item: InventoryItem):
        """Open dialog to edit an item."""
        dialog = ItemDialog(self, category=self.current_category, item=item)
        self.wait_window(dialog)
        
        if dialog.result:
            self.storage.update(item.id, dialog.result)
            self._refresh_list()
            self.status_label.configure(text="Item updated")
    
    def _delete_item(self, item: InventoryItem):
        """Delete an item with confirmation."""
        if messagebox.askyesno("Confirm Delete", f"Delete '{item.name} - {item.variant}'?"):
            self.storage.delete(item.id)
            self._refresh_list()
            self.status_label.configure(text="Item deleted")
    
    def _publish(self):
        """Publish inventory to GitHub."""
        if not self.publisher.is_configured():
            messagebox.showerror(
                "Configuration Error",
                "GitHub is not configured.\n\n"
                "Please copy config.example.json to config.json and add your GitHub token."
            )
            return
        
        self.status_label.configure(text="Publishing...")
        self.publish_btn.configure(state="disabled")
        self.update()
        
        # Get inventory JSON
        inventory_json = self.storage.get_json_string()
        inventory_path = self.publisher.config.get("inventory_path", "docs/inventory.json")
        
        # Publish
        success, message = self.publisher.publish_file(
            inventory_path,
            inventory_json,
            "Update inventory from desktop app"
        )
        
        self.publish_btn.configure(state="normal")
        
        if success:
            self.status_label.configure(text="Published!")
            messagebox.showinfo("Success", "Inventory published to GitHub!\n\nWebsite will update in a few minutes.")
        else:
            self.status_label.configure(text="Publish failed")
            messagebox.showerror("Publish Error", message)
