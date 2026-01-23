"""
Data Models for Cold Blooded Heartbeats Inventory
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class FeedingEntry:
    """Single feeding log entry."""
    date: str
    food_type: str


@dataclass
class InventoryItem:
    """Base inventory item - works for all categories."""
    id: str
    category: str  # animals, pantry, habitats, den
    name: str
    variant: str  # morph for animals, flavor for pantry, etc.
    price: float
    quantity: int
    image: str  # relative path to image
    status: str = "available"  # available, sold, reserved
    
    # Animals-specific (optional)
    verified_feeder: bool = False
    feeding_log: List[FeedingEntry] = field(default_factory=list)
    
    @classmethod
    def generate_id(cls, category: str) -> str:
        """Generate a unique SKU-style ID."""
        prefix_map = {
            "animals": "AN",
            "pantry": "PT",
            "habitats": "HB",
            "den": "DN"
        }
        prefix = prefix_map.get(category, "XX")
        date_str = datetime.now().strftime("%Y-%m-%d")
        short_uuid = uuid.uuid4().hex[:4].upper()
        return f"{prefix}-{date_str}-{short_uuid}"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "variant": self.variant,
            "price": self.price,
            "quantity": self.quantity,
            "image": self.image,
            "status": self.status,
        }
        
        # Only include animals-specific fields for animals
        if self.category == "animals":
            data["verified_feeder"] = self.verified_feeder
            data["feeding_log"] = [
                {"date": f.date, "food_type": f.food_type}
                for f in self.feeding_log
            ]
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "InventoryItem":
        """Create from dictionary."""
        feeding_log = []
        if "feeding_log" in data:
            feeding_log = [
                FeedingEntry(date=f["date"], food_type=f["food_type"])
                for f in data.get("feeding_log", [])
            ]
        
        return cls(
            id=data["id"],
            category=data["category"],
            name=data["name"],
            variant=data.get("variant", ""),
            price=data.get("price", 0.0),
            quantity=data.get("quantity", 0),
            image=data.get("image", ""),
            status=data.get("status", "available"),
            verified_feeder=data.get("verified_feeder", False),
            feeding_log=feeding_log
        )


# Category definitions for UI
CATEGORIES = [
    {"id": "animals", "label": "Live Animals", "icon": "🐍"},
    {"id": "pantry", "label": "The Pantry", "icon": "🍽️"},
    {"id": "habitats", "label": "Habitats", "icon": "🏠"},
    {"id": "den", "label": "The Den", "icon": "🎨"},
]
