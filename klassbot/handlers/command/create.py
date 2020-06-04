from telegram import Update
from telegram.ext import run_async, CallbackContext

from klassbot.models import Klass, User, UserKlass
from klassbot.utils.wrappers import private_command_wrapper, klass_command_wrapper


@run_async
@private_command_wrapper()
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
@klass_command_wrapper(False)
def klass_id(
    update: Update,
    context: CallbackContext,
    user: UserKlass = None,
    klass: Klass = None,
):
    if not klass.started:
        return
    update.effective_message.reply_text(
        f"This class id : {klass.id}\nInvite link {klass.invite_link}"
    )
    return
