"""
Local JSON Storage for Inventory
"""
import json
import os
from typing import List, Optional
from models import InventoryItem


class Storage:
    """Handles reading/writing inventory data to local JSON file."""
    
    def __init__(self, filepath: Optional[str] = None):
        if filepath is None:
            # Default to the same directory as storage.py
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")
        self.filepath = filepath
        self.items: List[InventoryItem] = []
        self.load()
    
    def load(self) -> None:
        """Load inventory from JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [InventoryItem.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading inventory: {e}")
                self.items = []
        else:
            self.items = []
    
    def save(self) -> None:
        """Save inventory to JSON file."""
        data = [item.to_dict() for item in self.items]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_all(self) -> List[InventoryItem]:
        """Get all items."""
        return self.items
    
    def get_by_category(self, category: str) -> List[InventoryItem]:
        """Get items filtered by category."""
        return [item for item in self.items if item.category == category]
    
    def get_by_id(self, item_id: str) -> Optional[InventoryItem]:
        """Get a single item by ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def add(self, item: InventoryItem) -> None:
        """Add a new item."""
        self.items.append(item)
        self.save()
    
    def update(self, item_id: str, updated_item: InventoryItem) -> bool:
        """Update an existing item."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items[i] = updated_item
                self.save()
                return True
        return False
    
    def delete(self, item_id: str) -> bool:
        """Delete an item by ID."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                self.save()
                return True
        return False
    
    def get_json_string(self) -> str:
        """Get inventory as JSON string for publishing."""
        data = [item.to_dict() for item in self.items]
        return json.dumps(data, indent=2, ensure_ascii=False)
