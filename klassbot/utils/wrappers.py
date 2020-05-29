"""Wrappers"""

from functools import wraps
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import (
    BadRequest,
    Unauthorized,
    TimedOut,
    RetryAfter,
)
from klassbot.db import get_session
from klassbot.klassbot import logging
from klassbot.models import User

logger = logging.getLogger("Wrapper")


def private_wrapper(commit=True):
    def real_wrapper(func):
        """Wrapper for private, set `context.user_data` to `User` obj"""

        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            if not update.effective_chat.type == "private":
                raise Exception("Wrapper for private chat only!")
            result = None
            session = get_session()
            try:
                user, created = get_or_create_user(
                    update.effective_user, session=session
                )
                result = func(update, context, user)
                if commit or created:
                    session.commit()
            except Exception as e:
                if not ignore_exception(e):
                    logger.exception(e.msg)
            finally:
                session.close()
                return result

        return wrapper

    return real_wrapper


def group_command_wrapper(func):
    """Wrapper only for group"""

    @wraps(func)
    def wrapper(update: Update, context: CallbackContext):
        if not (
            update.effective_chat.type == "group"
            or update.effective_chat.type == "supergroup"
        ):
            raise Exception("Wrapper for group | supergroup chat only!")
        result = None
        return result

    return wrapper


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


def get_name_from_tg_user(tg_user):
    """Return the best possible name for a User."""
    name = ""
    if tg_user.first_name is not None:
        name = tg_user.first_name
        name += " "
    if tg_user.last_name is not None:
        name += tg_user.last_name

    if tg_user.username is not None and name == "":
        name = tg_user.username

    if name == "":
        name = str(tg_user.id)

    for character in ["[", "]", "_", "*"]:
        name = name.replace(character, "")

    return name.strip()


def get_or_create_user(user_, session):
    try:
        return session.query(User).filter_by(id=user_.id).one(), False
    except NoResultFound:
        user = User(
            id=user_.id,
            name=get_name_from_tg_user(user_),
            username=user_.username,
        )
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
