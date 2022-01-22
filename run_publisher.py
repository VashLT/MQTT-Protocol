import sys
from defs import Publisher, connect_broker
from constants import NOT_ARG_MSG

def setup(arg):
    if not arg:
        print(NOT_ARG_MSG)
        return

    client = connect_broker()
    client.loop_start()
    Publisher(client, arg[0], freq_min=0.1)

if __name__ == "__main__":
    setup(sys.argv[1:])