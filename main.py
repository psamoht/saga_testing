import streamlit as st

#for festlng small code pieces
# Provided by streamlit-audiorec
# pip install streamlit-audiorec
from st_audiorec import st_audiorec

def main():
    st.title("Simple Audio Recorder in Streamlit")

    st.write("Click the microphone button below to start recording. "
             "Click again to stop. Your recorded audio will appear below.")

    # This returns `None` until a recording is made. Afterwards it returns WAV bytes.
    audio_data = st_audiorec()

    if audio_data is not None:
        st.write("### Playback:")
        st.audio(audio_data, format="audio/wav")

if __name__ == "__main__":
    main()
