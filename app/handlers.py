from aiogram import Router, F, types
from aiogram.types import Message, Contact, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart, Command
import asyncio
import os
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
import app.keyboards as kb
from app.database.requests import get_audio, get_video, get_photo
import logging

from aiogram.types import ErrorEvent


router = Router()


@router.message(F.photo)
async def audio(message: Message):
    file_id = message.photo[-1].file_id
    await message.answer(file_id)


@router.callback_query(F.data == "main_menu")
@router.message(CommandStart())
async def cmd_start(event: Message | CallbackQuery):
    user_name = event.from_user.first_name

    if isinstance(event, Message):
            text = f"👋 Добро пожаловать, {user_name}!"
            await event.bot.send_chat_action(event.from_user.id, ChatAction.TYPING)
            await asyncio.sleep(0.3)
            await event.answer(text, reply_markup=kb.main)
    else:
        text = "🏠 Вы в главном меню"
        if (event.message.photo or event.message.audio 
            or event.message.video or event.message.document):
            await event.message.delete()
            await event.message.answer(text, reply_markup=kb.main)
        else:
            try:
                await event.message.edit_text(text, reply_markup=kb.main)
            except Exception as e:
                await event.message.delete()
                await event.message.answer(text, reply_markup=kb.main)
    await event.answer()


@router.callback_query(F.data == "calculate_cost")
async def calculate_cost(callback: CallbackQuery):
    await callback.answer("Выбор услуги")
    await callback.message.edit_text("Выбор услуги", reply_markup=kb.calculate_cost)

#AUDIO
@router.callback_query(F.data =="audio_ad")
async def audio_ad(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Название меню для рекламы аудио", reply_markup=kb.audio_ad)
    
@router.callback_query(F.data == "order_audio")
async def order_audio(callback: CallbackQuery):
    await callback.answer("Заказ аудио...")
    await callback.message.edit_text("Для того чтобы заказать обратитесь по контактной информации:\n\nНомер телефона:\nTG: ", 
                                     reply_markup=kb.back)
    
#VIDEO_VOICEOVER
@router.callback_query(F.data == "voicover")
async def voiceover_ad(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Название меню для рекламы озвучки видео", reply_markup=kb.video_ad)
    
@router.callback_query(F.data == "order_voiceover")
async def order_voiceover(callback: CallbackQuery):
    await callback.answer("Заказ озучки...")
    await callback.message.edit_text("Для того чтобы заказать обратитесь по контактной информации:\n\nНомер телефона:\nTG: ", 
                                     reply_markup=kb.back)
    

#IVR
@router.callback_query(F.data == "ivr")
async def voiceover_ad(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Название меню для рекламы ivr", reply_markup=kb.ivr_ad)
    
@router.callback_query(F.data == "order_ivr")
async def order_voiceover(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Для того чтобы заказать обратитесь по контактной информации:\n\nНомер телефона:\nTG: ", 
                                     reply_markup=kb.back)
    
#RECORDING SONG
@router.callback_query(F.data =="song")
async def audio_ad(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Название меню для рекламы песен", reply_markup=kb.record_song)

    
@router.callback_query(F.data == "order_record")
async def order_audio(callback: CallbackQuery):
    await callback.answer("Заказ аудио...")
    await callback.message.edit_text("Для того чтобы заказать обратитесь по контактной информации:\n\nНомер телефона:\nTG: ", 
                                     reply_markup=kb.back)
    
#Portfolio
@router.callback_query(F.data == "portfolio")
async def main_portfolio(callback: CallbackQuery):
    try:
        await callback.message.edit_text("Выберите пункт портфолио", reply_markup=kb.main_portfolio)
    except:
        await callback.message.delete()
        await callback.message.answer("Выберите пункт портфолио", reply_markup=kb.main_portfolio)
    await callback.answer()
    
#Аудио-портфолио
@router.callback_query(F.data == "audio_case")
async def category_audio(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите категорию голоса, которую хотите прослушать",
                                     reply_markup=await kb.categories())
    
@router.callback_query(F.data.startswith("category_"))
async def audio(callback: CallbackQuery):
    await callback.answer()
    category_id = callback.data.split("_")[1]
    try:
        await callback.message.edit_text("Выберите голос",
                                     reply_markup=await kb.audios(category_id))
    except:
        await callback.message.delete()
        await callback.message.answer("Выберите голос",
                                        reply_markup=await kb.audios(category_id))
    
@router.callback_query(F.data.startswith("audio_"))
async def audio_info(callback: CallbackQuery):
    await callback.answer()
    audio_id = callback.data.split("_")[1]
    audio = await get_audio(audio_id)

    if audio:
        await callback.message.delete()
        await callback.message.answer_audio(
            audio=audio.file_id,
            caption=f"{audio.name}\n\n{audio.description}",
            reply_markup=await kb.back_category(audio.category_id)
        )
    else:
        await callback.message.answer("Аудио не найдено")
        
#Видео-портфолио
@router.callback_query(F.data == "video_case")
async def video(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите видео",
                                     reply_markup= await kb.video())
    
@router.callback_query(F.data.startswith("video_"))
async def video_info(callback: CallbackQuery):
    await callback.answer()
    video_id = callback.data.split("_")[1]
    video = await get_video(video_id)
    
    await callback.message.delete()
    await callback.message.answer_video(video=video.file_id,
                                        caption=f"{video.name}\n\n{video.description}",
                                        reply_markup= await kb.back_to_portfolio())    
    

#ABOUT
@router.callback_query(F.data == "photo_about")
async def about(callback: CallbackQuery):
    await callback.answer()
    
    photo_id = 1
    photo = await get_photo(photo_id)
    
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo.file_id,
                                        caption=f"{photo.name}\n\n{photo.description}",
                                        reply_markup=kb.back)
    
    
