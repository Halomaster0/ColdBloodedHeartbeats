import sys
import argparse
import random # Mocking API for now

# Thresholds
SAFE_MIN = 40
SAFE_MAX = 90
HARD_MIN = 30

def get_mock_temp(zip_code):
    # In a real app, this would call OpenWeatherMap or similar
    # Mocking different temps based on zip patterns
    if zip_code.startswith('9'): return 75 # California
    if zip_code.startswith('0'): return 25 # Northeast (Winter)
    if zip_code.startswith('3'): return 95 # Florida
    return 65

def check_shipping_safety(zip_code):
    temp = get_mock_temp(zip_code)
    print(f"Checking shipping safety for Zip: {zip_code} (Temp: {temp}F)")
    
    if temp < HARD_MIN or temp > SAFE_MAX:
        return "DENIED", f"Temperature ({temp}F) is unsafe for live animal transport."
    elif temp < SAFE_MIN:
        return "RESTRICTED", f"Temperature ({temp}F) requires 'Hold for Pickup' at FedEx Hub."
    else:
        return "SAFE", "Conditions are optimal for shipping."

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, help="Destination Zip Code")
    args = parser.parse_args()
    
    status, msg = check_shipping_safety(args.zip)
    print(f"Status: {status}\nMessage: {msg}")
    
    if status == "DENIED":
        sys.exit(1)
    sys.exit(0)
