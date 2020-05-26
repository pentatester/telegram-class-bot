from functools import wraps

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from klassbot.db import get_session


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


def session_wrapper(func):
    """
    `session` in kwargs,
    func should return `response`, `commit`
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        if "session" in kwargs.keys() and isinstance(
            kwargs["session"], Session
        ):
            response = func(*args, **kwargs)
        else:
            session = get_session()
            try:
                response, commit = func(*args, **kwargs, session=session)
                if commit:
                    session.commit()
            finally:
                session.close()
        if response is not None:
            return response

    return wrapper
