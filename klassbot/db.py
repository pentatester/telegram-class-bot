"""Helper class to get a database engine and to get a session."""
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from klassbot.config import config


db_conf = {
    "echo": True,
}
if config["database"]["postgres"]:
    db_conf["max_overflow"] = config["database"]["overflow_count"]
    db_conf["pool_size"] = config["database"]["connection_count"]
engine = create_engine(config["database"]["sql_uri"], **db_conf)
base = declarative_base(bind=engine)


def get_session(connection=None):
    """Get a new db session."""
    session = scoped_session(sessionmaker(bind=engine))
    return session


def get_one_or_create(
    session, model, create_method="", create_method_kwargs=None, **kwargs
):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, True
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), False
