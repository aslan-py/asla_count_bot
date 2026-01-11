from datetime import datetime

from sqlalchemy import func

from utils.constants import Errors, Success
from utils.logger_config import logger
from utils.models import Categories, Expenses, Logins


def db_add_data(ai_data, Session, login):
    """Заполняем БД из списка словарей сформированного ИИ.

    Отдельно из объекта message получили login = user_name.
    """
    with Session() as session:
        try:
            owner = session.query(Logins).filter_by(name=login).first()
            if not owner:
                owner = Logins(name=login)
                session.add(owner)
                session.flush()

            for item in ai_data:
                category_title = item.get('category', 'прочее')
                category = session.query(Categories).filter_by(
                    title=category_title).first()

                if not category:
                    category = Categories(title=category_title)
                    session.add(category)
                    session.flush()

                new_expense = Expenses(
                    login_id=owner.id,
                    category_id=category.id,
                    price=item.get('price', 0),
                    product=item.get('product', 'неизвестно')
                )
                session.add(new_expense)
            session.commit()
            logger.success(Success.DB_DATA_OK)
        except Exception as error:
            session.rollback()
            logger.error(Errors.DB_DATA_NOT_OK.format(error))
            raise ValueError(Errors.DB_DATA_NOT_OK.format(error))


def dates_period_pivot(json_dates, Session, login):
    """Формируем  выгрузку из БД для составления отчета затрат."""
    with Session() as session:
        try:
            start = datetime.strptime(
                json_dates['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(json_dates['end_date'], '%Y-%m-%d').date()
            result_pivot = session.query(
                Categories.title,
                func.sum(Expenses.price)
            ).join(Logins).join(Categories).filter(
                Expenses.create_at.between(start, end),
                Logins.name == login
            ).group_by(
                Categories.title, Logins.name
            ).order_by(func.sum(Expenses.price).desc()).all()
            if result_pivot and result_pivot[0][0] is not None:
                logger.success(Success.DB_UPLOAD_OK)
                return result_pivot
            raise ValueError(Errors.NO_DB_DATA)
        except Exception as error:
            logger.error(Errors.DB_ERROR_FULY.format(error))
            raise RuntimeError(Errors.SYS_ERROR_DB.format(error))
