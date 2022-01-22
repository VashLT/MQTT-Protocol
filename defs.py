import time
import requests
from bs4 import BeautifulSoup
from typing import Union
from constants import TOPICS, CLIENT_ID, USERNAME, PASSWORD, BROKER, PORT, SRC_URL
from paho.mqtt import client as mqtt_client


class PubSubMember:
    def __init__(self, client: mqtt_client, topic: Union[str, list] = "-100"):
        self._client = client
        if isinstance(topic, list):
            self._topic = []
            for item in topic:
                self._topic.append(self.get_topic(item))
        else:
            self._topic = self.get_topic(topic)

    def get_topic(self, arg):
        """arg can be -100 or +100 to get the respective topic"""
        if arg == "-100":
            return TOPICS[0]
        elif arg == "+100":
            return TOPICS[1]

        return ""


class Publisher(PubSubMember):
    def __init__(self, client, topic, freq_min=2):
        super().__init__(client, topic)
        self._freq = freq_min * 60
        self._message_count = 0

        self.start()

    def get_news_up100(self):
        if not hasattr(self, "_news_up100"):
            self._news_up100 = self.get_news(100, float("inf"))
            self._news_up100_index = 0
            self._news_up100_page = 0

        if self._news_up100_index >= len(self._news_up100):
            self._news_up100_page += 1
            self._news_up100_index = 0
            self._news_up100 = self.get_news(100, float("inf"), page=self._news_up100_page)

        self._news_up100_index += 1
        return self._news_up100[self._news_up100_index - 1]

    def get_news_down100(self):
        if not hasattr(self, "_news_down100"):
            self._news_down100 = self.get_news(0, 100)
            self._news_down100_index = 0
            self._news_down100_page = 0

        if self._news_down100_index >= len(self._news_down100):
            self._news_down100_page += 1
            self._news_down100_index = 0
            self._news_down100 = self.get_news(0, 100, page=self._news_down100_page)

        self._news_down100_index += 1
        return self._news_down100[self._news_down100_index - 1]
    
    def get_news(self, min_votes, max_votes, page = 0):
        tries = 0
        while tries < 5:
            news = get_news(min_votes, max_votes, page)
            if news:
                return news
            tries += 1
        return ['Last piece of news that could be found.']

    def start(self):
        should_iterate = True if isinstance(self._topic, list) else False
        while True:
            time.sleep(self._freq)
            if should_iterate:
                for topic in self._topic:
                    self.publish(topic)
            else:
                self.publish(self._topic)

    def publish(self, topic):
        msg = self.get_news_down100() if topic == TOPICS[0] else self.get_news_up100()
        status = self._client.publish(topic, msg)[0]

        if status == 0:
            print(f"Sent `{msg}` to topic `${topic}`")
        else:
            print(f"Failed to send message to topic `{topic}`")

        self._message_count += 1


class Subscriber(PubSubMember):
    def __init__(self, client: mqtt_client, topic: Union[str, list]):
        super().__init__(client, topic)

        if isinstance(self._topic, list):
            print(self._topic)
            topics = []
            for item in self._topic:
                topics.append((item, 0))

            print(topics)
            self._client.subscribe(topics)
        else:
            self._client.subscribe(self._topic)
        self._client.on_message = self.on_message

    def on_message(self, _, __, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def connect_broker():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code ${rc}\n")

    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)

    return client


def get_news(min_threshold: int, max_threshold: int, page=0):
    """Gets news from https://news.ycombinator.com/
    with upvotes between min_threshold and max_threhsold
    """
    url = SRC_URL
    if page > 0:
        # add parameters to the url
        url += f"news?p={page}"

    content = requests.get(url).content

    soup = BeautifulSoup(content, "html.parser")

    news = soup.find_all("tr", class_="athing")

    formatted_news = []
    for item in news:
        upvotes_container = item.findNext("tr").find("span")
        upvotes = int(upvotes_container.get_text().split(" ")[0])
        if upvotes <= min_threshold or upvotes >= max_threshold:
            continue

        link = item.find("a", class_="titlelink", href=True)
        news_item = f"{link.get_text()} || {link['href']}"

        formatted_news.append(news_item)

    return formatted_news


if __name__ == "__main__":
    get_news(0, 100)
