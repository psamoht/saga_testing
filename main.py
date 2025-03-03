import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import pydub
from io import BytesIO

# Keep a list of pydub.AudioSegment and a frame counter to debug frames
if "audio_segments" not in st.session_state:
    st.session_state["audio_segments"] = []
if "num_frames" not in st.session_state:
    st.session_state["num_frames"] = 0

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    # Each incoming frame increments the counter and is converted to pydub
    st.session_state["num_frames"] += 1

    raw_audio = frame.to_ndarray()
    sample_rate = frame.sample_rate
    channels = len(frame.layout.channels)

    segment = pydub.AudioSegment(
        data=raw_audio.tobytes(),
        sample_width=2,      # 16-bit
        frame_rate=sample_rate,
        channels=channels
    )
    st.session_state["audio_segments"].append(segment)

    return frame  # Must return the frame for callback signature

def main():
    st.title("Audio Recorder using streamlit-webrtc (SENDONLY)")

    st.write(
        "Click **Start** to begin recording. Then click **Stop** when done.\n"
        "If you see errors, let the page fully load before pressing Start."
    )

    webrtc_ctx = webrtc_streamer(
        key="audio-only",
        mode=WebRtcMode.SENDONLY,  # Only send audio from your mic to the server
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={"audio": True, "video": False},
        # Removed async_processing to reduce event-loop complexity
    )

    st.write(f"Frames captured: {st.session_state['num_frames']}")

    if st.button("Playback recorded audio"):
        if len(st.session_state["audio_segments"]) == 0:
            st.warning("No audio recorded yet!")
        else:
            combined = sum(st.session_state["audio_segments"])
            wav_io = BytesIO()
            combined.export(wav_io, format="wav")
            st.audio(wav_io.getvalue(), format="audio/wav")

    if st.button("Clear recording"):
        st.session_state["audio_segments"] = []
        st.session_state["num_frames"] = 0
        st.success("Cleared recorded audio.")

if __name__ == "__main__":
    main()
