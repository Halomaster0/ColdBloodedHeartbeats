import json
import os
from datetime import datetime, timedelta

SUBS_FILE = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'subscriptions.json')

def load_subscriptions():
    if not os.path.exists(SUBS_FILE):
        return []
    with open(SUBS_FILE, 'r') as f:
        return json.load(f)

def save_subscriptions(data):
    os.makedirs(os.path.dirname(SUBS_FILE), exist_ok=True)
    with open(SUBS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_subscription(user_id, item, frequency_weeks):
    subs = load_subscriptions()
    next_date = (datetime.now() + timedelta(weeks=frequency_weeks)).strftime('%Y-%m-%d')
    new_sub = {
        "sub_id": f"SUB-{len(subs)+1:04d}",
        "user_id": user_id,
        "item": item,
        "frequency_weeks": frequency_weeks,
        "next_ship_date": next_date,
        "status": "ACTIVE"
    }
    subs.append(new_sub)
    save_subscriptions(subs)
    print(f"Created subscription {new_sub['sub_id']} for {item}")
    return new_sub

if __name__ == "__main__":
    # Example usage: create a sub for 100 dubias every 2 weeks
    create_subscription("user_123", "100x Medium Dubia Roaches", 2)
