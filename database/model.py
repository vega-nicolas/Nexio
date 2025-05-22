from sqlalchemy import create_engine, Column, BigInteger, String, Boolean, DateTime, ForeignKey, Index, CheckConstraint, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    enabled = Column(Boolean, nullable=False, default=True) #Si el usuario de da de baja, se cambia el valor a False (0)
    admin = Column(Boolean, nullable=False, default=False)
    actor = relationship("Actor", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"

class Actor(Base):
    __tablename__ = "actors"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True, nullable=True)
    uri = Column(String(255), unique=True, nullable=False, index=True)
    preferred_username = Column(String(30), nullable=False, index=True)
    display_name = Column(String(30), nullable=False)
    remote_node = Column(String(255), nullable=True, index=True)
    inbox = Column(String(255), nullable=False)
    outbox = Column(String(255), nullable=False)
    public_key = Column(String(2048), nullable=False)
    private_key = Column(String(2048), nullable=True)
    is_local = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="actor")
    activities = relationship("Activity", back_populates="actor")

    __table_args__ = (
        Index('ix_actors_uri_preferred_username', 'uri', 'preferred_username'),
    )

    def __repr__(self):
        return f"<Actor {self.uri}>"

class Activity(Base):
    __tablename__ = "activities"
    id = Column(BigInteger, primary_key=True, index=True)
    actor_id = Column(BigInteger, ForeignKey("actors.id"), nullable=False, index=True)
    type = Column(String(30), nullable=False)
    object_type = Column(String(30), nullable=True)
    object_url = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    actor = relationship("Actor", back_populates="activities")

    def __repr__(self):
        return f"<Activity {self.type}>"

class BlockedActor(Base):
    __tablename__ = "blocked_actors"
    id = Column(BigInteger, primary_key=True, index=True)
    uri = Column(String(255), unique=True, nullable=False, index=True)
    reason = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<BlockedActor {self.uri}>"
 
class Followers(Base):
    __tablename__ = "followers"
    id = Column(BigInteger, primary_key=True, index=True)
    follower_id = Column(BigInteger, ForeignKey("actors.id"), nullable=False)
    following_id = Column(BigInteger, ForeignKey("actors.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    __table_args__ = (
        CheckConstraint('follower_id <> following_id', name='check_followers_different'),
    )
    follower = relationship("Actor", foreign_keys=[follower_id])
    following = relationship("Actor", foreign_keys=[following_id])


class Post(Base):
    __tablename__ = 'post'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, index=True)
    text = Column(String(1000), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    likes = Column(BigInteger, nullable=False, default=0)
    comments = Column(BigInteger, nullable=False, default=0)
    shares = Column(BigInteger, nullable=False, default=0)
    
class PrivateMessage(Base):
    __tablename__ = 'private_messages'    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sender_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    recipient_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    content = Column(String(1000), nullable=False)
    activity_id = Column(String(255), unique=True, nullable=True, index=True)  # URI de la actividad (Create/Note)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    is_read = Column(Boolean, nullable=False, default=False)
    __table_args__ = (
        CheckConstraint('sender_id <> recipient_id', name='check_sender_recipient_different'),
    )

class Like(Base):
    __tablename__ = 'likes'    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    post_id = Column(BigInteger, ForeignKey('post.id'), nullable=False, index=True)
    activity_id = Column(String(255), unique=True, nullable=True, index=True)  # URI de la actividad Like
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    actor = relationship('Actor')
    post = relationship('Post')

class Share(Base):
    __tablename__ = 'shares'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    post_id = Column(BigInteger, ForeignKey('post.id'), nullable=False, index=True)
    activity_id = Column(String(255), unique=True, nullable=True, index=True)  # URI de la actividad Announce
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    actor = relationship('Actor')
    post = relationship('Post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    post_id = Column(BigInteger, ForeignKey('post.id'), nullable=False, index=True)
    content = Column(String(1000), nullable=False)
    activity_id = Column(String(255), unique=True, nullable=True, index=True)  # URI de la actividad Create/Note
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    actor = relationship('Actor')
    post = relationship('Post')

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)  # Actor que recibe la notificación
    source_actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)  # Actor que genera la notificación
    type = Column(String(30), nullable=False, index=True)  # Ejemplo: 'follow', 'like', 'comment', 'mention', 'message'
    target_id = Column(BigInteger, nullable=True, index=True)  # ID del objeto relacionado (post, comment, message)
    target_type = Column(String(30), nullable=True)  # Tipo de objeto ('post', 'comment', 'private_message')
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    actor = relationship('Actor', foreign_keys=[actor_id])
    source_actor = relationship('Actor', foreign_keys=[source_actor_id])    
    
class Mention(Base):
    __tablename__ = 'mentions'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)  # Actor mencionado
    source_id = Column(BigInteger, nullable=False, index=True)  # ID del objeto (post, comment, private_message)
    source_type = Column(String(30), nullable=False)  # Tipo de objeto ('post', 'comment', 'private_message')
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    actor = relationship('Actor')

class Media(Base):
    __tablename__ = 'media'    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    url = Column(String(255), nullable=False)  # URL del archivo en tu servidor o CDN
    mime_type = Column(String(50), nullable=False)  # Ejemplo: 'image/jpeg', 'video/mp4'
    description = Column(String(500), nullable=True)  # Descripción para accesibilidad
    source_id = Column(BigInteger, nullable=False, index=True)  # ID del objeto (post, comment, private_message)
    source_type = Column(String(30), nullable=False)  # Tipo de objeto
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    
    actor = relationship('Actor')

class InboxQueue(Base):
    __tablename__ = 'inbox_queue'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    activity_id = Column(String(255), unique=True, nullable=False, index=True)  # URI de la actividad
    activity_data = Column(Text, nullable=False)  # JSON de la actividad
    status = Column(String(20), nullable=False, default='pending')  # 'pending', 'processed', 'failed'
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    actor = relationship('Actor')

class OutboxQueue(Base):
    __tablename__ = 'outbox_queue'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    activity_id = Column(String(255), unique=True, nullable=False, index=True)  # URI de la actividad
    activity_data = Column(Text, nullable=False)  # JSON de la actividad
    recipient_inbox = Column(String(255), nullable=False)  # Inbox del destinatario
    status = Column(String(20), nullable=False, default='pending')  # 'pending', 'sent', 'failed'
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    actor = relationship('Actor')

class RemoteInstance(Base):
    __tablename__ = 'remote_instances'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    domain = Column(String(255), unique=True, nullable=False, index=True)  # Ejemplo: 'mastodon.social'
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

class ReadNotification(Base):
    __tablename__ = 'read_notifications'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger, ForeignKey('private_messages.id'), nullable=False, index=True)
    actor_id = Column(BigInteger, ForeignKey('actors.id'), nullable=False, index=True)
    activity_id = Column(String(255), unique=True, nullable=True, index=True)  # URI de la actividad ext:Read
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    message = relationship('PrivateMessage')
    actor = relationship('Actor')



def genTabs():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except SQLAlchemyError as e:
        print(f"Error when creating tables: {str(e)}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise
    finally:
        db.close()