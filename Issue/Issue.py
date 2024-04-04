from datetime import datetime
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