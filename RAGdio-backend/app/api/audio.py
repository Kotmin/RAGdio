from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.adapters.whisper import WhisperAudioProcessor

from app.adapters.whisper_api import WhisperAPIAudioProcessor
router = APIRouter()
# whisper_processor = WhisperAudioProcessor()
whisper_processor = WhisperAPIAudioProcessor()


@router.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    """Endpoint to upload an audio file and get transcribed text."""
    try:
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        text = whisper_processor.transcribe(file_path)
        return {"filename": file.filename, "transcription": text}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
