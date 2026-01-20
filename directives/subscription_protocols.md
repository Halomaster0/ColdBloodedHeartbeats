# SOP: Feeder Subscriptions (Subscribe & Save)

## Overview
Feeders (insects/rodents) are recurring revenue drivers. This system manages user-defined frequencies for automatic reordering.

## Subscription Logic
1. **Frequencies**: Weekly, Bi-Weekly, Monthly.
2. **Discount**: Fixed 10% discount applied to all subscription items.
3. **Management**: Users must be able to skip a week or cancel via the client dashboard (handled by `execution/subscription_engine.py`).

## Procedures
1. **Creation**: When a user selects "Subscribe & Save", a subscription record is created with a `NextShipDate`.
2. **Processing**: Every Tuesday, the `subscription_engine.py` runs to process all orders due for that week.
3. **Live Arrival**: Subscriptions for live insects are subject to the same Weather API checks as animal sales.

## Maintenance
- Automated emails are triggered 48 hours before shipment via `execution/subscription_engine.py --notify`.
