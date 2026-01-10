import json
import os

VENDOR_DB = "database/vendors.json"


def get_vendors() -> list:
    """
    Returns the list of vendors from the database.
    Always returns a list (never crashes).
    """
    if not os.path.exists(VENDOR_DB):
        return []

    try:
        with open(VENDOR_DB, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
