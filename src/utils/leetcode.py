import dataclasses
import textwrap

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(url="https://leetcode.com/graphql/")


@dataclasses.dataclass
class Question:
    difficulty: str
    frontendQuestionId: str
    paidOnly: bool
    title: str
    titleSlug: str


class LeetcodeProblemDataDownloader:
    _client: Client

    def __init__(self, gql_client: Client):
        self._client = gql_client

    def get_all_questions(self) -> list[Question]:
        query = gql(textwrap.dedent(
            """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
              problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
              ) {
                total: totalNum
                questions: data {
                  difficulty
                  frontendQuestionId: questionFrontendId
                  paidOnly: isPaidOnly
                  title
                  titleSlug
                }
              }
            }
            """
        ))
        args = {
            "categorySlug": "",
            # We download the whole list before the service starts,
            # so the latency is not an issue.
            "limit": 10000,
            "skip": 0,
            "filters": {
                # We don't need paid-only questions so far.
                "premiumOnly": False,
                # We perform difficulty filtering locally. For reference only.
                # "difficulty": "EASY",
            }
        }
        result = self._client.execute(query, args)
        return [Question(**question) for question in result["problemsetQuestionList"]["questions"]]
