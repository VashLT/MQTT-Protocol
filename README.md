# MQTT-Protocol
Publish / Subscribe archetype implementation using https://mosquitto.org/ and python.

Publisher web scrapping data from [https://news.ycombinator.com/](https://news.ycombinator.com/) and publish to two different topics:
- upvotes_up100 news with upvotes over 100
- upvotes_down100 news with upvotes under 100

The news are retrieved using bs4 library.
