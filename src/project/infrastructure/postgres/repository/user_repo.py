from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, true
from sqlalchemy.exc import IntegrityError, InterfaceError

from project.resource.jwt_token import create_access_token
from project.schemas.users import UserSchema, UserCreateUpdateSchema
from project.infrastructure.postgres.models import User
from project.resource.auth import verify_password

class UserRepository:
    _collection: Type[User] = User

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = select(true())

        try:
            return await session.scalar(query)
        except (Exception, InterfaceError):
            return False

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> UserSchema:
        query = (
            select(self._collection)
            .where(self._collection.email == email)
        )

        user = await session.scalar(query)

        if not user:
            raise Exception(f"User  с {email} не найден")

        return UserSchema.model_validate(obj=user)

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[UserSchema]:
        query = select(self._collection)

        users = await session.scalars(query)

        return [UserSchema.model_validate(obj=user) for user in users.all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> UserSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == user_id)
        )

        user = await session.scalar(query)

        if not user:
            raise Exception(f"User  с id {user_id} не найден")

        return UserSchema.model_validate(obj=user)

    async def create_user(
        self,
        session: AsyncSession,
        user: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            insert(self._collection)
            .values(user.model_dump())
            .returning(self._collection)
        )

        try:
            created_user = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise Exception(f"User  с email {user.email} уже существует")

        return UserSchema.model_validate(obj=created_user)

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        user: UserCreateUpdateSchema,
    ) -> UserSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == user_id)
            .values(user.model_dump())
            .returning(self._collection)
        )

        updated_user = await session.scalar(query)

        if not updated_user:
            raise Exception(f"User  с id {user_id} не найден")

        return UserSchema.model_validate(obj=updated_user)

    async def delete_user(
        self,
        session: AsyncSession,
        user_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == user_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise Exception(f"User  с id {user_id} не найден")

    async def login(
            self,
            session: AsyncSession,
            email: str,
            password: str,
    ) -> dict:
        user = await self.get_user_by_email(session=session, email=email)

        if not verify_password(password, user.password):
            raise Exception("Неверный пароль")

        token = create_access_token({"user_id": user.id, "is_admin": user.is_admin})

        return {"user": user, "access_token": token, "token_type": "bearer"}