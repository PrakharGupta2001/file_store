from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import os
import hashlib
from collections import Counter

app = FastAPI()
FILE_DIR = "./server/storage"
os.makedirs(FILE_DIR, exist_ok=True)
metadata = {}  # Map filenames to content hashes


# Utility: Get file hash
def get_file_hash(file_content):
    return hashlib.md5(file_content).hexdigest()


# 1. Add a file to the store
@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    file_hash = get_file_hash(content)
    file_path = os.path.join(FILE_DIR, file_hash)

    if file_hash in metadata.values():
        return JSONResponse(content={"message": "Duplicate content!"}, status_code=409)

    with open(file_path, "wb") as f:
        f.write(content)

    metadata[file.filename] = file_hash
    return {"message": f"File '{file.filename}' uploaded successfully", "hash": file_hash}


# 2. Resumable file uploads (chunked)
@app.post("/files/chunk")
async def upload_file_chunk(file: UploadFile = File(...), chunk_number: int = Form(...), total_chunks: int = Form(...)):
    chunk_dir = os.path.join(FILE_DIR, f"{file.filename}_chunks")
    os.makedirs(chunk_dir, exist_ok=True)
    chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_number}")

    with open(chunk_path, "wb") as f:
        f.write(await file.read())

    if len(os.listdir(chunk_dir)) == total_chunks:
        with open(os.path.join(FILE_DIR, file.filename), "wb") as final_file:
            for i in range(1, total_chunks + 1):
                with open(os.path.join(chunk_dir, f"chunk_{i}"), "rb") as chunk_file:
                    final_file.write(chunk_file.read())
        os.rmdir(chunk_dir)
        return {"message": "File uploaded successfully"}

    return {"message": f"Chunk {chunk_number}/{total_chunks} uploaded"}


# 3. List files
@app.get("/files")
def list_files():
    return {"files": list(metadata.keys())}


# 4. Delete a file
@app.delete("/files/{filename}")
def delete_file(filename: str):
    file_hash = metadata.get(filename)
    if not file_hash:
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(os.path.join(FILE_DIR, file_hash))
    metadata.pop(filename)
    return {"message": f"File '{filename}' deleted successfully"}


# 5. Word count and frequency analysis
@app.get("/files/analysis")
def file_analysis(limit: int = 10, order: str = "desc"):
    word_count = 0
    word_freq = Counter()

    for file_hash in os.listdir(FILE_DIR):
        with open(os.path.join(FILE_DIR, file_hash), "r") as f:
            words = f.read().split()
            word_count += len(words)
            word_freq.update(words)

    sorted_freq = word_freq.most_common(limit if order == "desc" else -limit)
    return {"word_count": word_count, "frequent_words": sorted_freq}


# Health checks
@app.get("/healthz")
def health_check():
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}
