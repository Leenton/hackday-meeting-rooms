import sqlite3

from Floor import Floor

class MeetingRoom():
    def __init__(self, id: int, name: str, floor: Floor):
        self.id = id
        self.name = name
        self.floor = floor
    
    def get_Issues() -> list[Issue]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT issue_name, issue_id FROM issues WHERE room_id = ?", (self.id,))
        issues = c.fetchall()
        conn.close()
        
        return [Issue(issue[0], issue[1]) for issue in issues]
        