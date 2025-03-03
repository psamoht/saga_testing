import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import pydub
from io import BytesIO

# Keep track of audio data and frames
if "audio_segments" not in st.session_state:
    st.session_state["audio_segments"] = []

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    raw_audio = frame.to_ndarray()
    sample_rate = frame.sample_rate
    channels = len(frame.layout.channels)

    # Convert raw audio to a pydub segment
    segment = pydub.AudioSegment(
        data=raw_audio.tobytes(),
        sample_width=2,          # 16-bit audio
        frame_rate=sample_rate,
        channels=channels
    )

    st.session_state["audio_segments"].append(segment)
    return frame

def main():
    st.title("Streamlit-WebRTC Audio Recorder")

    # Start/Stop button from streamlit-webrtc
    webrtc_streamer(
        key="audio-only",
        mode=WebRtcMode.SENDONLY,  # Only sends audio from mic to server
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={"audio": True, "video": False}
    )

    # Playback button
    if st.button("Playback recorded audio"):
        if len(st.session_state["audio_segments"]) == 0:
            st.warning("No audio recorded yet!")
        else:
            combined = sum(st.session_state["audio_segments"])
            wav_io = BytesIO()
            combined.export(wav_io, format="wav")
            st.audio(wav_io.getvalue(), format="audio/wav")

    # Clear button
    if st.button("Clear recording"):
        st.session_state["audio_segments"] = []
        st.success("Recording cleared. Press 'Start' to record again.")

if __name__ == "__main__":
    main()
