from datetime import datetime
import requests
import re
from os import getenv
from html import escape

VALID_EMAIL = re.compile("[a-zA-Z0-9]+.[a-zA-Z0-9]+@futurenet.com")
KEY = getenv("FRESH_API_KEY")

class Issue():
    def __init__(self, note: str, author_email: str, created_date: datetime, is_resolved: bool, fresh_ticket_id : int, meeting_room_id: int, id: int):
        self.note = note
        self.author_email = author_email
        self.created_date = created_date
        self.is_resolved = is_resolved
        self.fresh_ticket_id = fresh_ticket_id
        self.meeting_room_id = meeting_room_id
        self.id = id

def create_ticket(email, note, meeting_room_name) -> int | None:
    if re.match(VALID_EMAIL, email):
        request = requests.post(
            "https://futurenet.freshservice.com/api/v2/tickets",
            headers = 
            {"Content-Type": "application/json",
                "Authorization": KEY,
                "Accept": "application/json"},
            json=
                {"requester_id": 50004119550,
                "description": "Email: " +  email + ".\nNote: " + note,
                "subject": f"Meeting Room Ticket for {meeting_room_name}.", 
                "priority": 1, 
                "status": 2, 
                "group_id": 50000005179,
                "category": "Hotdesk/Meeting Room", 
                "sub_category": "Other"
                }
        )
        request = dict(request.json)
        if request.status_code == "201":
            return request["ticket"]["id"]
        else:
            return None
    else:
        # Return nothing to indicate the request was not made.
        return None