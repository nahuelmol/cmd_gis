import sys

from src.commands import Command
from src.index import Map

def switch(cmd):
    msg = ''
    if cmd.h == True:
        msg = 'helping'
    if cmd.rootCommand == 'map':
        MAP = Map(cmd.targetType)
        if cmd.targetType == 'base':
            MAP.base()
            msg = 'map base'
        elif cmd.targetType == 'prof':
            MAP.add_profiles()
            msg = 'add point'
        elif cmd.targetType == 'sh':
            MAP.sheet()
            msg = 'add sheet'
        elif cmd.targetType == 'zeb':
            MAP.zebra()
            msg = 'add sheet'
        else:
            msg = 'not recognized map type'
            return False, msg
        MAP.save()
    msg = '----PROCESS:DONE----{}'.format(msg)
    return True, msg

if __name__ == "__main__":
    command = None
    if (len(sys.argv) > 0):
        command = Command(sys.argv)
    else:
        msg = 'please, be serious, type a valid command'
        sys.exit(msg)
    command.setCommand()
    res, msg = command.setArgs()
    if res == True:
        print(msg)
    res, msg = switch(command)
    print(msg)

