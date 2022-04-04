from linebot import models


def is_tagged(message: models.TextMessage, user_id: str) -> bool:
    if message.mention is None:
        return False
    mentionee_ids = [mentionee.user_id for mentionee in message.mention.mentionees]
    return user_id in mentionee_ids
