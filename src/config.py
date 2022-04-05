import os

# Use the template to add a config
# NAME = os.environ.get("NAME", "DEFAULT")
LINE_CHANNEL_TOKEN = os.environ.get("LINE_CHANNEL_TOKEN", "")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
# We can replace this config to test Line Messaging API locally
LINE_API_ENDPOINT = os.environ.get("LINE_API_ENDPOINT", "https://api.line.me")

LEETCODE_GRAPHQL_ENDPOINT = os.environ.get("LEETCODE_GRAPHQL_ENDPOINT", "https://leetcode.com/graphql/")
