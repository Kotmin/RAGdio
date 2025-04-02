from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from typing import List
# from app.adapters.whisper import WhisperAudioProcessor

from app.adapters.whisper_api import WhisperAPIAudioProcessor

from app.services.audio_factory import AudioProcessorFactory

router = APIRouter()
# whisper_processor = WhisperAudioProcessor()
# transcribe_processor = WhisperAPIAudioProcessor()

from app.services.rag_pipeline import RAGPipelineService

pipeline = RAGPipelineService()
transcribe_processor = AudioProcessorFactory().get_audio_processor()



SUPPORTED_FORMATS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}
MAX_FILES = 5

@router.post("/upload_audio/")
async def upload_audio(files: List[UploadFile] = File(...)):
    """Endpoint to upload an audio file and get transcribed text."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    if len(files) > MAX_FILES:
        raise HTTPException(status_code=413, detail=f"Max {MAX_FILES} files allowed.")
    

    try:
        temp_dir = Path("temp")
        temp_dir.mkdir(parents=True, exist_ok=True)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    results = []
    for file in files:
        ext = file.filename.split(".")[-1].lower()
        if ext not in SUPPORTED_FORMATS:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {file.filename}")
        

    # prevent collisions?
    # import uuid
    # file_path = f"temp/{uuid.uuid4()}.{ext}"
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        try:
            transcription = transcribe_processor.transcribe(file_path)
            # transcription = "yes yes" *32
            results.append({
                "filename": file.filename,
                "transcription": transcription
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
        finally:
            # print("ok")
            Path(file_path).unlink(missing_ok=True)

    return {"results": results}
            # Return structured response
    # return SendFileResponse(
    #     filename=file.filename,
    #     transcription=transcription
    # )

    # return {"filename": file.filename, "transcription": transcription}
    # return {"filename": "file ", "transcription": transcription}


# TODO guess that payload should be defined
@router.post("/rag/ingest")
async def manual_ingest(payload: dict):
    transcription = payload.get("transcription")
    metadata = payload.get("metadata", {})

    if not transcription:
        raise HTTPException(status_code=400, detail="Missing transcription.")

    pipeline.ingest_text(transcription, metadata)
    return {"status": "ok"}
