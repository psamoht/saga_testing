import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import pydub
from io import BytesIO

# We'll store the captured frames and a frame counter in session_state
if "audio_segments" not in st.session_state:
    st.session_state["audio_segments"] = []

if "num_frames" not in st.session_state:
    st.session_state["num_frames"] = 0  # We'll increment this in the callback

def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    """
    Called each time a new audio frame arrives from the browser.
    We'll convert it to pydub.AudioSegment and store it in session_state.
    Also increment a frame counter for debugging.
    """
    # 1. Increment our debug counter
    st.session_state["num_frames"] += 1

    # 2. Convert raw frame data to a pydub.AudioSegment
    #    - Make sure we have a 16-bit PCM array.
    raw_audio = frame.to_ndarray()
    sample_rate = frame.sample_rate
    channels = len(frame.layout.channels)  # e.g. 1 or 2

    audio_segment = pydub.AudioSegment(
        data=raw_audio.tobytes(),
        sample_width=2,        # 16-bit audio
        frame_rate=sample_rate,
        channels=channels
    )

    # 3. Accumulate the segments
    st.session_state["audio_segments"].append(audio_segment)

    # 4. Return the frame unchanged
    return frame

def main():
    st.title("Audio Recorder using streamlit-webrtc")

    st.markdown(
        """
        **Instructions**  
        1. Click "Start" to begin capturing audio from your mic (check your browser's permission settings).  
        2. Speak or make noise, then click "Stop" to end the recording.  
        3. Click "Playback recorded audio" to play what you captured.  
        4. If no audio is recorded, see the debug info below and try the suggestions.  
        """
    )

    # The core webrtc widget: audio only, with our callback to collect frames
    webrtc_ctx = webrtc_streamer(
        key="audio-only",
        mode=WebRtcMode.SENDRECV,            # or SENDONLY if you don't need to receive remote audio
        audio_frame_callback=audio_frame_callback,
        media_stream_constraints={"audio": True, "video": False},  # audio-only
        async_processing=True,
    )

    st.write(f"Debug: Frames received so far: {st.session_state['num_frames']}")

    # Button to play back the captured audio
    if st.button("Playback recorded audio"):
        if len(st.session_state["audio_segments"]) == 0:
            st.warning("No audio recorded yet!")
        else:
            # Combine all segments
            combined_segment = sum(st.session_state["audio_segments"])

            # Convert to WAV bytes
            wav_io = BytesIO()
            combined_segment.export(wav_io, format="wav")

            st.audio(wav_io.getvalue(), format="audio/wav")

    # Button to clear recordings
    if st.button("Clear recording"):
        st.session_state["audio_segments"] = []
        st.session_state["num_frames"] = 0
        st.success("Recording buffer cleared.")

if __name__ == "__main__":
    main()
