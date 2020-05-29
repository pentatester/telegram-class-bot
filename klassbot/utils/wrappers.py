"""Wrappers"""

from functools import wraps
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from telegram import Update, Chat
from telegram.ext import CallbackContext
from telegram.error import (
    BadRequest,
    Unauthorized,
    TimedOut,
    RetryAfter,
)
from klassbot.db import get_session
from klassbot.klassbot import logging
from klassbot.models import User, Klass

logger = logging.getLogger("Wrapper")


def message_wrapper(commit=True, klass_=False):
    def real_wrapper(func):
        """Wrapper for message, set `context.user_data` to `User` obj"""

        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            result = None
            session = get_session()
            try:
                user, created_user = get_or_create_user(
                    update.effective_user, session=session
                )
                if klass_ and update.effective_chat.type == "group":
                    klass, created_klass = get_or_create_klass(
                        update.effective_chat, session=session
                    )
                    user_klass = klass.add_user(user, session=session)
                    result = func(update, context, user_klass, klass)
                    if commit or created_user or created_klass:
                        session.commit()
                else:
                    result = func(update, context, user)
                    if commit or created_user:
                        session.commit()
            except Exception as e:
                if not ignore_exception(e):
                    logger.exception(e.msg)
            finally:
                session.close()
                return result

        return wrapper

    return real_wrapper


def klass_command_wrapper(commit=True):
    """Wrapper only for klass"""

    def real_wrapper(func):
        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            if not (update.effective_chat.type == "group"):
                return
            result = None
            session = get_session()
            try:
                klass, created_klass = get_or_create_klass(
                    update.effective_chat, session
                )
                user, created_user = get_or_create_user(
                    update.effective_user, session
                )
                result = func(update, context, klass, user)
                if commit or created_klass or created_user:
                    session.commit()
            except Exception as e:
                if not ignore_exception(e):
                    logger.exception(e.msg)
            finally:
                session.close()
                return result

        return wrapper

    return real_wrapper


def ignore_exception(exception):
    """Check whether we can safely ignore this exception."""
    if isinstance(exception, BadRequest):
        if (
            exception.message.startswith("Query is too old")
            or exception.message.startswith("Have no rights to send a message")
            or exception.message.startswith("Message_id_invalid")
            or exception.message.startswith("Message identifier not specified")
            or exception.message.startswith("Schedule_date_invalid")
            or exception.message.startswith("Message to edit not found")
            or exception.message.startswith(
                "Message is not modified: specified new message content"
            )
        ):
            return True

    if isinstance(exception, Unauthorized):
        if (
            exception.message.lower()
            == "forbidden: bot was blocked by the user"
        ):
            return True
        if exception.message.lower() == "forbidden: message_author_required":
            return True
        if (
            exception.message.lower()
            == "forbidden: bot is not a member of the supergroup chat"
        ):
            return True
        if exception.message.lower() == "forbidden: user is deactivated":
            return True
        if (
            exception.message.lower()
            == "forbidden: bot was kicked from the group chat"
        ):
            return True
        if (
            exception.message.lower()
            == "forbidden: bot was kicked from the supergroup chat"
        ):
            return True
        if exception.message.lower() == "forbidden: chat_write_forbidden":
            return True

    if isinstance(exception, TimedOut):
        return True

    if isinstance(exception, RetryAfter):
        return True

    return False


def get_or_create_klass(chat: Chat, session):
    try:
        return session.query(Klass).filter_by(id=chat.id).one(), False
    except NoResultFound:
        klass = Klass.from_chat(chat)
        try:
            session.add(klass)
            session.flush()
            return klass, True
        except IntegrityError:
            session.rollback()
            return (
                session.query(Klass).filter_by(id=chat.id).one(),
                False,
            )


def get_or_create_user(user_, session):
    try:
        return session.query(User).filter_by(id=user_.id).one(), False
    except NoResultFound:
        user = User.from_user(user_)
        try:
            session.add(user)
            session.flush()
            return user, True
        except IntegrityError:
            session.rollback()
            return (
                session.query(User).filter_by(id=user_.id).one(),
                False,
            )
