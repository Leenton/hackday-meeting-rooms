import sqlite3

from Floor import Floor
class Office():
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id
    
    def get_floors(self) -> list[Floor]:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()      
        try:
            c.execute("SELECT floor_id, meeting_room_floor_number FROM office_floors WHERE office_id = $1", (self.id,))
            office_floors = c.fetchall()
            return [Floor(id=office_floor[0], floor_num=office_floor[1], office_id=self.id) for office_floor in office_floors]
        except Exception as e:
            raise Exception("Cannot find floors")

def get_offices() -> list[Office]:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        c.execute("SELECT name, office_id FROM offices")
        offices = c.fetchall()
        conn.close()

        return [Office(office[0], office[1]) for office in offices]
    except Exception as e:
        raise Exception("Cannot find offices")

def get_office(office_id: int) -> Office:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    try:
        c.execute("SELECT name, office_id FROM offices WHERE office_id = $1", (office_id,))
        office = c.fetchone()
        print(office)
        conn.close()
        return Office(name = office[0], id=office[1])
    except:
        raise Exception("Cannot find office")