from klassbot.handlers.command import register as register_commands

registrar = [register_commands]


def register(dispatcher):
    for reg in registrar:
        reg(dispatcher)
