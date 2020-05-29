from telegram import Update
from telegram.ext import run_async, CallbackContext

from klassbot.models import User, UserKlass, Klass
from klassbot.utils.wrappers import message_wrapper


@run_async
@message_wrapper(True)
def create(update: Update, context: CallbackContext, user: User = None):
    update.effective_message.reply_text(
        """
    To create a class, add me to the group.
    Then give me permission for
    Ban Users
    Add Users
    Pin Messages
    Then send /create command.
    """
    )
    return


@run_async
@message_wrapper(True, True)
def create_klass(update: Update, context: CallbackContext, user: UserKlass = None, klass: Klass = None):
    pass
