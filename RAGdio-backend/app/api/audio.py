from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
# from app.adapters.whisper import WhisperAudioProcessor

from app.adapters.whisper_api import WhisperAPIAudioProcessor
router = APIRouter()
# whisper_processor = WhisperAudioProcessor()
whisper_processor = WhisperAPIAudioProcessor()


@router.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    """Endpoint to upload an audio file and get transcribed text."""
    try:
        temp_dir = Path("temp")
        temp_dir.mkdir(parents=True, exist_ok=True)


        # prevent collisions?
#         import uuid
        # file_path = temp_dir / f"{uuid.uuid4()}.wav"
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # text = whisper_processor.transcribe(file_path)
        text = "yes yes"

        Path(file_path).unlink(missing_ok=True)
                # Return structured response
        # return SendFileResponse(
        #     filename=file.filename,
        #     transcription=text
        # )

        # return {"filename": file.filename, "transcription": text}
        return {"filename": "file ", "transcription": text}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
