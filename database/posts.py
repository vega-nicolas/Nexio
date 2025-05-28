from database import connection
from typing import List
from models.post import Post

conn = connection.conn
cur = connection.conn.cursor()

def addPost(user_id: int, text: str) -> bool:
    sql = "insert into post (user_id, text, likes, comments, shares) values (%s, %s, 0, 0, 0);"
    if cur.execute(sql, (user_id, text)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False
    
def getAllPosts(page: int) -> List[Post]:
    sql = "SELECT post.id, post.user_id, preferred_username, display_name, post.text, actors.uri, post.created_at, post.likes, post.comments, post.shares FROM post INNER JOIN actors ON post.user_id = actors.id   ORDER BY  post.created_at ASC  LIMIT %s, 10;"
    cur.execute(sql, (page))
    return cur.fetchall()

def deletePost(post_id: int, user_id: int) -> bool:
    sql = "delete from post where id = %s and user_id = %s;"
    if cur.execute(sql, (post_id, user_id)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False
    
def editPost(edit: str, post_id: int, user_id: int) -> bool:
    sql = "update post set text = %s where id = %s and user_id = %s"
    if cur.execute(sql, (edit, post_id, user_id)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False