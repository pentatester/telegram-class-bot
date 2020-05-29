from telegram import Update
from telegram.ext import run_async, CallbackContext

from klassbot.models import User
from klassbot.utils.wrappers import message_wrapper


@run_async
@message_wrapper(False)
def start(update: Update, context: CallbackContext, user: User = None):
    update.effective_message.reply_text("Welcome!\nSend /help")
