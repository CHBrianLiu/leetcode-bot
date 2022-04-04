import random

import linebot
from linebot.models import MessageEvent, TextMessage

from src import config
from src.utils import line, leetcode
from src.app import cache

line_api = linebot.LineBotApi(config.LINE_CHANNEL_TOKEN, config.LINE_API_ENDPOINT)
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    # Tag message only.
    if not line.is_tagged(event.message, config.LINE_OFFICIAL_ACCOUNT_ID):
        return

    reply_token = event.reply_token

    # For the current version, we pick 3 easy questions. This logic should be improved in the future.
    questions = list(filter(lambda question: question.difficulty == "Easy", cache.questions))
    picked = random.sample(questions, 3)
    reply_message = compose_message_text(picked)

    line_api.reply_message(reply_token, TextMessage(text=reply_message))


def compose_message_text(questions: list[leetcode.Question]):
    def compose_single_line(question: leetcode.Question) -> str:
        return f"{question.frontendQuestionId}. {question.title}, link: https://leetcode.com/problems/{question.titleSlug}"

    return "\n".join(map(compose_single_line, questions))
