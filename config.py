import os

# Directory for temp files
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# Default values
DEFAULT_MODEL_FILE = os.path.join("models", "kokoro-v1.0.onnx")
DEFAULT_VOICES_FILE = os.path.join("models", "voices-v1.0.bin")
DEFAULT_OUTPUT_FORMAT = "mp3"
DEFAULT_MIN_PAUSE = 0.5
DEFAULT_MAX_PAUSE = 1.2
DEFAULT_SAMPLE_RATE = 24000

# Default sentence configuration
DEFAULT_SENTENCE = {
    "text": "",
    "lang": "en-us",
    "voice": "af_sarah",
    "speed": 1.0,
}

# Voice configurations
VOICES = {
    "en-us": [
        "af_heart",
        "af_alloy",
        "af_aoede",
        "af_bella",
        "af_jessica",
        "af_kore",
        "af_nicole",
        "af_nova",
        "af_river",
        "af_sarah",
        "af_sky",
        "am_adam",
        "am_echo",
        "am_eric",
        "am_fenrir",
        "am_liam",
        "am_michael",
        "am_onyx",
        "am_puck",
        "am_santa",
    ],
    "en-gb": [
        "bf_alice",
        "bf_emma",
        "bf_isabella",
        "bf_lily",
        "bm_daniel",
        "bm_fable",
        "bm_george",
        "bm_lewis",
    ],
    "ja": [
        "jf_alpha",
        "jf_gongitsune",
        "jf_nezumi",
        "jf_tebukuro",
        "jm_kumo",
    ],
    "zh": [
        "zf_xiaobei",
        "zf_xiaoni",
        "zf_xiaoxiao",
        "zf_xiaoyi",
        "zm_yunjian",
        "zm_yunxi",
        "zm_yunxia",
        "zm_yunyang",
    ],
    "es": [
        "ef_dora",
        "em_alex",
        "em_santa",
    ],
    "fr": [
        "ff_siwis",
    ],
    "hi": [
        "hf_alpha",
        "hf_beta",
        "hm_omega",
        "hm_psi",
    ],
    "it": [
        "if_sara",
        "im_nicola",
    ],
    "pt-br": [
        "pf_dora",
        "pm_alex",
        "pm_santa",
    ],
}

LANGS = {
    "American English": "en-us",
    "British English": "en-gb",
    "Japanese": "ja",
    "Mandarin Chinese": "zh",
    "Spanish": "es",
    "French": "fr",
    "Hindi": "hi",
    "Italian": "it",
    "Brazilian Portuguese": "pt-br",
}
