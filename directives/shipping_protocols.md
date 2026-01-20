# SOP: Live Animal Shipping Protocols

## Overview
Shipping live reptiles requires strict temperature controls to ensure animal safety. This directive defines the rules enforced by `execution/shipping_guard.py`.

## Temperature Thresholds
- **Safe Zone**: 40°F - 90°F (Day-of-delivery high).
- **Below 40°F**: FORCE "Hold for Pickup" at FedEx Hub.
- **Below 30°F**: DISABLE Shipping / Disable Checkout.
- **Above 90°F**: DISABLE Shipping / Disable Checkout.

## Shipping Schedule
- **Allowed Days**: Monday, Tuesday, Wednesday.
- **Goal**: Ensure the animal arrives by Thursday/Friday to avoid being stuck in a hub over the weekend.

## Procedures
1. **Cart Validation**: Before allowing checkout, the system calls `execution/shipping_guard.py --zip [ZIPCODE]`.
2. **Weather API**: The script fetches a 24-hour forecast for the destination.
3. **DOA Agreement**: A mandatory unboxing video requirement must be accepted by the user at checkout.

## Emergency Protocols
- If a delivery is delayed, the carrier must be contacted immediately to reroute to the nearest climate-controlled hub.
