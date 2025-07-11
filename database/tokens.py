from database import connection
from controllers import security

conn = connection.conn
cur = connection.conn.cursor()

def addToken(user_id: int, token: str) -> bool:
    sql = "insert into tokens (user_id, token_hash) values (%s, %s);"
    if cur.execute(sql, (user_id, security.hash_token(token))):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False
    
def validToken(token: str) -> bool:
    sql = "select * from tokens where token_hash = %s;"
    if cur.execute(sql, (security.hash_token(token))):
        if cur.fetchone()[0]:
            return True
    else:
        return False
    
def getUserId(token: str) -> int:
    sql = "select user_id from tokens where token_hash = %s;"
    if cur.execute(sql, (security.hash_token(token))):
        id = cur.fetchone()[0]
        if id > 0:
            return id
    else:
        return False

def getActorId(token: str) -> int:
    sql = "SELECT actors.id FROM tokens JOIN users ON tokens.user_id = users.id JOIN actors ON users.id = actors.user_id WHERE tokens.token_hash = %s;"
    if cur.execute(sql, (security.hash_token(token))):
        id = cur.fetchone()[0]
        if id > 0:
            return id
    else:
        return False
