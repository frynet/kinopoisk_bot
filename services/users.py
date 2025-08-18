from telebot.types import User

from database.core.session import SessionLocal
from database.dao.users import UserDao
from database.repos.users import UserRepository


class UserService:

    @classmethod
    def get_or_create_user(cls, tg_user: User) -> UserDao:
        with SessionLocal() as session:
            user = UserRepository.get_by_telegram_id(session, tg_user.id)

            if not user:
                user = UserRepository.create(
                    session=session,
                    tg_id=tg_user.id,
                    username=tg_user.username,
                    first_name=tg_user.first_name,
                    last_name=tg_user.last_name,
                )

            return user


user_service = UserService()
