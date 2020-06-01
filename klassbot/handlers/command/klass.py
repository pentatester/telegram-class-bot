from telegram import Update
from telegram.ext import CallbackContext, run_async

from klassbot.models import User
from klassbot.utils.wrappers import private_command_wrapper


@run_async
@private_command_wrapper()
def klass_list(update: Update, context: CallbackContext, user: User = None):
    pass
