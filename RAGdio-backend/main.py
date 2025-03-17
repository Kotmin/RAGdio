from fastapi import FastAPI, UploadFile, File
from app.services.audio_service import AudioProcessor
from app.adapters.whisper_adapter import WhisperAudioProcessor

app = FastAPI()
audio_processor = WhisperAudioProcessor()  # Can be replaced later

@app.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    text = await audio_processor.process_audio(file)
    return {"transcription": text}