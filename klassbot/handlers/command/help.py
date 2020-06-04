from telegram import Update
from telegram.ext import CallbackContext, run_async

from klassbot.models import User
from klassbot.utils.wrappers import private_command_wrapper


@run_async
@private_command_wrapper()
def help(update: Update, context: CallbackContext, user: User):
    update.effective_message.reply_text("Check")
