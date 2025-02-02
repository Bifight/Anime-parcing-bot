
from aiogram import Router, types, F
from  aiogram.filters import  CommandStart, Command
from aiogram.types import CallbackQuery

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(messege: types.Message):
    await rq.set_user_and_items(messege.from_user.id)
    await  messege.answer("Привет , я бот которй может облегчить поиск аниме", reply_markup=kb.main)


# @router.message(Command('help'))
# async def cmd_start(message: types.Message):
#     await  message.answer(text="Gig", reply_markup=kb.main)

@router.message(F.text == 'catalog')
async def cmd_catalog(message: types.Message):
    await  message.answer(text="Выберите день недели:", reply_markup= await kb.categories())

@router.callback_query(F.data.startswith('day_'))
async def category(callback: CallbackQuery):
    await callback.answer("Вы выбрали день")
    day = await kb.items(callback.data.split('_')[1])
    await callback.message.answer(f"Выберите anime:", reply_markup = day)

    

@router.callback_query(F.data.startswith('anime_'))
async def category_anime(callback: CallbackQuery):
    anime_data = await rq.get_item(callback.data.split('_')[1])
    episod0 = anime_data.episod.split(" ")
    favorite = await rq.examination_favorites(callback.from_user.id, anime_id = anime_data.id)
    await callback.answer("Вы выбрали anime")
    await callback.message.answer_photo(photo=anime_data.photo_path, 
                        caption=f"Название: {anime_data.name}\nCерия: {episod0[0]}\nДата: {anime_data.data}\nlink: {anime_data.href}\nИзбраное (True = есть, False = нету): {favorite}", 
                        reply_markup= await kb.item(anime_data.id))

@router.callback_query(F.data.startswith('to_main0')) 
async def category(callback: CallbackQuery):
    await callback.answer("Вы вернулись на главную страницу")
    await callback.message.answer("Вы вернулись на главную страницу", reply_markup= kb.main)

@router.callback_query(F.data.startswith('to_main1')) 
async def category(callback: CallbackQuery):
    await callback.answer("Вы вернулись на выбор дня")
    await callback.message.answer("Выберите день недели:", reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('to_main2')) 
async def category(callback: CallbackQuery):
    await callback.answer("Вы вернулись на выбор anime")
    day = await  kb.items(callback.data.split('2')[1])
    await callback.message.answer(f"Выберите anime:", reply_markup = day)

@router.callback_query(F.data.startswith('addfavorite_')) 
async def category(callback: CallbackQuery):
    await callback.answer("Вы добавили в избранное")
    anime = (callback.data.split('_')[1])
    await rq.add_favorite(callback.from_user.id, anime_id= anime)

@router.callback_query(F.data.startswith('deletefavorite_')) 
async def category(callback: CallbackQuery):
    await callback.answer("Вы удалили из избранного")
    anime = (callback.data.split('_')[1])
    await rq.remove_favorite(callback.from_user.id, anime_id = anime)



@router.callback_query(F.data.startswith('all_')) 
async def category(callback: CallbackQuery):
    await callback.answer("Вы выбрали все аниме дня")
    all_items = await rq.get_categorise_in_items(callback.data.split('_')[1])
    for item in all_items:
        episod0 = item.episod.split(" ")
        await callback.message.answer_photo(photo=item.photo_path, 
                        caption=f"Название: {item.name}\nCерия: {episod0[0]}\nДата: {item.data}\nlink: {item.href}")



@router.message(F.text == 'update')
async def cmd_favorites(message: types.Message):
    await rq.add_items_all_or_update(add_update = 1)
    await  message.answer(text="Обновлено", reply_markup=kb.main)


@router.message(F.text == 'favorite')
async def cmd_favorites(message: types.Message):
    await  message.answer(text=f"Избранное", reply_markup = await kb.favorite_user(message.from_user.id))
    
    # photo_url = "https://imgos.info/media/cache/thumbs_500x700/upload/anime/images/676281ef3e674631272550.jpg"
    # await  message.answer_photo(photo=photo_url, caption="Вот ваше изображение!")

# @router.message(F.photo)
# async  def get_photo(message: types.Message):
#     await message.answer(f"ID photo: {message.photo[-1].file_id}")
