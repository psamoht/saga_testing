"""
Streamlit Audio Recorder without 'key' Parameter
================================================

This script records audio in the user's browser using st_audiorec, then
plays it back immediately. It omits the 'key' argument to avoid TypeError
on older st_audiorec versions.

If you need stable widget states, consider upgrading st_audiorec to a
version that supports the 'key' argument, or explore alternative approaches.
"""

import streamlit as st
from st_audiorec import st_audiorec

def record_audio():
    """
    Creates an audio recorder widget and returns the recorded WAV data.
    """
    # Just call st_audiorec() without passing key=..., to avoid the TypeError.
    audio_data = st_audiorec()
    return audio_data

def main():
    """
    Main function that sets up the Streamlit app layout, instructions, and
    handles audio recording + playback.
    """
    st.title("Audio Recorder in Streamlit")

    st.write(
        "Click on the microphone icon below to start and stop recording. "
        "If you see errors, check your microphone permissions or logs."
    )

    # Capture audio data
    audio_data = record_audio()

    # If there's valid audio data, let the user play it
    if audio_data is not None:
        st.write("Your recording is ready. Click play below to listen.")
        st.audio(audio_data, format="audio/wav")

if __name__ == "__main__":
    main()
