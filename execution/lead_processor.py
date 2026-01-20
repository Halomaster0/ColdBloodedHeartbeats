import json
import os
import sys
from datetime import datetime

LEADS_FILE = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'leads.json')

def process_lead(name, email, message):
    """
    Processes a lead by saving it to a local JSON file.
    In a real scenario, this might trigger an email or API call.
    """
    data = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    new_lead = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "message": message,
        "status": "NEW"
    }
    
    data.append(new_lead)
    
    os.makedirs(os.path.dirname(LEADS_FILE), exist_ok=True)
    with open(LEADS_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Lead processed for: {name} ({email})")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python lead_processor.py [name] [email] [message]")
        sys.exit(1)
    
    process_lead(sys.argv[1], sys.argv[2], sys.argv[3])
