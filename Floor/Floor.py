import sqlite3
from MeetingRoom import MeetingRoom
from Issue import Issue

class Floor():
    def __init__(self, id: int, floor_num: int):
        self.id = id
        self.floor_num = floor_num
    
    def get_meeting_room(self) -> list[MeetingRoom]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT issue_name, issue_id FROM issues WHERE room_id = ?", (self.id,))
        issues = c.fetchall()
        conn.close()
        
        return [Issue(issue[0], issue[1]) for issue in issues]

def get_floors(office_id) -> list[Floor]:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()      
    try:
        c.execute("SELECT meeting_room_floor_number FROM office_floors WHERE office_id = $1", (office_id,))
        office_floors = c.fetchall()
        conn.close()
        return [Floor(office_floor[0], office_floor[1]) for office_floor in office_floors]

    except:
        conn.close()
        raise Exception("Cannot find floors")
    

def get_floor(floor_id: str) -> Floor:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    try:
        c.execute("SELECT * FROM office_floors WHERE floor_id = ?", (floor_id,))
        floor = c.fetchone()
        conn.close()
        return Floor(id = floor[0], floor_num=floor[1])
    except:
        conn.close()
        raise Exception("Cannot find floor")