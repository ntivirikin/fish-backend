from fastapi import FastAPI

app = FastAPI()

# Sanity test for uvicorn
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Checks number of catches
# @app.get("/{user_id}/check")
@app.get("/check")
async def checkCatches():

    # Check DB here for catch number of user_id
    catches = 0
    return {"catches": catches}