import streamlit as st

# IMPORTANT: You must install st_audiorec separately.
# pip install streamlit-audiorec
from st_audiorec import st_audiorec

def main():
    st.title("Audio Recorder in Streamlit")

    st.write("Click the microphone button below to start and stop recording.")

    # This function call creates the audio recorder widget.
    # Once the user finishes recording, the return value will no longer be None.
    audio_data = st_audiorec()

    # If we have recorded audio data, we can play it back to the user.
    if audio_data is not None:
        st.write("Here is your recorded audio:")
        st.audio(audio_data, format='audio/wav')

if __name__ == "__main__":
    main()
