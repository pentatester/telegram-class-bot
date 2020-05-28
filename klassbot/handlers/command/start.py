from telegram import Update
from telegram.ext import run_async, CallbackContext

from klassbot.utils.wrappers import private_wrapper


@run_async
@private_wrapper
def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text("Welcome!")
