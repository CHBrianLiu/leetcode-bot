import fastapi
import linebot
import linebot.exceptions

from src.app.event_handlers import webhook_handler

router = fastapi.APIRouter()


@router.post("/webhook")
async def line_message_api_webhook_api(request: fastapi.Request):
    """
    Respond 200 OK for every request that passes the signature validation
    """
    try:
        body = (await request.body()).decode("utf-8")
        x_line_signature = request.headers.get("x-line-signature", "")
        webhook_handler.handle(body, x_line_signature)
    except linebot.exceptions.InvalidSignatureError as e:
        raise fastapi.HTTPException(400) from e
    return


@router.get("/ping")
async def health_check_api():
    """
    Respond "pong" for every single request. This API is to keep the app awake on Heroku.
    """
    return {"message": "pong"}
