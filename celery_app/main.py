from fastapi import FastAPI, File, UploadFile

from celery_app.celery_worker import upload_file


app = FastAPI()


@app.post("/upload-file/")
def post_file(file: UploadFile = File(...)):
    upload_file.delay(file)
    return {"message": "The requested file will be uploaded soon!"}
