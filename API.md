# API Documentation

This document provides comprehensive documentation for the Audio Studio AI REST API, including examples and usage instructions.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Request Examples](#request-examples)
- [Response Format](#response-format)
- [Error Handling](#error-handling)

## 🏁 Getting Started

### Starting the API Server

```bash
# Navigate to project directory
cd audio-studio-ai

# Start the API server
python api.py
```

The API will be available at: `http://localhost:8000`

### API Documentation

Once the server is running, you can view the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## 📡 Endpoints

### 1. Generate Audio
**POST** `/generate-audio`

Generate audio from text using TTS (Text-to-Speech).

### 2. Download Audio
**GET** `/download/{file_name}`

Download generated audio files.

### 3. List Voices
**GET** `/voices`

Get available voices from the TTS model.

---

## 📝 Request Examples

### 1. Basic Audio Generation (Single Sentence)

```bash
curl -X POST "http://localhost:8000/generate-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      {
        "text": "Hello world! This is a test of the audio generation API.",
        "lang": "en-us",
        "voice": "af_sarah",
        "speed": 1.0
      }
    ],
    "min_pause": 0.5,
    "max_pause": 1.0,
    "output_format": "wav"
  }'
```

### 2. Multiple Sentences with Different Languages

```bash
curl -X POST "http://localhost:8000/generate-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      {
        "text": "Hello, welcome to Audio Studio AI!",
        "lang": "en-us",
        "voice": "af_sarah",
        "speed": 1.0
      },
      {
        "text": "Olá, bem-vindo ao Audio Studio AI!",
        "lang": "pt-br",
        "voice": "pf_dora",
        "speed": 0.9
      },
      {
        "text": "Hola, bienvenido a Audio Studio AI!",
        "lang": "es",
        "voice": "ef_dora",
        "speed": 1.1
      }
    ],
    "min_pause": 0.8,
    "max_pause": 1.5,
    "output_format": "mp3"
  }'
```

### 3. Fast Speech Generation

```bash
curl -X POST "http://localhost:8000/generate-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      {
        "text": "This is a fast-paced announcement. Please pay attention to the following information.",
        "lang": "en-us",
        "voice": "am_michael",
        "speed": 1.5
      }
    ],
    "min_pause": 0.2,
    "max_pause": 0.4,
    "output_format": "wav"
  }'
```

### 4. Slow and Clear Speech

```bash
curl -X POST "http://localhost:8000/generate-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      {
        "text": "This is a slow and clear explanation for educational purposes.",
        "lang": "en-us",
        "voice": "af_nova",
        "speed": 0.7
      }
    ],
    "min_pause": 1.0,
    "max_pause": 2.0,
    "output_format": "mp3"
  }'
```

### 5. Brazilian Portuguese Audio Generation

```bash
curl -X POST "http://localhost:8000/generate-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      {
        "text": "Olá! Bem-vindo ao Audio Studio AI. Esta é uma demonstração da síntese de voz em português brasileiro.",
        "lang": "pt-br",
        "voice": "pf_dora",
        "speed": 1.0
      }
    ],
    "min_pause": 0.6,
    "max_pause": 1.2,
    "output_format": "wav"
  }'
```

### 6. Download Generated Audio

```bash
# First, generate audio and get the download URL from the response
# Then use the file_name from the response to download

curl -X GET "http://localhost:8000/download/output.wav" \
  --output "my_generated_audio.wav"
```

### 7. List Available Voices

```bash
curl -X GET "http://localhost:8000/voices"
```

---

## 📤 Response Format

### Successful Audio Generation Response

```json
{
  "url_download": "/download/output.mp3"
}
```

### Voices List Response

```json
{
  "voices": [
    "af_sarah", "af_nova", "af_river", "am_michael",
    "bf_alice", "jf_alpha", "pf_dora", "..."
  ]
}
```

### Error Response

```json
{
  "detail": "Error message description"
}
```

---

## 🎛️ Request Parameters

### AudioRequest Body

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `sentences` | Array | Yes | - | List of sentences to generate |
| `min_pause` | Float | No | 0.5 | Minimum pause between sentences (seconds) |
| `max_pause` | Float | No | 1.2 | Maximum pause between sentences (seconds) |
| `output_format` | String | No | "mp3" | Audio format: "wav" or "mp3" |

### Sentence Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | String | Yes | Text to convert to speech |
| `lang` | String | Yes | Language code (e.g., "en-us", "pt-br") |
| `voice` | String | Yes | Voice identifier |
| `speed` | Float | Yes | Speech speed (0.5 - 2.0) |

---

## 🌍 Supported Languages & Voices

| Language | Code | Available Voices |
|----------|------|------------------|
| **American English** | `en-us` | af_heart, af_alloy, af_aoede, af_bella, af_jessica, af_kore, af_nicole, af_nova, af_river, af_sarah, af_sky, am_adam, am_echo, am_eric, am_fenrir, am_liam, am_michael, am_onyx, am_puck, am_santa |
| **British English** | `en-gb` | bf_alice, bf_emma, bf_isabella, bf_lily, bm_daniel, bm_fable, bm_george, bm_lewis |
| **Japanese** | `ja` | jf_alpha, jf_gongitsune, jf_nezumi, jf_tebukuro, jm_kumo |
| **Mandarin Chinese** | `zh` | zf_xiaobei, zf_xiaoni, zf_xiaoxiao, zf_xiaoyi, zm_yunjian, zm_yunxi, zm_yunxia, zm_yunyang |
| **Spanish** | `es` | ef_dora, em_alex, em_santa |
| **French** | `fr` | ff_siwis |
| **Hindi** | `hi` | hf_alpha, hf_beta, hm_omega, hm_psi |
| **Italian** | `it` | if_sara, im_nicola |
| **Brazilian Portuguese** | `pt-br` | pf_dora, pm_alex, pm_santa |

---

## ⚠️ Error Handling

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `404` | File not found |
| `422` | Validation error (invalid request parameters) |
| `500` | Internal server error (model not initialized, etc.) |

### Common Error Scenarios

1. **TTS Model Not Initialized**
   ```json
   {
     "detail": "TTS model not initialized"
   }
   ```

2. **Invalid Voice for Language**
   ```json
   {
     "detail": "Validation error: Invalid voice for selected language"
   }
   ```

3. **File Not Found**
   ```json
   {
     "detail": "File not found"
   }
   ```

---

## 💡 Usage Tips

1. **Audio Quality**: Use WAV format for highest quality, MP3 for smaller file sizes
2. **Speech Speed**: Optimal range is 0.8-1.2 for natural speech
3. **Pauses**: Adjust min/max pause for better flow between sentences
4. **Voice Selection**: Test different voices to find the best match for your content
5. **Language Mixing**: You can mix languages within the same request
6. **File Management**: Generated files are stored temporarily and may be cleaned up periodically

---

## 🔧 Integration Examples

### Python with requests

```python
import requests
import json

def generate_audio(text, lang="en-us", voice="af_sarah", output_format="mp3"):
    url = "http://localhost:8000/generate-audio"
    data = {
        "sentences": [{
            "text": text,
            "lang": lang,
            "voice": voice,
            "speed": 1.0
        }],
        "output_format": output_format
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        download_url = f"http://localhost:8000{result['url_download']}"
        return download_url
    else:
        print(f"Error: {response.text}")
        return None

# Usage
download_url = generate_audio("Hello, this is a test!")
print(f"Download your audio: {download_url}")
```

### JavaScript with fetch

```javascript
async function generateAudio(text, lang = "en-us", voice = "af_sarah", outputFormat = "mp3") {
    const url = "http://localhost:8000/generate-audio";
    const data = {
        sentences: [{
            text: text,
            lang: lang,
            voice: voice,
            speed: 1.0
        }],
        output_format: outputFormat
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            return `http://localhost:8000${result.url_download}`;
        } else {
            console.error('Error:', await response.text());
            return null;
        }
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Usage
generateAudio("Hello, this is a test!").then(downloadUrl => {
    console.log(`Download your audio: ${downloadUrl}`);
});
```
