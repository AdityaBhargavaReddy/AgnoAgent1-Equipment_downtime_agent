import json
import os

TICKET_DB = "database/tickets.json"
VENDOR_DB = "database/vendors.json"


def _generate_ticket_id(tickets):
    if not tickets:
        return "TICKET-00001"
    last_id = tickets[-1]["ticket_id"]
    return f"TICKET-{int(last_id.split('-')[1]) + 1:05d}"


def _select_vendor(equipment_name: str, equipment_type: str) -> str:
    """
    Selects the best available vendor based on:
    1. equipment_name + equipment_type
    2. equipment_type only
    3. any active vendor (fallback)
    """
    if not os.path.exists(VENDOR_DB):
        return "UNASSIGNED"

    with open(VENDOR_DB, "r") as f:
        vendors = json.load(f)

    active_vendors = [v for v in vendors if v.get("active")]

    # 1️⃣ Exact match
    for v in active_vendors:
        caps = v.get("capabilities", {})
        if (
            equipment_name in caps.get("equipment_names", [])
            and equipment_type in caps.get("equipment_types", [])
        ):
            return v["vendor_id"]

    # 2️⃣ Type match
    for v in active_vendors:
        if equipment_type in v.get("capabilities", {}).get("equipment_types", []):
            return v["vendor_id"]

    # 3️⃣ Emergency fallback
    if active_vendors:
        return active_vendors[0]["vendor_id"]

    return "UNASSIGNED"


def store_ticket(
    is_gym_equipment: bool,
    equipment_name: str,
    equipment_type: str,
    urgency: str,
    status: str
) -> dict:
    os.makedirs("database", exist_ok=True)

    # Load existing tickets
    if os.path.exists(TICKET_DB):
        with open(TICKET_DB, "r") as f:
            tickets = json.load(f)
    else:
        tickets = []

    ticket_id = _generate_ticket_id(tickets)

    # ✅ Vendor assignment happens HERE (not in agent)
    vendor_id = _select_vendor(equipment_name, equipment_type)

    final_status = "Assigned" if vendor_id != "UNASSIGNED" else "Open"

    ticket = {
        "ticket_id": ticket_id,
        "is_gym_equipment": is_gym_equipment,
        "equipment_name": equipment_name,
        "equipment_type": equipment_type,
        "urgency": urgency,
        "status": final_status,
        "vendor_id": vendor_id
    }

    tickets.append(ticket)

    with open(TICKET_DB, "w") as f:
        json.dump(tickets, f, indent=2)

    return ticket
