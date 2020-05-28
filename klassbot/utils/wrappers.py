"""Wrappers"""

from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import (
    BadRequest,
    Unauthorized,
    TimedOut,
    RetryAfter,
)
from klassbot.db import get_session
from klassbot.logging import logging
from klassbot.models import User

logger = logging.getLogger("Wrapper")


def private_wrapper(func):
    """Wrapper for private, set `context.user_data` to `User` obj"""

    @wraps
    def wrapper(update: Update, context: CallbackContext):
        if not update.effective_chat.type == "private":
            raise Exception("Wrapper for private chat only!")
        result = None
        session = get_session()
        try:
            context.user_data = User.from_user(update.effective_user, session)
            result = func(update, context)
            session.commit()
            del context.user_data
        except Exception as e:
            if not ignore_exception(e):
                logger.exception(e.msg)
        finally:
            session.close()
            return result

    return wrapper


def group_command_wrapper(func):
    """Wrapper only for group"""

    @wraps
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
