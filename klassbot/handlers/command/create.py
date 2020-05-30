from telegram import Update, Chat, ChatMember
from telegram.ext import run_async, CallbackContext

from klassbot.models import User, UserKlass, Klass
from klassbot.utils.wrappers import message_wrapper, klass_command_wrapper


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
@klass_command_wrapper(True)
def create_klass(
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
    if user:
        user.from_chat(chat)
    klass.creator = user.user
    klass.started = True
    return
