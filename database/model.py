from sqlalchemy import create_engine, Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    enabled = Column(Boolean, nullable=False, default=True) #Si el usuario de da de baja, se cambia el valor a False (0)
    actor = relationship("Actor", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"

class Actor(Base):
    __tablename__ = "actors"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True, nullable=True)
    uri = Column(String(255), unique=True, nullable=False)
    preferred_username = Column(String(50), nullable=False)
    inbox = Column(String(255), nullable=False)
    outbox = Column(String(255), nullable=False)
    public_key = Column(Text, nullable=False)
    private_key = Column(Text, nullable=True)
    is_local = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="actor")
    activities = relationship("Activity", back_populates="actor")

    def __repr__(self):
        return f"<Actor {self.uri}>"

class Activity(Base):
    __tablename__ = "activities"
    id = Column(BigInteger, primary_key=True, index=True)
    actor_id = Column(BigInteger, ForeignKey("actors.id"), nullable=False)
    type = Column(String(50), nullable=False)
    object_type = Column(String(50))
    object_url = Column(String(255))
    content = Column(Text)
    actor_uri = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

    actor = relationship("Actor", back_populates="activities")


    def __repr__(self):
        return f"<Activity {self.type}>"

class BlockedActor(Base):
    __tablename__ = "blocked_actors"
    id = Column(BigInteger, primary_key=True, index=True)
    uri = Column(String(255), unique=True, nullable=False)
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<BlockedActor {self.uri}>"
    
try:
    Base.metadata.create_all(bind=engine)
except:
        print("Error al crear las tablas")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()