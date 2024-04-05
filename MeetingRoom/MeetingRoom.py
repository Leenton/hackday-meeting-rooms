import sqlite3
from datetime import datetime
from Issue import Issue

class MeetingRoom():
    def __init__(self, id: int, name: str, floor_id: int):
        self.id = id
        self.name = name
        self.floor_id = floor_id

    def get_issues(self, resolved:bool) -> list[Issue]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        try:
            c.execute("SELECT issue_note, author_email, created_date, is_resolved, fresh_ticket_id, meeting_room_id, issue_id FROM issues WHERE is_resolved = $1 AND meeting_room_id = $2", (int(resolved) , self.id))
            issues = c.fetchall()
            conn.close()
            return [
                Issue(
                    note=issue[0],
                    author_email=issue[1],
                    created_date=datetime.fromtimestamp(issue[2]),
                    is_resolved=issue[3],
                    fresh_ticket_id=issue[4],
                    meeting_room_id=issue[5],
                    id=issue[6]
                ) for issue in issues
            ]
        except Exception as e:
            raise Exception("Cannot find issues for room")
        
def get_meeting_room(meeting_room_id: int) -> MeetingRoom:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    try:
        c.execute("SELECT meeting_room_id, meeting_room_name, floor_id FROM meeting_rooms WHERE meeting_room_id = ?", (meeting_room_id,))
        meeting_room = c.fetchone()
        conn.close()
        return MeetingRoom(id=meeting_room[0], name=meeting_room[1], floor_id=meeting_room[2])
    except:
        raise Exception("Cannot find meeting room")