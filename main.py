from fastapi import FastAPI, Request, Form, File,UploadFile, BackgroundTasks
from fastapi.responses import FileResponse

import psycopg2
import os

# establish a connection
conn = psycopg2.connect(
    host="localhost",
    database="",
    user="",
    password=""
)

# create a cursor object

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/hello")
async def hello():
    results = []
    cur = conn.cursor()
    try:
    
        # execute a query
        cur.execute("SELECT * FROM yourtable")

        # fetch the results
        results = cur.fetchall()

        # print the results
        for row in results:
            print(row)

        # close the cursor and connection
    finally:
        cur.close()
        conn.close()
    return {"message":results}

@app.post("/post1")
async def test(request: Request):
    data = await request.json()

    # Access the value based on the key
    value = data.get("name")
    return value


@app.post("/upload")
async def upload(file: UploadFile = File(...), description: str = Form(...)):
    print(description)
    try:
        file_extension = os.path.splitext(file.filename)[1]  # Get the file extension
        # Define the desired filename
        desired_filename = "pic" + file_extension
        root_dir = os.getcwd()+"/media/"
        file_path = os.path.join(root_dir, desired_filename)
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        return {"message": f"There was an error uploading the file {e}"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/image")
def get_image():
    root_dir = os.getcwd()
    image_path = root_dir+"\media\shopping-cart-309592_1280.png"  # Specify the path to the image file
    return FileResponse(image_path, media_type="image/jpeg")


def process_data(desc: str = Form(...)):
    # Simulate some long-running process
    print(f"Processing data: {desc}")
    # ... Additional processing logic ...

@app.post("/data")
async def create_data(background_tasks: BackgroundTasks, desc: str = Form(...)):
    background_tasks.add_task(process_data, desc)
    return {"message": "Data processing has been scheduled"}