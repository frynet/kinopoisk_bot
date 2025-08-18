from sqlalchemy import select
from sqlalchemy.orm import Session

from database.dao.users import UserDao


class UserRepository:

    @classmethod
    def get_by_telegram_id(
            cls,
            session: Session,
            telegram_id: int,
    ) -> UserDao | None:
        stmt = select(UserDao).where(UserDao.telegram_id == telegram_id)

        return session.execute(stmt).scalar_one_or_none()

    @classmethod
    def create(
            cls,
            session: Session,
            tg_id: int,
            username: str | None,
            first_name: str | None,
            last_name: str | None,
    ) -> UserDao:
        user = UserDao(
            telegram_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
