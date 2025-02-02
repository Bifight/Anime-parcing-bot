from app.database.models import asyns_session
from app.database.models import User,Category,Item, Favorite
from sqlalchemy import select, update

from app.database.parcing import Parsing


async def set_user_and_items(tg_id: int):
    async with asyns_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await add_category()
            await add_items_all_or_update()
            await session.commit()


async def update_item(name: str = None, episod: int = None, data: str = None, href: str = None, photo_path: str = None):
    async with asyns_session() as session:
        # Получаем объект из базы данных
        item = await session.scalar(select(Item).where(Item.name == name))
        
        if not item:
            print(f"Item с name {name} не найден.")
            return
        
        # Обновляем только переданные параметры
        if name:
            item.name = name
        if episod:
            item.episod = episod
        if data:
            item.data = data
        if href:
            item.href = href
        if photo_path:
            item.photo_path = photo_path
        
        await session.commit()
        #print(f"name {name} успешно обновлен!")

async def add_category():
    days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    async with asyns_session() as session:
        for ind, day in enumerate(days_of_week):
            category = Category(
                id = ind,
                name_week = day   
            )
            session.add(category)
            await session.commit()

async def add_items_all_or_update(add_update: int = 0, driver_path :  str = r"C:\working\Python\parcing\AnimeGo\app\database\chromedriver.exe", link : str ="https://animego.me/" ):
    
        parser = Parsing(driver_path)
        week = parser.load_main(link)
        for ind,day in enumerate(week):
            for anime in (week[day]):
                #id = anime[0]
                name = anime[1]
                episod = anime[2]
                data = anime[3]
                href = anime[4]
                photo_path = anime[5]
                if add_update == 0:
                    async with asyns_session() as session:
                        item =  await session.scalar(select(Item).where(Item.name == name))
                        if not item:
                            await add_item_to_category(name, episod, data, href, photo_path, category_id=ind, category_day = day)
                elif add_update == 1:
                    await update_item(name, episod, data, href, photo_path)


async def add_item_to_category(name: str, episod: int, data: str, href: str, photo_path: str, category_id: int, category_day: str):
    async with asyns_session() as session:
        # Проверяем, существует ли категория
        category = await session.scalar(select(Category).where(Category.id == category_id))
        
        if not category:
            print(f"Категория с ID {category_id} не найдена.")
            return
        
        # Создаём новый объект Item и связываем с категорией
        new_item = Item(
    
            name=name,
            episod=episod,
            data=data,
            href=href,
            photo_path=photo_path,
            category_id=category_id,
            category_day = category_day
        )
        
        session.add(new_item)
        await session.commit()


async def get_categories():
    async with asyns_session() as session:
        return await session.scalars(select(Category))
    

async def get_categorise_in_items(day_week: str):
    async with asyns_session() as session:
        return await session.scalars(select(Item).where(Item.category_day == day_week))
    

async def get_item(item_id):
    async with asyns_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))
    
async def search_item(anime_id):
    async with asyns_session() as session:
        return await session.scalar(select(Item).where(Item.id == anime_id))

async def add_favorite(user_id: int, anime_id: int):
    # Проверяем, есть ли уже в избранном
    async with asyns_session() as session:
        existing_favorite = await session.scalar(
            select(Favorite).where(Favorite.user_id == user_id, Favorite.item_id == anime_id)
        )
        
        if not existing_favorite:
            session.add(Favorite(user_id=user_id, item_id = anime_id))
            await session.commit()


async def remove_favorite(user_id: int, anime_id: int):
    async with asyns_session() as session:
        favorite = await session.scalar(
            select(Favorite).where(Favorite.user_id == user_id, Favorite.item_id == anime_id)
        )

        if favorite:
            await session.delete(favorite)
            await session.commit()
            
async def examination_favorites(user_id : int, anime_id : int):
    async with asyns_session() as session:
        favorite = await session.scalar(
            select(Favorite).where(Favorite.user_id == user_id, Favorite.item_id == anime_id)
        )
        if favorite:
            return True
        else:
            return False

async def get_favorites(user_id: int):
    async with asyns_session() as session:
        favorites = await session.scalars(
            select(Item).join(Favorite).where(Favorite.user_id == user_id)
        )
        return favorites.all()
    