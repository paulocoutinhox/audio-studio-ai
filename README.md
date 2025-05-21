<p align="center">
    <a href="https://github.com/paulocoutinhox/audio-studio-ai" target="_blank" rel="noopener noreferrer">
        <img width="180" src="extras/images/logo.png" alt="Logo">
    </a>
</p>

# Audio Studio AI 🎤

Audio Studio AI is an interactive application built with **Python** and **Streamlit**, allowing users to generate high-quality audio content locally using advanced text-to-speech technology. It's perfect for creating voiceovers for videos, podcasts, and other audio content.

## 🚀 Features

- **Local AI-powered text-to-speech** with high-quality voice synthesis
- **Multiple language support** with various voices for each language
- **Sentence-based audio generation** with customizable pauses
- **Individual sentence preview** and editing
- **Export/Import** functionality for sentence configurations
- **Multiple output formats** (WAV, MP3)
- **Customizable speech speed** for each sentence
- **Beautiful Streamlit web interface** for easy interaction
- **Local processing** - no cloud dependencies required

## 📞 Installation

### **1. Clone the Repository**
```sh
git clone https://github.com/paulocoutinhox/audio-studio-ai.git
cd audio-studio-ai
```

### **2. Create a Virtual Environment**
```sh
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Download Required Model Files**
Download the required model files from the model repository and place them in the `models/` directory of the project. See the [Model Support](#model-support) section for details.

## ⚙️ Configuration

### **1. Model Files**
The application expects the model files to be in the `models/` directory. See the [Model Support](#model-support) section for specific file requirements.

### **2. Output Configuration**
You can configure the following settings in the sidebar:
- Output format (WAV or MP3)
- Minimum and maximum pause duration between sentences
- Model and voices file paths

## 🛠️ Usage

1. **Run the Application**
   ```sh
   streamlit run app.py
   ```

2. **Steps in the Web UI**
   - Add sentences using the "Add Sentence" button
   - For each sentence:
     - Enter the text
     - Select the language
     - Choose a voice
     - Adjust the speech speed
   - Use the up/down arrows to reorder sentences
   - Delete sentences using the trash icon
   - Click "Generate Audio" to create the final audio
   - Preview individual sentences or download the complete audio

## 🌍 Supported Languages and Voices

The application supports multiple languages with various voices for each:

- **American English** (en-us)
  - Multiple voices including af_sarah, af_nova, af_river, and more
- **British English** (en-gb)
  - Voices like bf_alice, bf_emma, bm_daniel, and more
- **Japanese** (ja)
  - Voices including jf_alpha, jf_gongitsune, jm_kumo, and more
- **Mandarin Chinese** (zh)
  - Multiple voices like zf_xiaobei, zf_xiaoxiao, zm_yunjian, and more
- **Spanish** (es)
  - Voices including ef_dora, em_alex
- **French** (fr)
  - Voice ff_siwis
- **Hindi** (hi)
  - Voices including hf_alpha, hf_beta, hm_omega
- **Italian** (it)
  - Voices if_sara, im_nicola
- **Brazilian Portuguese** (pt-br)
  - Voices pf_dora, pm_alex, pm_santa

## 🤖 Model Support

This application currently supports the Kokoro TTS model for high-quality text-to-speech synthesis. To use the application:

1. Download the following files from [Hugging Face - Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M):
   - `kokoro-v1.0.onnx`
   - `voices-v1.0.bin`

2. Download the model files using these direct links:
   - [kokoro-v1.0.onnx](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx)
   - [voices-v1.0.bin](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin)

3. Place these files in the `models/` directory of the project.

The Kokoro model provides:
- High-quality voice synthesis
- Support for multiple languages
- Various voice options for each language
- Fast local processing
- No cloud dependencies

## 📁 Project Structure

```
audio-studio-ai/
│
├── 📝 README.md               # Project documentation and guide
├── 🎯 app.py                  # Main Streamlit application interface
├── ⚙️ config.py               # Configuration and settings management
├── 🛠️ utils.py                # Utility functions and helpers
├── 📦 requirements.txt        # Project dependencies list
│
├── 🤖 models/                 # AI model files directory
│   ├── 🧠 kokoro-v1.0.onnx    # TTS neural network model
│   └── 🗣️ voices-v1.0.bin     # Voice data and configurations
│
├── 🎵 temp/                   # Temporary audio files storage
│
└── 🎨 extras/                 # Additional resources
    └── 🖼️ images/             # Images, icons and assets
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push to the branch (`git push origin feature-xyz`)
5. Open a **pull request**

## 📞 Contact

For issues or contributions, open a **GitHub issue** or contact:
💎 **paulocoutinhox@gmail.com**
🔗 **[GitHub](https://github.com/paulocoutinho)**

## 📜 License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2025, Paulo Coutinho
