import json
import os
import sys

INVENTORY_FILE = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'inventory.json')

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return {"animals": [], "dry_goods": []}
    with open(INVENTORY_FILE, 'r') as f:
        return json.load(f)

def save_inventory(data):
    os.makedirs(os.path.dirname(INVENTORY_FILE), exist_ok=True)
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_animal(sku, species, morph, price):
    data = load_inventory()
    if any(item['sku'] == sku for item in data['animals']):
        print(f"Error: SKU {sku} already exists.")
        return False
    
    new_animal = {
        "sku": sku,
        "species": species,
        "morph": morph,
        "price": price,
        "status": "AVAILABLE",
        "last_meal": None
    }
    data['animals'].append(new_animal)
    save_inventory(data)
    print(f"Added {sku}: {species} ({morph})")
    return True

def mark_sold(sku):
    data = load_inventory()
    for animal in data['animals']:
        if animal['sku'] == sku:
            animal['status'] = "SOLD"
            save_inventory(data)
            print(f"SKU {sku} marked as SOLD.")
            return True
    print(f"Error: SKU {sku} not found.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inventory_manager.py [add|sell|list]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) == 6:
        add_animal(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]))
    elif cmd == "sell" and len(sys.argv) == 3:
        mark_sold(sys.argv[2])
    elif cmd == "list":
        inv = load_inventory()
        print(json.dumps(inv, indent=2))
