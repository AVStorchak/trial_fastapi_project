from fastapi import APIRouter, FastAPI, File, UploadFile

from celery_app.celery_worker import upload_file

router = APIRouter(prefix="/celery", tags=['celery app'])


@router.post("/upload-file/")
def post_file(file: UploadFile = File(...)) -> object:
    """
    Calls worker to save the file locally. Not functional currently.
    :param file: file to be saved.
    """
    pass
    #upload_file.delay(file)
    #return {"message": "The requested file will be uploaded soon!"}
