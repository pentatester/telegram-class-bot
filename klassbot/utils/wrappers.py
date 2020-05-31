"""Wrappers"""

from functools import wraps
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
from klassbot.models import User, Klass, UserKlass

logger = logging.getLogger("Wrapper")


def message_wrapper(commit=True, klass_=True, session=False):
    def real_wrapper(func):
        """Wrapper for message, set `context.user_data` to `User` obj"""

        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            result = None
            session = get_session()
            try:
                user, _ = User.get_or_create(
                    update.effective_user, session=session
                )
                args = [update, context]
                kwargs = dict()
                if klass_ and is_group(update.effective_chat):
                    klass, _ = Klass.get_or_create(update, session=session)
                    user_klass, _ = UserKlass.get_or_create(
                        user, klass, session
                    )
                    args.append(user_klass)
                    args.append(klass)
                else:
                    args.append(user)
                if session:
                    kwargs["session"] = session
                result = func(*args, **kwargs)
                if commit:
                    session.commit()
            except Exception as e:
                if not ignore_exception(e):
                    logger.exception(e.msg)
            finally:
                session.close()
                return result

        return wrapper

    return real_wrapper


def private_command_wrapper(commit=True, session=False):
    def real_wrapper(func):
        """Wrapper for message, set `context.user_data` to `User` obj"""

        @wraps(func)
        def wrapper(update: Update, context: CallbackContext):
            result = None
            session = get_session()
            try:
                user, _ = User.get_or_create(
                    update.effective_user, session=session
                )
                kwargs = dict()
                if session:
                    kwargs["session"] = session
                result = func(update, context, user, **kwargs)
                if commit:
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
                klass, _ = Klass.get_or_create(update.effective_chat, session)
                if klass.started:
                    user, _ = User.get_or_create(update.effective_user, session)
                    user_klass, created = UserKlass.get_or_create(
                        user, klass, session
                    )
                    result = func(update, context, user=user, klass=klass)
                else:
                    result = func(update, context, klass=klass)
                if commit:
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


def is_group(chat: Chat):
    return chat.type == Chat.GROUP or chat.type == Chat.SUPERGROUP
