from database import connection
from typing import List
from models.post import Post

conn = connection.conn
cur = connection.conn.cursor()

def addPost(actor_id: int, text: str) -> bool:
    sql = "insert into post (actor_id, text, likes, comments, shares) values (%s, %s, 0, 0, 0);"
    if cur.execute(sql, (actor_id, text)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False
    
def getAllPosts(page: int) -> List[Post]:
    sql = "SELECT post.id, post.actor_id, preferred_username, display_name, post.text, actors.uri, post.created_at, post.likes, post.comments, post.shares FROM post INNER JOIN actors ON post.actor_id = actors.id ORDER BY post.created_at DESC LIMIT %s, 10;"
    cur.execute(sql, (page))
    return cur.fetchall()

def deletePost(post_id: int, actor_id: int) -> bool:
    sql = "delete from post where id = %s and actor_id = %s;"
    if cur.execute(sql, (post_id, actor_id)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False
    
def editPost(edit: str, post_id: int, actor_id: int) -> bool:
    sql = "update post set text = %s where id = %s and actor_id = %s"
    if cur.execute(sql, (edit, post_id, actor_id)):
        conn.commit()
        return True
    else:
        conn.rollback()
        return False