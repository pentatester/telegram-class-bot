"""Wrappers"""

from functools import wraps

from sqlalchemy.exc import IntegrityError

from klassbot.db import get_session
from klassbot.models import User


def message_wrapper(private=False):
    """Create a session, handle permissions, handle exceptions and prepare some entities."""

    def real_decorator(func):
        """Parametrized decorator closure."""

        @wraps(func)
        def wrapper(update, context):
            user = None
            session = get_session()
            try:
                if hasattr(update, "message") and update.message:
                    message = update.message
                elif (
                    hasattr(update, "edited_message") and update.edited_message
                ):
                    message = update.edited_message
                else:
                    raise Exception("Got an update without a message")

                user, _ = get_user(session, message.from_user)
                if user.banned:
                    return

                if private and message.chat.type != "private":
                    message.chat.send_message(
                        "Please do this in a direct conversation with me."
                    )
                    return

                response = func(context.bot, update, session, user)

                session.commit()

                # Respond to user
                if response is not None:
                    message.chat.send_message(response)

            except Exception as e:
                session.close()

        return wrapper

    return


def get_user(session, tg_user):
    """Get the user from the event."""
    user = session.query(User).get(tg_user.id)
    if user is None:
        user = User(tg_user.id, tg_user.username)
        session.add(user)
        try:
            session.commit()
            # increase_stat(session, "new_users")
        # Handle race condition for parallel user addition
        # Return the user that has already been created
        # in another session
        except IntegrityError as e:
            session.rollback()
            user = session.query(User).get(tg_user.id)
            if user is None:
                raise e

    if tg_user.username is not None:
        user.username = tg_user.username.lower()

    name = get_name_from_tg_user(tg_user)
    user.name = name

    # Ensure user statistics exist for this user
    # We need to track at least some user activity, since there seem to be some users which
    # abuse the bot by creating polls and spamming up to 1 million votes per day.
    #
    # I really hate doing this, but I don't see another way to prevent DOS attacks
    # without tracking at least some numbers.
    user_statistic = session.query(UserStatistic).get((date.today(), user.id))

    if user_statistic is None:
        user_statistic = UserStatistic(user)
        session.add(user_statistic)
        try:
            session.commit()
        # Handle race condition for parallel user statistic creation
        # Return the statistic that has already been created in another session
        except IntegrityError as e:
            session.rollback()
            user_statistic = session.query(UserStatistic).get(
                (date.today(), user.id)
            )
            if user_statistic is None:
                raise e

    return user, user_statistic


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
