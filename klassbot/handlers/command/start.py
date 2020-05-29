from telegram import Update
from telegram.ext import run_async, CallbackContext

from klassbot.models import User
from klassbot.utils.wrappers import private_wrapper


@run_async
@private_wrapper(False)
def start(update: Update, context: CallbackContext, user: User = None):
    update.effective_message.reply_text("Welcome!")
