from fastapi import FastAPI as f 


app = f()
@app.get("/")
def root():
    return {"Message": "hello bro"} 