from app.database.portfolio import Audio_Portfolio, Video_Portfolio, Audio_Category, Photo, async_session
from sqlalchemy import select, update

async def get_audio_categories():
    async with async_session() as session:
        return await session.scalars(select(Audio_Category))
    
    
async def get_audio_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Audio_Portfolio).where(Audio_Portfolio.category_id == category_id))

async def get_audio(audio_id):
    async with async_session() as session:
        result = await session.execute(select(Audio_Portfolio).where(Audio_Portfolio.id == audio_id))
        return result.scalar_one_or_none()
    
async def get_all_video():
    async with async_session() as session:
        result =  await session.execute(select(Video_Portfolio))    
        videos = result.scalars().all()
        return videos


async def get_video(video_id):
    async with async_session() as session:
        result = await session.execute(select(Video_Portfolio).where(Video_Portfolio.id == video_id))
        return result.scalar_one_or_none()
    
async def get_photo(photo_id):
    async with async_session() as session:
        result = await session.execute(select(Photo).where(Photo.id == photo_id))
    return result.scalar_one_or_none()