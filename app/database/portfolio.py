from sqlalchemy import BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from datetime import datetime
from sqlalchemy import DateTime

engine = create_async_engine(url="sqlite+aiosqlite:///database.db",
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Audio_Portfolio(Base):
    __tablename__ = "audios"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # Увеличил длину для названий
    description: Mapped[str] = mapped_column(Text)  # Использую Text для длинных описаний
    file_id: Mapped[str] = mapped_column(String(256))  # Унифицированное название
    category_id: Mapped[int] = mapped_column(ForeignKey("audio_categories.id"))

class Photo(Base):
    __tablename__ = "photo"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    file_id: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)

class Video_Portfolio(Base):
    __tablename__ = "videos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    file_id: Mapped[str] = mapped_column(String(256))  # Исправлено: было audio, теперь file_id
    duration: Mapped[int] = mapped_column(BigInteger, nullable=True)  # Длительность в секундах
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=True)  # Размер файла

class Audio_Category(Base):
    __tablename__ = "audio_categories"  # Исправил опечатку
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    

    
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        