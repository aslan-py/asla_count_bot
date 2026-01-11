from sqlalchemy import (Column, Date, ForeignKey, Integer, String,
                        create_engine, func)
from sqlalchemy.orm import declarative_base, relationship

from utils.constants import Models_SQL

Base = declarative_base()


class Logins(Base):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True)
    name = Column(String(Models_SQL.STR_LEN), nullable=False)
    expenses = relationship(
        'Expenses', cascade='all, delete-orphan', back_populates='owner')

    def __repr__(self):
        return self.name


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String(Models_SQL.STR_LEN), unique=True, nullable=False)
    expenses = relationship(
        'Expenses', cascade='all, delete-orphan', back_populates='category')

    def __repr__(self):
        return self.title


class Expenses(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    login_id = Column(Integer, ForeignKey('logins.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Integer)
    product = Column(String(Models_SQL.STR_PROd_LEN))
    create_at = Column(Date, server_default=func.current_date())
    owner = relationship('Logins', back_populates='expenses')
    category = relationship('Categories', back_populates='expenses')

    def __repr__(self):
        return f'Цена: {self.price}, Дата создания: {self.create_at}'


def database_setup():
    engine = create_engine(Models_SQL.DB_STAFF)
    Base.metadata.create_all(engine)
    return engine
