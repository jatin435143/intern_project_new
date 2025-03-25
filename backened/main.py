from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_code
import uvicorn


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_code
import uvicorn

# ✅ Define app first
app = FastAPI()

# ✅ Add CORS middleware AFTER defining `app`
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/analyze-code")
async def analyze_code_file(file: UploadFile = File(...)):
    content = await file.read()
    result = analyze_code(file.filename, content.decode("utf-8"))
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
