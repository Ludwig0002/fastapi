from typing import Optional
from fastapi import FastAPI

# app = FastAPI()
# @app.get("/")
# async def root():
#    return {"message": "Hello World"}
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}



# from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oder spezifische Domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/sse")
async def sse_endpoint():
    async def event_generator():
        for i in range(10):
            yield f"data: Nachricht {i}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
