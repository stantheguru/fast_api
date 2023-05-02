from fastapi import FastAPI
import psycopg2

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