import uvicorn
from fastapi import FastAPI

from schemas import Orders

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


@app.post("/orders/orders")
def test(items: Orders):
    return {'status': 'success'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
