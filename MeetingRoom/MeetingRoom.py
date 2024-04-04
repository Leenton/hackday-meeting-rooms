import sqlite3

from Issue import Issue

class MeetingRoom():
    def __init__(self, id: int, name: str, floor_id: int):
        self.id = id
        self.name = name
        self.floor_id = floor_id

    def get_issues(resolved:bool, meeting_room_id:int) -> list[Issue]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        try:
            c.execute("SELECT issue_note, author_email, created_date, is_resolved, fresh_ticket_id meeting_room_id FROM issues WHERE is_resolved = $1 AND meeting_room_id = $2", (int(resolved) , meeting_room_id))
            issues = c.fetchall()
            conn.close()
            return [Issue(issue[0],issue[1],issue[2],issue[3],issue[4],issue[5]) for issue in issues]
        except:
            conn.close()
            raise Exception("Cannot find meeting room")
        
        
def get_meeting_room(meeting_room_id: int) -> MeetingRoom:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    try:
        c.execute("SELECT * FROM meeting_rooms WHERE meeting_room_id = ?", (meeting_room_id,))
        meeting_room = c.fetchone()
        conn.close()
        return MeetingRoom(id = meeting_room[0], name=meeting_room[1], floor_id=meeting_room[2])
    except:
        conn.close()
        raise Exception("Cannot find meeting room")