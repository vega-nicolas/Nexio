from database import connection

conn = connection.conn
cur = connection.conn.cursor()

def addActor(user_id: int, uri: str, preferred_username: str, displayName: str, inbox: str, outbox:str, public_key: str, private_key: str) -> bool:
    sql = "insert into actors (user_id, uri, preferred_username, display_name, inbox, outbox, public_key, private_key, is_local, created_at) values (%s, %s, %s, %s, %s, %s, %s, %s, 1, now());"
    if cur.execute(sql, (user_id, uri, preferred_username, displayName, inbox, outbox, public_key, private_key)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False
    
def addExternalActor(uri: str, preferred_username: str, displayName: str, inbox: str, outbox:str, public_key: str) -> bool:
    sql = "insert into actors (uri, preferred_username, display_name inbox, outbox, public_key, is_local, created_at) values (%s, %s, %s, %s, %s, %s, 0, now());"
    if cur.execute(sql, (uri, preferred_username, displayName, inbox, outbox, public_key)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False