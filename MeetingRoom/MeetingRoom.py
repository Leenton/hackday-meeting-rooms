import sqlite3

class MeetingRoom():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.floor = None
     
    def get_floors() -> list[Floor]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT floor_name, floor_id FROM floors WHERE room_id = ?", (self.id,))
        floors = c.fetchall()
        conn.close()
        
        return [Floor(floor[0], floor[1]) for floor in floors]
    
    def get_Issues() -> list[Issue]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT issue_name, issue_id FROM issues WHERE room_id = ?", (self.id,))
        issues = c.fetchall()
        conn.close()
        
        return [Issue(issue[0], issue[1]) for issue in issues]
        