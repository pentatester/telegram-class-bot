from telegram import Update
from telegram.ext import CallbackContext, run_async

from klassbot.models import User
from klassbot.utils.wrappers import message_wrapper


@run_async
@message_wrapper(False)
def help(update: Update, context: CallbackContext, user: User):
    update.effective_message.reply_text("Check")
