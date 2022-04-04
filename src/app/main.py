import fastapi
import gql
import gql.transport.requests

from src.app import routes
from src.app import cache
from src import config

app = fastapi.FastAPI()

gql_transport = gql.transport.requests.RequestsHTTPTransport(url=config.LEETCODE_GRAPHQL_ENDPOINT)
gql_client = gql.Client(transport=gql_transport)
cache.set_question_cache(gql_client)

app.include_router(routes.router)
