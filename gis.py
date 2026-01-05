import sys

from src.commands import Command
from src.index import Map

def switch(cmd):
    msg = ''
    if cmd.h == True:
        msg = 'helping'
    if cmd.rootCommand == 'map':
        if cmd.targetType == 'base':
            MAP = Map(cmd.targetType)
            MAP.start()
            msg = 'map base'
        else:
            msg = 'not recognized target type'
            return False, msg
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

