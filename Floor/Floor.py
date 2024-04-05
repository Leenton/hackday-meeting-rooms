import sqlite3
from MeetingRoom import MeetingRoom
from Issue import Issue

class Floor():
    def __init__(self, id: int, floor_num: int, office_id: int):
        self.id = id
        self.floor_num = floor_num
        self.office_id = office_id
    
    def get_meeting_rooms(self) -> list[MeetingRoom]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        
        try:
            c.execute("SELECT meeting_room_id, meeting_room_name FROM meeting_rooms WHERE floor_id = ?", (self.id,))
            issues = c.fetchall()
            conn.close()

            return [MeetingRoom(id=issue[0], name=issue[1], floor_id=self.id) for issue in issues]
        except Exception as e:
            raise Exception("Cannot find meeting rooms")
    

def get_floor(floor_id: str) -> Floor:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    try:
        c.execute("SELECT floor_id, meeting_room_floor_number, office_id FROM office_floors WHERE floor_id = ?", (floor_id,))
        floor = c.fetchone()
        conn.close()
        return Floor(id=floor[0], floor_num=floor[1], office_id=floor[2])
    except:
        conn.close()
        raise Exception("Cannot find floor")