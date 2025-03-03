"""
Audio Recording and Playback with streamlit-webrtc
==================================================

1. Install dependencies in your requirements.txt:
   streamlit-webrtc
   av
   pydub

2. Deploy or run locally. 
3. Click "Start" on the webrtc widget to begin capturing audio frames.
4. Click "Stop" when you're finished.
5. Press "Playback recorded audio" to hear your captured audio.
6. Press "Clear recording" if you want to discard and record again.
"""

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import pydub
from io import BytesIO

# We'll store the captured audio segments in session_state so they persist
# across script reruns while the app is running.
if "audio_segments" not in st.session_state:
    st.session_state["audio_segments"] = []

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    """
    This callback is invoked in real-time for each incoming audio frame.
    We convert the raw data to a pydub AudioSegment and store it in session_state.
    """
    # Convert the frame's audio data to a NumPy array (int16)
    raw_audio = frame.to_ndarray()
    sample_rate = frame.sample_rate
    channels = len(frame.layout.channels)  # typically 1 or 2

    # Create a pydub AudioSegment from the raw PCM audio
    audio_segment = pydub.AudioSegment(
        data=raw_audio.tobytes(),
        sample_width=2,       # 16-bit audio
        frame_rate=sample_rate,
        channels=channels
    )

    # Accumulate the segments in session_state
    st.session_state["audio_segments"].append(audio_segment)

    # Return the frame unmodified (required for callback signature)
    return frame

def main():
    st.title("Audio Recorder using streamlit-webrtc")

    st.write(
        "1. Click **Start** below to begin capturing audio from your microphone.\n"
        "2. Speak or make noise.\n"
        "3. Click **Stop** to end recording.\n"
        "4. Press **Playback recorded audio** to listen.\n"
        "5. Press **Clear recording** to start over."
    )

    # The webrtc_streamer sets up the audio pipeline. 
    # mode=WebRtcMode.SENDRECV means we send audio from the browser to the server,
    # and also can receive something back (though we won't use returning stream here).
    # audio_frame_callback is where we handle frames.
    webrtc_ctx = webrtc_streamer(
        key="audio-only",
        mode=WebRtcMode.SENDRECV,
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={"audio": True, "video": False},  # audio-only
        async_processing=True,
    )

    # Button: Playback the recorded audio
    if st.button("Playback recorded audio"):
        if len(st.session_state["audio_segments"]) == 0:
            st.warning("No audio recorded yet!")
        else:
            # Concatenate all recorded segments into one continuous segment
            combined_segment = sum(st.session_state["audio_segments"])

            # Convert the combined segment to WAV in memory
            wav_io = BytesIO()
            combined_segment.export(wav_io, format="wav")

            # st.audio() can play the WAV data directly from bytes
            st.audio(wav_io.getvalue(), format="audio/wav")

    # Button: Clear any accumulated audio
    if st.button("Clear recording"):
        st.session_state["audio_segments"] = []
        st.success("Recording buffer cleared. You can record again.")

if __name__ == "__main__":
    main()
