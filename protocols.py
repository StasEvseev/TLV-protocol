#coding: utf-8


class Protocol(object):
    """
    Фабрика команд.
    """
    @classmethod
    def get_command(cls, type_code):
        try:
            return {
                '0x12': CommandOn,
                '0x13': CommandOff,
                '0x20': CommandColor}[type_code]
        except KeyError:
            print "Nothing"

class CheckDataError(Exception):
    pass

class Command(object):

    @classmethod
    def check_data(cls, length, data):
        pass

    @classmethod
    def do(cls, length, data):
        cls.check_data(length, data)


class CommandEmptyData(Command):
    class EmptyDataError(CheckDataError):
        message = u"Команда не требует данных."

    @classmethod
    def check_data(cls, length, data):
        if length > 0:
            raise CommandEmptyData.EmptyDataError()


class CommandData(Command):
    class DataError(CheckDataError):
        message = u"Для выполнения команды недостаточно данных."
    LENGTH = 1

    @classmethod
    def check_data(cls, length, data):
        if length != cls.LENGTH:
            raise CommandData.DataError()


class CommandOn(CommandEmptyData):
    @classmethod
    def do(cls, length, data):
        super(CommandOn, cls).do(length, data)

        print "ON"

class CommandOff(CommandEmptyData):
    @classmethod
    def do(cls, length, data):
        super(CommandOff, cls).do(length, data)

        print "OFF"

class CommandColor(CommandData):
    LENGTH = 3
    @classmethod
    def do(cls, length, data):
        super(CommandColor, cls).do(length, data)
        print "COLOR (%s)" % ', '.join([hex(x) for x in data])