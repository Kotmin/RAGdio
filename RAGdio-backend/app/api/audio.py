from fastapi import APIRouter, UploadFile, File, HTTPException
from app.adapters.whisper import WhisperAudioProcessor

router = APIRouter()
whisper_processor = WhisperAudioProcessor()


@router.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    """Endpoint to upload an audio file and get transcribed text."""
    try:
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        text = whisper_processor.transcribe(file_path)
        return {"filename": file.filename, "transcription": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
