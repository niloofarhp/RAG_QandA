from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
import uvicorn
import os
import time
from typing import Generator

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <html>
        <head>
            <title>Shyftlabs RAG Application</title>
        </head>
        <body>
            <h1>Welcome to the Shyftlabs RAG Application</h1>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Allow only PDF and HTML file types
    allowed_extensions = {"pdf", "html"}
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and HTML are allowed.")

    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = os.path.join(upload_dir, filename)
    
    # Save the uploaded file
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"info": f"File '{filename}' saved at '{file_location}'"}

def fake_streaming() -> Generator[str, None, None]:
    # Simulate a streaming response in chunks
    for i in range(5):
        yield f"Chunk {i+1}: This is part of the streamed output.\n"
        time.sleep(1)

@app.get("/stream")
async def stream_output():
    return StreamingResponse(fake_streaming(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
