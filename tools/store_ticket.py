import json
import os

TICKET_DB = "database/tickets.json"

def store_ticket(
    is_gym_equipment: bool,
    ticket_id: str,
    equipment_name: str,
    equipment_type: str,
    urgency: str,
    status: str
) -> str:
    os.makedirs("database", exist_ok=True)

    ticket = {
        "is_gym_equipment": is_gym_equipment,
        "ticket_id": ticket_id,
        "equipment_name": equipment_name,
        "equipment_type": equipment_type,
        "urgency": urgency,
        "status": status
    }

    if os.path.exists(TICKET_DB):
        with open(TICKET_DB, "r") as f:
            tickets = json.load(f)
    else:
        tickets = []

    tickets.append(ticket)

    with open(TICKET_DB, "w") as f:
        json.dump(tickets, f, indent=2)

    return "Ticket stored successfully"
