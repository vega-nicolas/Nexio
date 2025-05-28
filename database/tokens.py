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
    
def getUserId(token: str) -> str:
    sql = "select user_id from tokens where token_hash = %s;"
    if cur.execute(sql, (security.hash_token(token))):
        if cur.fetchone()[0]:
            return True
    else:
        return False
