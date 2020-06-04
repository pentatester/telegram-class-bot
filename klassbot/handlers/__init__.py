from klassbot.handlers.command import register as register_commands
from klassbot.handlers.conversation import register as registes_conversations

registrar = [register_commands, registes_conversations]


def register(dispatcher):
    for reg in registrar:
        reg(dispatcher)
