"""
Item Dialog - Add/Edit Inventory Item
"""
import customtkinter as ctk
from tkinter import filedialog
import os
import sys
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import InventoryItem, FeedingEntry


class ItemDialog(ctk.CTkToplevel):
    """Dialog for adding or editing an inventory item."""
    
    def __init__(self, parent, category: str, item: InventoryItem = None):
        super().__init__(parent)
        
        self.category = category
        self.item = item
        self.result = None
        self.selected_image_path = None
        
        # Window setup
        self.title("Edit Item" if item else "Add Item")
        self.geometry("500x650")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._build_ui()
        
        if item:
            self._populate_fields(item)
    
    def _build_ui(self):
        """Build the dialog UI."""
        # Main container with padding
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # === Basic Info ===
        ctk.CTkLabel(self.container, text="Basic Information", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        # Name
        ctk.CTkLabel(self.container, text="Name:").pack(anchor="w", pady=(10, 0))
        self.name_entry = ctk.CTkEntry(self.container, width=400)
        self.name_entry.pack(anchor="w")
        
        # Variant (morph, flavor, etc.)
        variant_label = "Morph:" if self.category == "animals" else "Variant:"
        ctk.CTkLabel(self.container, text=variant_label).pack(anchor="w", pady=(10, 0))
        self.variant_entry = ctk.CTkEntry(self.container, width=400)
        self.variant_entry.pack(anchor="w")
        
        # Price and Quantity row
        row_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        row_frame.pack(anchor="w", pady=(10, 0), fill="x")
        
        ctk.CTkLabel(row_frame, text="Price ($):").pack(side="left")
        self.price_entry = ctk.CTkEntry(row_frame, width=100)
        self.price_entry.pack(side="left", padx=(5, 20))
        
        ctk.CTkLabel(row_frame, text="Quantity:").pack(side="left")
        self.quantity_entry = ctk.CTkEntry(row_frame, width=80)
        self.quantity_entry.pack(side="left", padx=5)
        self.quantity_entry.insert(0, "1")
        
        # Status dropdown
        ctk.CTkLabel(self.container, text="Status:").pack(anchor="w", pady=(10, 0))
        self.status_var = ctk.StringVar(value="available")
        self.status_dropdown = ctk.CTkOptionMenu(
            self.container,
            values=["available", "reserved", "sold"],
            variable=self.status_var
        )
        self.status_dropdown.pack(anchor="w")
        
        # === Image ===
        ctk.CTkLabel(self.container, text="Image", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(20, 0))
        
        image_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        image_frame.pack(anchor="w", pady=5, fill="x")
        
        self.image_label = ctk.CTkLabel(image_frame, text="No image selected", text_color="gray")
        self.image_label.pack(side="left")
        
        self.image_btn = ctk.CTkButton(
            image_frame,
            text="Choose Image",
            width=120,
            command=self._select_image
        )
        self.image_btn.pack(side="right")
        
        # === Animals-specific fields ===
        if self.category == "animals":
            # Verified Feeder checkbox
            self.verified_var = ctk.BooleanVar(value=False)
            self.verified_check = ctk.CTkCheckBox(
                self.container,
                text="Verified Feeder",
                variable=self.verified_var
            )
            self.verified_check.pack(anchor="w", pady=(15, 0))
            
            # Feeding Log (simplified - last 3 meals)
            ctk.CTkLabel(
                self.container,
                text="Feeding Log (optional):",
                font=ctk.CTkFont(weight="bold")
            ).pack(anchor="w", pady=(15, 5))
            
            self.feeding_entries = []
            for i in range(3):
                feed_frame = ctk.CTkFrame(self.container, fg_color="transparent")
                feed_frame.pack(anchor="w", fill="x", pady=2)
                
                date_entry = ctk.CTkEntry(feed_frame, width=100, placeholder_text="Date")
                date_entry.pack(side="left", padx=(0, 5))
                
                food_entry = ctk.CTkEntry(feed_frame, width=200, placeholder_text="Food type")
                food_entry.pack(side="left")
                
                self.feeding_entries.append((date_entry, food_entry))
        
        # === Action Buttons ===
        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
            command=self.destroy
        )
        self.cancel_btn.pack(side="left")
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="Save",
            command=self._save
        )
        self.save_btn.pack(side="right")
    
    def _select_image(self):
        """Open file dialog to select an image."""
        filetypes = [
            ("Images", "*.png *.jpg *.jpeg *.gif *.webp"),
            ("All files", "*.*")
        ]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        
        if filepath:
            self.selected_image_path = filepath
            filename = os.path.basename(filepath)
            self.image_label.configure(text=filename, text_color="white")
    
    def _populate_fields(self, item: InventoryItem):
        """Populate fields when editing an existing item."""
        self.name_entry.insert(0, item.name)
        self.variant_entry.insert(0, item.variant)
        self.price_entry.insert(0, str(item.price))
        self.quantity_entry.delete(0, "end")
        self.quantity_entry.insert(0, str(item.quantity))
        self.status_var.set(item.status)
        
        if item.image:
            self.image_label.configure(text=os.path.basename(item.image), text_color="white")
        
        if self.category == "animals":
            self.verified_var.set(item.verified_feeder)
            
            # Populate feeding log
            for i, entry in enumerate(item.feeding_log[:3]):
                self.feeding_entries[i][0].insert(0, entry.date)
                self.feeding_entries[i][1].insert(0, entry.food_type)
    
    def _save(self):
        """Validate and save the item."""
        # Validate required fields
        name = self.name_entry.get().strip()
        variant = self.variant_entry.get().strip()
        
        if not name:
            self._show_error("Name is required")
            return
        
        try:
            price = float(self.price_entry.get() or 0)
            quantity = int(self.quantity_entry.get() or 0)
        except ValueError:
            self._show_error("Invalid price or quantity")
            return
        
        # Determine image path
        image_path = ""
        if self.selected_image_path:
            # Copy image to local assets and set path
            filename = os.path.basename(self.selected_image_path)
            # For now, just store the filename - actual copy happens on publish
            image_path = f"Assets/{filename}"
            
            # Copy to local assets folder
            local_assets = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
            os.makedirs(local_assets, exist_ok=True)
            shutil.copy2(self.selected_image_path, os.path.join(local_assets, filename))
        elif self.item and self.item.image:
            image_path = self.item.image
        
        # Build feeding log for animals
        feeding_log = []
        if self.category == "animals":
            for date_entry, food_entry in self.feeding_entries:
                date = date_entry.get().strip()
                food = food_entry.get().strip()
                if date and food:
                    feeding_log.append(FeedingEntry(date=date, food_type=food))
        
        # Create item
        item_id = self.item.id if self.item else InventoryItem.generate_id(self.category)
        
        self.result = InventoryItem(
            id=item_id,
            category=self.category,
            name=name,
            variant=variant,
            price=price,
            quantity=quantity,
            image=image_path,
            status=self.status_var.get(),
            verified_feeder=self.verified_var.get() if self.category == "animals" else False,
            feeding_log=feeding_log
        )
        
        self.destroy()
    
    def _show_error(self, message: str):
        """Show an error message."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x100")
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        ctk.CTkLabel(error_dialog, text=message).pack(pady=20)
        ctk.CTkButton(error_dialog, text="OK", command=error_dialog.destroy).pack()
