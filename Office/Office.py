import sqlite3

class Office():
    def __init__(self, name: str, id: int):
        self.name = name
        self.office_id = id

def get_offices() -> list[Office]:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        c.execute("SELECT name, office_id FROM offices")
        offices = c.fetchall()
        conn.close()

        return [Office(office[0], office[1]) for office in offices]
    except Exception as e:
        conn.close()
        print(e)
        raise Exception("Cannot find offices")

def get_office(office_id: str) -> Office:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    try:
        c.execute("SELECT * FROM offices WHERE office_id = $1", (office_id,))
        office = c.fetchone()
        print(office)
        conn.close()
        return Office(name = office[0], id=office[1])
    except:
        conn.close()
        raise Exception("Cannot find office")