# Lead Handling Directive

> This directive defines the SOP for processing and managing incoming business leads for Cold Blooded Heartbeats.

## 📥 Inbound Flow
1. **Frontend Capture**: Leads are captured via the `lead-form` modal in the UI.
2. **Layer 2 Handoff**: `app.js` validates the input and prepares the payload.
3. **Layer 3 Execution**: `execution/lead_processor.py` stores the lead data.

## 🛠️ Processing Rules
- All leads MUST be stored in `.tmp/leads.json` for initial processing.
- A "NEW" status should be assigned to any fresh entry.
- Email addresses must be validated at the frontend layer before submission.

## 🏛️ Storage Schema
```json
{
    "timestamp": "ISO-8601 string",
    "name": "Full Name",
    "email": "validated email",
    "message": "request details",
    "status": "NEW | CONTACTED | CONVERTED | CLOSED"
}
```

## 🔄 Self-Annealing
- If `leads.json` becomes corrupted, the processor should initialize a new empty list.
- If storage fails due to permissions, log the entry to stdout for manual recovery.
