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

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oder spezifische Domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/sse")
async def sse_endpoint():
    async def event_generator():
        for i in range(10):
            yield f"data: Nachricht {i}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")








@app.post("/upload1")
async def sse_endpoint():
    async def event_generator():
        for i in range(10):
            yield f"data: Nachricht {i}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")





# from fastapi import FastAPI, Request
# from fastapi.responses import StreamingResponse
# import asyncio

# app = FastAPI()

@app.post("/upload2")
async def sse_endpoint(request: Request):
    async def event_generator():
        body = await request.body()
        total_size = len(body)
        chunk_size = total_size // 20  # 5% Schritte
        sent = 0
        last_percent = 0

        for i in range(0, total_size, chunk_size):
            await asyncio.sleep(0.2)  # Simuliere Verarbeitung
            sent = min(i + chunk_size, total_size)
            percent = int((sent / total_size) * 100)

            if percent >= last_percent + 5:
                last_percent = percent
                # yield f"{percent}\n\n"
                json_data = json.dumps({"progress": percent})
                yield f"data: {json_data}\n\n"


        yield f"100\n\n" # yield f"data: Upload abgeschlossen\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")











@app.post("/upload")
async def upload(request: Request):
    size = 0
    total = int(request.headers.get('content-length', 0))
    chunk_size = 1024 * 1024  # 1MB
    last_reported_progress = 0

    async for chunk in request.stream():
        size += len(chunk)
        if total:
            progress = int((size / total) * 100)
            if progress >= last_reported_progress + 5:
                last_reported_progress = progress
                print(f"Fortschritt: {progress}% ({size} von {total} Bytes)")

    return JSONResponse({"message": "Upload abgeschlossen"})

