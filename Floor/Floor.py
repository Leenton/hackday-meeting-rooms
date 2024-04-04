import sqlite3
from MeetingRoom import MeetingRoom

class Floor():
    def __init__(self, id: int, floor_num: int):
        self.id = id
        self.floor_num = floor_num
    
    def get_meeting_room() -> list[MeetingRoom]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT issue_name, issue_id FROM issues WHERE room_id = ?", (self.id,))
        issues = c.fetchall()
        conn.close()
        
        return [Issue(issue[0], issue[1]) for issue in issues]
        