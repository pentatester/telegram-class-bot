from sqlalchemy.orm import Query
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, run_async

from klassbot.models import User, UserKlass, Klass
from klassbot.utils import build_menu, callback_wrapper


@run_async
@callback_wrapper(session_=True)
def klass_list(
    update: Update, context: CallbackContext, user: User, session=None
):
    klasses: Query = session.query(UserKlass).filter_by(user_id=user.id)
    if klasses.count() > 0:
        buttons = list()
        for user_klass in klasses.all():
            klass: Klass = user_klass.klass
            buttons.append(
                InlineKeyboardButton(
                    str(klass.name), callback_data=klass.cb_detail
                )
            )
        menu = build_menu(buttons, 2)
        update.effective_message.reply_text(
            "Your classes", reply_markup=InlineKeyboardMarkup(menu)
        )
    else:
        update.effective_message.reply_text("No class for you.")
    return


@run_async
@callback_wrapper()
def klass_settings(update: Update, context: CallbackContext, user: User):
    if not update.callback_query:
        return


@run_async
@callback_wrapper()
def klass_detail(update: Update, context: CallbackContext, user: User):
    pass
