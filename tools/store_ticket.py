import json
import os
from tools.email_user import email_user

TICKET_DB = "database/tickets.json"
VENDOR_DB = "database/vendors.json"


def _generate_ticket_id(tickets):
    if not tickets:
        return "TICKET-00001"
    last_id = tickets[-1]["ticket_id"]
    return f"TICKET-{int(last_id.split('-')[1]) + 1:05d}"


def _load_json_safe(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _select_vendor(equipment_type: str):
    vendors = _load_json_safe(VENDOR_DB)
    active_vendors = [v for v in vendors if v.get("active")]

    for v in active_vendors:
        if equipment_type in v.get("capabilities", {}).get("equipment_types", []):
            return v

    return None


def store_ticket(
    is_gym_equipment: bool,
    equipment_name: str,
    equipment_type: str,
    urgency: str,
    status: str
) -> dict:
    os.makedirs("database", exist_ok=True)

    tickets = _load_json_safe(TICKET_DB)
    ticket_id = _generate_ticket_id(tickets)

    vendor = _select_vendor(equipment_type)

    final_status = "Assigned" if vendor else "Open"

    ticket = {
        "ticket_id": ticket_id,
        "is_gym_equipment": is_gym_equipment,
        "equipment_name": equipment_name,
        "equipment_type": equipment_type,
        "urgency": urgency,
        "status": final_status,
        "vendor_id": vendor["vendor_id"] if vendor else None,
        "vendor_email": vendor["email"] if vendor else None,
        "vendor_name": vendor["vendor_name"] if vendor else None
    }

    tickets.append(ticket)

    with open(TICKET_DB, "w") as f:
        json.dump(tickets, f, indent=2)

    # ✅ EMAIL SENT HERE (DETERMINISTIC, SAFE)
    if final_status == "Assigned":
        email_user(
            to_email=vendor["email"],
            subject="New Gym Equipment Ticket Assigned",
            body=(
                f"Ticket ID: {ticket_id}\n"
                f"Equipment: {equipment_name}\n"
                f"Type: {equipment_type}\n"
                f"Urgency: {urgency}"
            )
        )

    return {
        "ticket_id": ticket_id,
        "status": final_status,
        "vendor_email": ticket["vendor_email"],
        "vendor_name": ticket["vendor_name"]
    }
