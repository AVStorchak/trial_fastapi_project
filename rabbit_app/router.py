from fastapi import Request, APIRouter

from .schema import MessageSchema


router = APIRouter(
    tags=['rabbit app'],
    responses={404: {"description": "Page not found"}}
)


@router.post('/send-message')
async def send_message(payload: MessageSchema, request: Request):
    """
    Sends message to the pika client
    :param payload: message payload
    :param request: HTML request
    :return: completion status
    """
    request.app.pika_client.send_message(
        {"message": payload.message}
    )
    return {"status": "ok"}
