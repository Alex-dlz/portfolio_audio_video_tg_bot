from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_audio_categories, get_audio_by_category, get_all_video

main = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Заказать", callback_data="calculate_cost")],
   [InlineKeyboardButton(text="Портфолио", callback_data="portfolio")],
   [InlineKeyboardButton(text="О нас", callback_data="photo_about")]
])

calculate_cost = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Аудиореклама", callback_data="audio_ad")],
    [InlineKeyboardButton(text="Озвучка видео", callback_data="voicover")],
    [InlineKeyboardButton(text="IVR Система", callback_data="ivr")],
    [InlineKeyboardButton(text="Запись песен", callback_data="song")],
    [InlineKeyboardButton(text="Своя задача", callback_data="my_project")],
    [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
])

#AUDIO_AD
audio_ad = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text="Заказать аудио", callback_data="order_audio")],
  [InlineKeyboardButton(text="Назад", callback_data="calculate_cost")]
])

#VIDEO_VOICEOVER
video_ad = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text="Заказать озвучку видео", callback_data="order_voiceover")],
  [InlineKeyboardButton(text="Назад", callback_data="calculate_cost")]
])


#IVR
ivr_ad = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text="Заказать ivr", callback_data="order_ivr")],
  [InlineKeyboardButton(text="Назад", callback_data="calculate_cost")]
])

#RECORDING SONG
record_song = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text="Заказать аудио", callback_data="order_record")],
  [InlineKeyboardButton(text="Назад", callback_data="calculate_cost")]
])

#MAIN PORTFOLIO
main_portfolio = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео кейсы", callback_data="video_case")],
    [InlineKeyboardButton(text="Аудио кейсы", callback_data="audio_case")],
    [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
])

  
back_cont = InlineKeyboardMarkup(inline_keyboard=[
  [InlineKeyboardButton(text="Назад", callback_data="portfolio")]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Главное меню/Назад", callback_data="main_menu")]
    ]
)

async def categories():
  keyboard = InlineKeyboardBuilder()
  all_categories = await get_audio_categories()
  for category in all_categories:
    keyboard.row(InlineKeyboardButton(text=category.name,
                                      callback_data=f"category_{category.id}"))
  keyboard.row(InlineKeyboardButton(text="Назад",
                                      callback_data="portfolio"))
  return keyboard.as_markup()

async def audios(category_id):
  keyboard = InlineKeyboardBuilder()
  all_audios = await get_audio_by_category(category_id) 
  for audio in all_audios:
    keyboard.row(InlineKeyboardButton(text=f"{audio.name}",
                                      callback_data=f"audio_{audio.id}"))
  keyboard.row(InlineKeyboardButton(text="Назад",
                                    callback_data="audio_case"))
  return keyboard.as_markup( )

async def back_category(category_id):
  return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data=f"category_{category_id}")]
  ])

async def video():
  keyboard = InlineKeyboardBuilder()
  all_videos = await get_all_video() 
  for video in all_videos:
    keyboard.row(InlineKeyboardButton(text=f"{video.name}",
                                      callback_data=f"video_{video.id}"))
  keyboard.row(InlineKeyboardButton(text="Назад",
                                    callback_data="portfolio"))
  return keyboard.as_markup()

async def back_to_portfolio():
  return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="portfolio")]
  ])