from telegram import Update, Chat, ChatMember
from telegram.ext import run_async, CallbackContext

from klassbot.models import Klass, User, UserKlass
from klassbot.utils.wrappers import private_command_wrapper, klass_command_wrapper


@run_async
@private_command_wrapper()
def start(update: Update, context: CallbackContext, user: User = None):
    update.effective_message.reply_text("Welcome!\nSend /help")


@run_async
@klass_command_wrapper(True)
def start_klass(
    update: Update,
    context: CallbackContext,
    user: UserKlass = None,
    klass: Klass = None,
):
    if klass.started:
        return
    chat: Chat = update.effective_chat
    chat_member: ChatMember = chat.get_member(user.user_id)
    if not chat_member.status == ChatMember.CREATOR:
        return
    update.effective_message.reply_text(
        """
    Thanks, please give me permission for
    Ban Users
    Add Users
    Pin Messages
    Then send /create command.
    """
    )
    if user:
        user.from_chat(chat)
    klass.creator = user.user
    klass.started = True
    return


@run_async
@private_command_wrapper()
def start_join(update: Update, context: CallbackContext, user: User = None):
    pass
