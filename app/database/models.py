from sqlalchemy import BigInteger, String, ForeignKey, CacheKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine



engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

asyns_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id : Mapped[int] = mapped_column(primary_key=True)
    name_week : Mapped[str] = mapped_column(String(20))


class Item(Base):
    __tablename__ = "items"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name : Mapped[str] = mapped_column(String(250))
    episod : Mapped[int] = mapped_column(String(30))
    data : Mapped[str] = mapped_column(String(50))
    href : Mapped[str] = mapped_column(String(300))
    photo_path : Mapped[str] = mapped_column(String(300))
    category_id : Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category_day : Mapped[str] = mapped_column(String(30))

    favorited_by = relationship("Favorite", back_populates="item", cascade="all, delete-orphan")
    
class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # ID пользователя
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))  # ID аниме (или товара)

    user = relationship("User", back_populates="favorites")
    item = relationship("Item", back_populates="favorited_by")  

async def async_main():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)

