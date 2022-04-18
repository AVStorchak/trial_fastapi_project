import aiofiles

from celery import Celery
from celery.utils.log import get_task_logger

celery = Celery('tasks',
                broker='amqp://guest:guest@127.0.0.1:5672//')
celery_log = get_task_logger(__name__)


@celery.task
async def upload_file(uploaded_file: object) -> object:
    """
    Uploads files to the server.
    :param uploaded_file: file to be uploaded
    :return: completion status
    """
    file_location = f"files/{uploaded_file.filename}"
    async with aiofiles.open(file_location, 'wb+') as f:
        while content := await uploaded_file.read(1024):
            await f.write(content)

    return {"Result": "OK"}
