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





@app.post("/upload")
async def upload(request: Request):
    size = 0
    total = int(request.headers.get('content-length', 0))
    chunk_size = 1024 * 1024  # 1MB
    async for chunk in request.stream():
        size += len(chunk)
        progress = (size / total) * 100 if total else None
        print(f"Empfangen: {size} Bytes, Fortschritt: {progress:.2f}%")
        # Hier können Sie z.B. Zwischenspeichern oder verarbeiten

    return JSONResponse({"message": "Upload abgeschlossen"})
