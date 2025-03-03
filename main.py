import streamlit as st
# pip install streamlit-media-recorder
from streamlit_media_recorder import st_media_recorder

def main():
    st.title("Record & Play Audio")

    # This component shows a "Start" button. Once pressed, it records
    # audio from your mic. Press "Stop" to finish.
    audio_data = st_media_recorder(audio=True, video=False)

    # If we have recorded audio data, let the user play it back.
    if audio_data is not None:
        st.write("Here is your recorded audio:")
        st.audio(audio_data, format="audio/wav")

if __name__ == "__main__":
    main()
