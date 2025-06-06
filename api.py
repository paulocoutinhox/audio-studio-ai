import os
from typing import List

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config import (
    DEFAULT_MAX_PAUSE,
    DEFAULT_MIN_PAUSE,
    DEFAULT_MODEL_FILE,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_VOICES_FILE,
    LANGS,
    TEMP_DIR,
)
from utils import (
    generate_audio_for_sentence,
    generate_silence,
    load_kokoro_model,
    save_final_audio,
    save_sentence_audio,
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Kokoro model
try:
    kokoro = load_kokoro_model(DEFAULT_MODEL_FILE, DEFAULT_VOICES_FILE)
except Exception as e:
    print(f"Error loading model: {e}")
    kokoro = None


class Sentence(BaseModel):
    text: str
    lang: str
    voice: str
    speed: float


class AudioRequest(BaseModel):
    sentences: List[Sentence]
    min_pause: float = DEFAULT_MIN_PAUSE
    max_pause: float = DEFAULT_MAX_PAUSE
    output_format: str = DEFAULT_OUTPUT_FORMAT


@app.post("/generate-audio")
async def generate_audio(request: AudioRequest):
    if not kokoro:
        raise HTTPException(status_code=500, detail="TTS model not initialized")

    try:
        # Generate audio for all sentences
        audios = []
        sentence_files = []
        sample_rate = DEFAULT_SAMPLE_RATE

        for idx, sentence in enumerate(request.sentences):
            # Generate audio for sentence
            samples, sample_rate = generate_audio_for_sentence(
                kokoro,
                {
                    "text": sentence.text,
                    "lang": sentence.lang,
                    "voice": sentence.voice,
                    "speed": sentence.speed,
                },
                sample_rate,
            )
            audios.append(samples)

            # Save individual sentence audio
            sentence_files.append(
                save_sentence_audio(samples, sample_rate, idx, request.output_format)
            )

            # Add silence between sentences (except for last sentence)
            if idx < len(request.sentences) - 1:
                silence = generate_silence(
                    sample_rate, request.min_pause, request.max_pause
                )
                audios.append(silence)

        # Concatenate all audio samples
        combined_samples = np.concatenate(audios)

        # Save final audio file
        audio_file = save_final_audio(
            combined_samples, sample_rate, request.output_format
        )

        return {
            "url_download": f"/download/{os.path.basename(audio_file)}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{file_name}")
async def download_audio(file_name: str):
    file_path = os.path.join(TEMP_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Determine media type based on file extension
    file_extension = os.path.splitext(file_name)[1].lower()
    if file_extension == ".mp3":
        media_type = "audio/mpeg"
    elif file_extension == ".wav":
        media_type = "audio/wav"
    else:
        media_type = "audio/wav"  # Default fallback

    return FileResponse(file_path, media_type=media_type, filename=file_name)


# Add route before the main block
@app.get("/voices")
async def list_voices():
    if not kokoro:
        raise HTTPException(status_code=500, detail="TTS model not initialized")

    try:
        # Get available voices from the model
        voices = kokoro.get_voices()
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
