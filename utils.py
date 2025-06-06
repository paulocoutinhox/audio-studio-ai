import json
import os
import random

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

from config import DEFAULT_SENTENCE, TEMP_DIR, VOICES


def load_kokoro_model(model_file, voices_file):
    """Load the Kokoro TTS model"""
    try:
        return Kokoro(model_file, voices_file)
    except Exception as e:
        raise Exception(f"Error loading model: {e}")


def generate_audio_for_sentence(kokoro, sentence, sample_rate):
    """Generate audio for a single sentence"""
    return kokoro.create(
        sentence["text"],
        voice=sentence["voice"],
        speed=sentence["speed"],
        lang=sentence["lang"],
    )


def save_sentence_audio(samples, sample_rate, idx, output_format="wav"):
    """Save audio for a single sentence"""
    temp_sent_file = os.path.join(TEMP_DIR, f"sentence_{idx}.{output_format}")
    sf.write(temp_sent_file, samples, sample_rate)
    return temp_sent_file


def generate_silence(sample_rate, min_pause, max_pause):
    """Generate silence between sentences"""
    return np.zeros(int(random.uniform(min_pause, max_pause) * sample_rate))


def save_final_audio(full_audio, sample_rate, output_format):
    """Save the complete audio file"""
    full_path = os.path.join(TEMP_DIR, f"output.{output_format}")
    sf.write(full_path, full_audio, sample_rate)
    return full_path


def get_voices_for_lang(lang):
    """Get available voices for a language"""
    return VOICES.get(lang, [])


def validate_voice_for_lang(sentence):
    """Validate and fix voice selection for language"""
    voices = get_voices_for_lang(sentence["lang"])
    if sentence["voice"] not in voices and voices:
        sentence["voice"] = voices[0]
        return True
    return False


def create_new_sentence(sentences):
    """Create a new sentence copying settings from the last one if available"""
    if not sentences:
        return DEFAULT_SENTENCE.copy()

    last_sentence = sentences[-1]
    return {
        "text": "",  # Always empty text
        "lang": last_sentence["lang"],
        "voice": last_sentence["voice"],
        "speed": last_sentence["speed"],
    }


def move_sentence(sentences, idx, direction):
    """Move a sentence up or down in the list"""
    if direction == "up" and idx > 0:
        sentences[idx], sentences[idx - 1] = sentences[idx - 1], sentences[idx]
    elif direction == "down" and idx < len(sentences) - 1:
        sentences[idx], sentences[idx + 1] = sentences[idx + 1], sentences[idx]
    return sentences


def export_sentences(sentences):
    """Export sentences to JSON string"""
    return json.dumps(sentences, indent=2)


def import_sentences(json_data):
    """Import sentences from JSON data"""
    try:
        imported = json.loads(json_data)
        if not isinstance(imported, list):
            raise ValueError("Invalid format: expected a list of sentences")
        return imported
    except Exception as e:
        raise Exception(f"Error importing sentences: {e}")
