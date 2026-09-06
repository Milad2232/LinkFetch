from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI(title="LinkFetch Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {
        "app": "LinkFetch Backend",
        "status": "online"
    }


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    url = request.url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    ydl_opts = {
        "quiet": True,
        "no_warnings": False,
        "skip_download": True,
        "js_runtimes": {"deno": {}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []

        for fmt in info.get("formats", []):
            if not fmt.get("url"):
                continue

            formats.append({
                "format_id": fmt.get("format_id"),
                "ext": fmt.get("ext"),
                "resolution": fmt.get("resolution"),
                "width": fmt.get("width"),
                "height": fmt.get("height"),
                "fps": fmt.get("fps"),
                "filesize": fmt.get("filesize"),
                "vcodec": fmt.get("vcodec"),
                "acodec": fmt.get("acodec"),
            })

        return {
            "success": True,
            "id": info.get("id"),
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "webpage_url": info.get("webpage_url"),
            "formats": formats,
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not analyze this URL: {str(e)}"
        )