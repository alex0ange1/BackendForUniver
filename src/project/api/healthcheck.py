from fastapi import APIRouter, status

from project.api.depends import database, user_repo
from project.schemas.healthcheck import HealthCheckSchema


class DatabaseError(Exception):
	"""
    Исключение для ошибок, связанных с базой данных.
    """
	_ERROR_MESSAGE_TEMPLATE: str = "Произошла ошибка в базе данных: {message}"

	def __init__(self, message: str) -> None:
		"""
        Инициализирует исключение с сообщением об ошибке.
        """
		self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
		super().__init__(self.message)


healthcheck_router = APIRouter()


@healthcheck_router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
	try:
		async with database.session() as session:
			db_is_ok = await user_repo.check_connection(session=session)
			if not db_is_ok:
				raise DatabaseError(message="Не удалось подключиться к базе данных")
	except DatabaseError as error:
		db_is_ok = False
		print(error)
	except Exception as error:
		db_is_ok = False
		raise DatabaseError(message=f"Непредвиденная ошибка: {error}")

	return HealthCheckSchema(database_status="OK" if db_is_ok else "FAIL")
