from datetime import datetime
import requests
import re
from os import getenv

VALID_EMAIL = re.compile("[a-zA-Z]+.[a-zA-Z]+@futurenet.com")
KEY = getenv("FRESH_API_KEY")

class Issue():
    def __init__(self, note: str, author_email: str, created_date: datetime, is_resolved: bool, fresh_ticket_id : int, id: int):
        self.note = note
        self.author_email = author_email
        self.created_date = created_date
        self.is_resolved = is_resolved
        self.fresh_ticket_id = fresh_ticket_id
        self.id = id

    def __str__(self):
        return f"{self.name} ({self.id})"
    
def create_ticket(email, note, meeting_room_id):
    if re.match(VALID_EMAIL, email):
        request = requests.post(
            "https://futurenet.freshservice.com/api/v2/tickets",
            headers = 
            {"Content-Type": "application/json",
                "Authorization": KEY,
                "Accept": "application/json"},
            json=
                {"requester_id": 50004119550,
                "description": f"Email: {email}\nNote: {note}",
                "subject": f"Meeting Room Ticket for {meeting_room_id}.", 
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

