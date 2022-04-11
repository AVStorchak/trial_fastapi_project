import aiofiles
import os

from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_db():
    """
    Creates a new SQLAlchemy local session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user
    :param user: user to be created
    :param db: database session
    :return: updated database with created user
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetches list of users from the database
    :param skip: query offset
    :param limit: query limit
    :param db: database session
    :return: list of users with created items for each user
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetches a user with a list of items created by this user
    :param user_id: id of the user
    :param db: database session
    :return: user attributes together with the list of items created by this user
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Creates an item on behalf of the user
    :param user_id: id of the user
    :param item: item to be created
    :param db: database session
    :return: the created item
    """
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_class=HTMLResponse)
async def read_items(request: Request, page_id: int = 1, page_size: int = 5, db: Session = Depends(get_db)):
    """
    Fetches a list of items according to the specified query range
    and displays it in the browser
    :param request: HTTP request
    :param page_id: number of the page to be displayed
    :param page_size: size of the page to be displayed
    :param db: database session
    :return: HTML response
    """
    skip = (page_id-1) * page_size
    limit = skip + page_size
    items = crud.get_items(db, skip=skip, limit=limit)
    result = [(item.title, item.description) for item in items]
    return templates.TemplateResponse("index.html", {"request": request, "result": result})


@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    async with aiofiles.open(file_location, 'wb+') as f:
        content = await file.read()
        await f.write(content)

    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

'''
@app.post("/upload-file/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
'''


@app.get("/download-file/{filename}")
async def download_file(filename: str):
    file_location = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"files/{filename}")
    #file_location = f"files/{filename}"
    return FileResponse (file_location, filename=filename)
