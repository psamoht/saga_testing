import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import pydub
from io import BytesIO

# Store recorded audio segments
if "audio_segments" not in st.session_state:
    st.session_state["audio_segments"] = []

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    raw_audio = frame.to_ndarray()
    sample_rate = frame.sample_rate
    channels = len(frame.layout.channels)

    # Convert raw audio to pydub segment
    segment = pydub.AudioSegment(
        data=raw_audio.tobytes(),
        sample_width=2,  # 16-bit audio
        frame_rate=sample_rate,
        channels=channels
    )
    st.session_state["audio_segments"].append(segment)
    return frame

def main():
    st.title("Audio Recorder (streamlit-webrtc)")

    webrtc_streamer(
        key="audio-only",
        mode=WebRtcMode.SENDONLY,  # Only sends audio from mic
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={"audio": True, "video": False}
    )

    if st.button("Playback recorded audio"):
        if not st.session_state["audio_segments"]:
            st.warning("No audio recorded yet!")
        else:
            combined = sum(st.session_state["audio_segments"])
            wav_io = BytesIO()
            combined.export(wav_io, format="wav")
            st.audio(wav_io.getvalue(), format="audio/wav")

    if st.button("Clear recording"):
        st.session_state["audio_segments"] = []
        st.success("Recording cleared. Click Start again to record.")

if __name__ == "__main__":
    main()
