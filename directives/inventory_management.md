# SOP: Unique Animal SKU Management

## Overview
Unlike dry goods, each live animal is a unique individual. This directive ensures that each animal is tracked with a unique ID and handled as a Single Stock Keeping Unit (SSKU).

## ID Format
`[SPECIES]-[YEAR]-[CLUTCH]-[INDIVIDUAL]`
Example: `BP-2026-05-01` (Ball Python, 2026, Clutch 5, Hatchling 1)

## Procedures
1. **Entry**: All new hatchlings must be added to the inventory via `execution/inventory_manager.py`.
2. **Sales**: When an animal is purchased, the script must mark the SKU as `SOLD` immediately.
3. **Double-Click Prevention**: The frontend logic (`app.js`) must disable the "Buy Now" button instantly upon local click event while the server processes.
4. **Genetic Tags**: Use consistent tags for morphs (e.g., `Piebald`, `Banana`, `Het-Clarinet`).

## Validation
- Run `python execution/inventory_manager.py --check-collisions` daily to ensure no duplicate IDs exist.
