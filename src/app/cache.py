"""
To not abuse Leetcode API and get blocked, we download the whole
question list and store in a single in this module before the
service is ready to serve traffic.
"""

import gql

from src.utils import leetcode

questions: list[leetcode.Question] = []


def set_question_cache(client: gql.Client):
    global questions
    questions = leetcode.LeetcodeProblemDataDownloader(client).get_all_questions()
