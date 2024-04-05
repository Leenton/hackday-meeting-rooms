CREATE TABLE IF NOT EXISTS offices (
    office_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS office_floors (
    floor_id INTEGER PRIMARY KEY,
    office_id INTEGER,
		meeting_room_floor_number INTEGER,
    FOREIGN KEY (office_id) REFERENCES offices(office_id)
);      
CREATE TABLE IF NOT EXISTS meeting_rooms (
    meeting_room_id INTEGER PRIMARY KEY NOT NULL,
    floor_id INTEGER,
    meeting_room_name TEXT,
  	FOREIGN KEY (floor_id) REFERENCES office_floors(floor_id)
);

CREATE TABLE IF NOT EXISTS issues (
    issue_id INTEGER PRIMARY KEY,
    meeting_room_id INTEGER KEY,
    author_email TEXT NOT NULL,
    issue_note TEXT,
    -- Store date as UNIX timestamp
    created_date INTEGER,
    is_resolved INTEGER,
    fresh_ticket_id INTEGER,
  	FOREIGN KEY (meeting_room_id) REFERENCES meeting_rooms(meeting_room_id)
);
