import sys
from defs import Subscriber, connect_broker
from constants import NOT_ARG_MSG

def run(topics):
    if not topics:
        print(NOT_ARG_MSG)
        return

    print(topics)

    client = connect_broker()
    Subscriber(client, topics)
    
    client.loop_forever()

if __name__ == "__main__":
    # pass command line arguments
    run(sys.argv[1:])