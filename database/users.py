from database import connection
from controllers import security

conn = connection.conn
cur = connection.conn.cursor()

def addUser(email: str, password: str) -> bool:
    sql = "insert into users (email, password_hash, created_at, enabled, admin) values (%s, %s, now(), 1, 0);"
    if cur.execute(sql, (email, security.hashPassword(password))):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False
    
def validUser(user: str, password: str) -> bool:
    sql = "select password_hash from users where email = %s;"
    if cur.execute(sql, (user)):
        hash = cur.fetchone()[0]
        if security.checkPassword(password, hash) == True:
            sql2 = "select * from users where email = %s and password_hash = %s and enabled = 1;"
            if cur.execute(sql2, (user, hash)):
                return True
    else:
        return False
    
def get_id(email: str) -> int:
    sql = "select id from users where email = %s;"
    if cur.execute(sql, email):
        return cur.fetchone()[0]
    else:
        return 0