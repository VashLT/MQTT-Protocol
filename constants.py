import random

BROKER = 'broker.emqx.io'
PORT = 1883
TOPICS = ["/upvotes_down100", "/upvotes_up100"]
CLIENT_ID = f"python-mqtt-{random.randint(0, 1000)}"
USERNAME = "emqx"
PASSWORD = "public"

SRC_URL = "https://news.ycombinator.com/"

NOT_ARG_MSG = "missing parameter, pass a topic, can be '-100' or '+100', which correspond to the number of upvotes"