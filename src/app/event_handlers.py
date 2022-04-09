import random
import re

import linebot
from linebot.models import MessageEvent, TextMessage

from src import config
from src.utils import leetcode
from src.app import cache

line_api = linebot.LineBotApi(config.LINE_CHANNEL_TOKEN, config.LINE_API_ENDPOINT)
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    cmd_regex = r"^選題(((?P<easy>\d+)E)?((?P<medium>\d+)M)?((?P<hard>\d+)H)?)$"
    result = re.match(cmd_regex, event.message.text)
    if result is None:
        return

    # We pick non-paid-only questions only.
    questions = list(filter(lambda q: not q.paidOnly, cache.questions))

    easy_count = int(result.groupdict().get("easy") or "0")
    medium_count = int(result.groupdict().get("medium") or "0")
    hard_count = int(result.groupdict().get("hard") or "0")

    # If no difficulty requirement given, pick three easy questions by default.
    if not any((easy_count, medium_count, hard_count)):
        easy_count = 3

    easy_questions = pick_questions(questions, "Easy", easy_count)
    medium_questions = pick_questions(questions, "Medium", medium_count)
    hard_questions = pick_questions(questions, "Hard", hard_count)

    reply_message = compose_message_text(easy_questions, medium_questions, hard_questions)
    line_api.reply_message(event.reply_token, TextMessage(text=reply_message))


def pick_questions(questions: list[leetcode.Question], difficulty: str, count: int) -> list[leetcode.Question]:
    if not count:
        return []
    questions = list(filter(lambda question: question.difficulty == difficulty, questions))
    return random.sample(questions, count)


def compose_message_text(
        easy_questions: list[leetcode.Question],
        medium_questions: list[leetcode.Question],
        hard_questions: list[leetcode.Question],
):
    def compose_single_line(question: leetcode.Question) -> str:
        return f"{question.frontendQuestionId}. {question.title}, link: https://leetcode.com/problems/{question.titleSlug}"

    sections = []
    if easy_questions:
        sections.append("Easy\n" + "\n".join(map(compose_single_line, easy_questions)))
    if medium_questions:
        sections.append("Medium\n" + "\n".join(map(compose_single_line, medium_questions)))
    if hard_questions:
        sections.append("Hard\n" + "\n".join(map(compose_single_line, hard_questions)))

    return "\n".join(sections)
