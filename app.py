import os

import numpy as np
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="Audio Studio AI", layout="wide")

from config import (
    DEFAULT_MAX_PAUSE,
    DEFAULT_MIN_PAUSE,
    DEFAULT_MODEL_FILE,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_VOICES_FILE,
    LANGS,
)
from utils import (
    create_new_sentence,
    export_sentences,
    generate_audio_for_sentence,
    generate_silence,
    get_voices_for_lang,
    import_sentences,
    load_kokoro_model,
    move_sentence,
    save_final_audio,
    save_sentence_audio,
    validate_voice_for_lang,
)


def init_session_state():
    """Initialize session state variables"""
    if "sentences" not in st.session_state:
        st.session_state.sentences = [create_new_sentence([])]
    if "audio_generated" not in st.session_state:
        st.session_state.audio_generated = False
    if "audio_file" not in st.session_state:
        st.session_state.audio_file = ""
    if "sentence_files" not in st.session_state:
        st.session_state.sentence_files = []
    # This ID will be used to create unique keys for all UI components
    if "ui_key_base" not in st.session_state:
        st.session_state.ui_key_base = 0


def add_sentence_callback():
    """Callback for adding a new sentence"""
    st.session_state.sentences.append(create_new_sentence(st.session_state.sentences))
    # Regenerate UI keys
    st.session_state.ui_key_base += 1


def delete_sentence_callback(idx):
    """Callback for deleting a sentence"""
    st.session_state.sentences.pop(idx)
    # Regenerate UI keys
    st.session_state.ui_key_base += 1


def move_up_callback(idx):
    """Callback for moving a sentence up"""
    st.session_state.sentences = move_sentence(st.session_state.sentences, idx, "up")
    # Regenerate UI keys
    st.session_state.ui_key_base += 1


def move_down_callback(idx):
    """Callback for moving a sentence down"""
    st.session_state.sentences = move_sentence(st.session_state.sentences, idx, "down")
    # Regenerate UI keys
    st.session_state.ui_key_base += 1


def import_sentences_callback():
    """Callback for importing sentences"""
    if st.session_state.import_file is not None:
        try:
            imported_sentences = import_sentences(
                st.session_state.import_file.getvalue()
            )
            # Make sure each sentence has all required fields
            for sentence in imported_sentences:
                if "text" not in sentence:
                    sentence["text"] = ""
                if "lang" not in sentence:
                    sentence["lang"] = "en-us"
                if "voice" not in sentence:
                    sentence["voice"] = "af_sarah"
                if "speed" not in sentence:
                    sentence["speed"] = 1.0
                # Validate voice for language
                validate_voice_for_lang(sentence)

            st.session_state.sentences = imported_sentences
            # Regenerate UI keys to force a UI refresh
            st.session_state.ui_key_base += 1
            st.session_state.import_success = True
        except Exception as e:
            st.error(str(e))


def render_sidebar():
    """Render sidebar configuration"""
    # Center the logo in sidebar using native Streamlit
    _, col2, _ = st.sidebar.columns([1, 2, 1])
    with col2:
        st.image(
            "extras/images/logo-sidebar.png",
            use_container_width=True,
        )

    st.sidebar.markdown("#### Audio Settings")

    output_formats = ["wav", "mp3"]
    config = {
        "output_format": st.sidebar.selectbox(
            "Output format",
            output_formats,
            index=(
                output_formats.index(DEFAULT_OUTPUT_FORMAT)
                if DEFAULT_OUTPUT_FORMAT in output_formats
                else 0
            ),
            key=f"output_format_{st.session_state.ui_key_base}",
        ),
        "min_pause": st.sidebar.slider(
            "Min silence (seconds)",
            0.1,
            3.0,
            DEFAULT_MIN_PAUSE,
            0.1,
            key=f"min_pause_{st.session_state.ui_key_base}",
        ),
        "max_pause": st.sidebar.slider(
            "Max silence (seconds)",
            0.1,
            3.0,
            DEFAULT_MAX_PAUSE,
            0.1,
            key=f"max_pause_{st.session_state.ui_key_base}",
        ),
        "model_file": st.sidebar.text_input(
            "Model file (.onnx)",
            DEFAULT_MODEL_FILE,
            key=f"model_file_{st.session_state.ui_key_base}",
        ),
        "voices_file": st.sidebar.text_input(
            "Voices file (.bin)",
            DEFAULT_VOICES_FILE,
            key=f"voices_file_{st.session_state.ui_key_base}",
        ),
    }

    # Import functionality
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Import/Export Sentences")

    # Use on_change to detect when file is uploaded
    st.sidebar.file_uploader(
        "Import sentences JSON",
        type=["json"],
        key="import_file",
        on_change=import_sentences_callback,
    )

    # Show success message if needed
    if "import_success" in st.session_state and st.session_state.import_success:
        st.sidebar.success("Sentences imported successfully!")
        st.session_state.import_success = False

    # Export functionality with direct download
    json_str = export_sentences(st.session_state.sentences)
    st.sidebar.download_button(
        "Export sentences",
        json_str,
        file_name="sentences.json",
        mime="application/json",
        key=f"export_btn_{st.session_state.ui_key_base}",
    )

    return config


def render_sentence_editor(idx, sent):
    """Render the editor for a single sentence"""
    key_base = f"{idx}_{st.session_state.ui_key_base}"

    st.markdown(f"**Sentence {idx+1}**")
    cols = st.columns([4, 2, 2, 1, 1, 1, 1])

    # Text input with on_change callback to update session state
    def update_text():
        st.session_state.sentences[idx]["text"] = st.session_state[f"text_{key_base}"]

    sent["text"] = cols[0].text_area(
        f"Text {idx+1}",
        value=sent["text"],
        key=f"text_{key_base}",
        on_change=update_text,
    )

    # Language selection with on_change callback
    def update_lang():
        st.session_state.sentences[idx]["lang"] = st.session_state[f"lang_{key_base}"]
        validate_voice_for_lang(st.session_state.sentences[idx])

    sent["lang"] = cols[1].selectbox(
        "Language",
        list(LANGS.values()),
        index=list(LANGS.values()).index(sent["lang"]),
        key=f"lang_{key_base}",
        on_change=update_lang,
    )

    # Voice selection with on_change callback
    def update_voice():
        st.session_state.sentences[idx]["voice"] = st.session_state[f"voice_{key_base}"]

    voices = get_voices_for_lang(sent["lang"])
    sent["voice"] = cols[2].selectbox(
        "Voice",
        voices,
        index=voices.index(sent["voice"]) if sent["voice"] in voices else 0,
        key=f"voice_{key_base}",
        on_change=update_voice,
    )

    # Speed control with on_change callback
    def update_speed():
        st.session_state.sentences[idx]["speed"] = st.session_state[f"speed_{key_base}"]

    sent["speed"] = cols[3].number_input(
        "Speed",
        0.5,
        2.0,
        sent["speed"],
        0.1,
        key=f"speed_{key_base}",
        on_change=update_speed,
    )

    # Move up/down buttons
    if cols[4].button("⬆️", key=f"up_{key_base}"):
        move_up_callback(idx)
        st.rerun()

    if cols[5].button("⬇️", key=f"down_{key_base}"):
        move_down_callback(idx)
        st.rerun()

    # Delete button
    if cols[6].button("🗑️", key=f"del_{key_base}"):
        delete_sentence_callback(idx)
        st.rerun()


def render_sentences_tab():
    """Render the sentences editor tab"""
    st.header("Sentences")

    # Display the current sentences
    for idx, sent in enumerate(st.session_state.sentences):
        render_sentence_editor(idx, sent)

    st.markdown("---")

    # Add new sentence button
    if st.button("Add Sentence", key=f"add_sentence_{st.session_state.ui_key_base}"):
        add_sentence_callback()
        st.rerun()


def render_generation_tab(config):
    """Render the audio generation tab"""
    st.header("Audio Generation")

    if st.button("Generate Audio", key=f"gen_audio_{st.session_state.ui_key_base}"):
        st.session_state.audio_generated = False
        st.session_state.audio_file = ""
        st.session_state.sentence_files = []

        # Validate model files
        if not os.path.exists(config["model_file"]):
            st.error(f"Model file not found: {config['model_file']}")
            st.info(
                "Please download the model files and place them in the app directory."
            )
            return

        if not os.path.exists(config["voices_file"]):
            st.error(f"Voices file not found: {config['voices_file']}")
            st.info(
                "Please download the voices file and place it in the app directory."
            )
            return

        # Load model and generate audio
        with st.spinner("Loading Kokoro model..."):
            try:
                kokoro = load_kokoro_model(config["model_file"], config["voices_file"])
            except Exception as e:
                st.error(str(e))
                return

        audios = []
        sentence_files = []

        progress = st.progress(0, "Generating audio for sentences...")
        for i, sent in enumerate(st.session_state.sentences):
            progress.progress(
                i / len(st.session_state.sentences),
                f"Processing sentence {i+1}/{len(st.session_state.sentences)}",
            )

            # Generate audio for sentence
            samples, sample_rate = generate_audio_for_sentence(
                kokoro, sent, DEFAULT_SAMPLE_RATE
            )
            audios.append(samples)

            # Save individual sentence audio
            sentence_files.append(save_sentence_audio(samples, sample_rate, i))

            # Add silence between sentences
            silence = generate_silence(
                sample_rate, config["min_pause"], config["max_pause"]
            )
            audios.append(silence)

        # Save final audio
        full_audio = np.concatenate(audios)
        st.session_state.audio_file = save_final_audio(
            full_audio, DEFAULT_SAMPLE_RATE, config["output_format"]
        )
        st.session_state.audio_generated = True
        st.session_state.sentence_files = sentence_files
        progress.progress(1.0, "Done!")

    # Show generated audio
    if st.session_state.audio_generated and st.session_state.audio_file:
        st.success("Audio generated successfully!")

        # Play full audio
        audio_bytes = open(st.session_state.audio_file, "rb").read()
        st.audio(
            audio_bytes,
            format=f"audio/{config['output_format']}",
        )

        # Download button
        st.download_button(
            "Download Audio",
            audio_bytes,
            file_name=f"output.{config['output_format']}",
            key=f"download_audio_{st.session_state.ui_key_base}",
        )

        # Individual sentence preview
        st.subheader("Preview Each Sentence")
        for idx, sent_file in enumerate(st.session_state.sentence_files):
            if os.path.exists(sent_file):
                st.markdown(f"Sentence {idx+1}:")
                st.audio(
                    open(sent_file, "rb").read(),
                    format=f"audio/{config['output_format']}",
                )


def main():
    # Initialize session state
    init_session_state()

    # Render sidebar and get config
    config = render_sidebar()

    # Create tabs
    tab1, tab2 = st.tabs(["Sentences", "Audio Generation"])

    with tab1:
        render_sentences_tab()

    with tab2:
        render_generation_tab(config)


if __name__ == "__main__":
    main()
