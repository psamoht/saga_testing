import streamlit as st
from st_audiorec import st_audiorec

def record_audio():
    """
    Returns audio data recorded via the st_audiorec component.
    Including a stable key to help Streamlit handle widget re-runs.
    """
    # We use a stable key to avoid re-mounting issues.
    audio_data = st_audiorec(key="my_audio_recorder")
    return audio_data

def main():
    st.title("Audio Recorder Demo")

    st.write(
        "1. Verify your browser has granted microphone permission.\n"
        "2. Click the microphone icon to start recording. Click again to stop.\n"
        "3. If it records only briefly or not at all, try:\n"
        "   • Refreshing the page\n"
        "   • Clicking 'Reset' and re-trying\n"
        "   • Changing browsers\n"
        "   • Checking st_audiorec GitHub issues if persistent"
    )

    # Get the audio data
    audio_data = record_audio()

    if audio_data is not None:
        st.write("Your recording is ready. Click play below to listen.")
        st.audio(audio_data, format="audio/wav")

if __name__ == "__main__":
    main()
