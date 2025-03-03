"""
Streamlit Audio Recorder Demo with Debug Suggestions
====================================================

This script uses st_audiorec for in-browser audio recording and immediate
playback. Some users experience a short, cutoff initial recording, requiring
extra clicks (Start → Stop → Reset → Start). This quirk is often due to how
the underlying st_audiorec JavaScript manages microphone state.

Tips:
- Check mic permissions in your browser.
- Refresh or try a different browser (Chrome, Firefox, Edge).
- Check logs if you see errors.
- If the flow remains problematic, consider using streamlit-webrtc instead.
"""

import streamlit as st
from st_audiorec import st_audiorec

def main():
    st.title("Audio Recorder in Streamlit")

    st.markdown(
        """
        **Instructions**  
        1. Make sure your browser's microphone permission is granted.  
        2. Click the microphone below to start recording, click again to stop.  
        3. If it only records for a split second on the first try, you may need 
           to click "Reset" and start again. (This is a known quirk with some
           st_audiorec versions/browsers.)  
        4. Once you have a proper recording, it will appear below.
        """
    )

    # Attempt to record audio
    audio_data = st_audiorec()

    # Debugging: show raw data structure to see if it recorded anything
    st.write("Debug: raw audio_data output:", audio_data)

    # If there is recorded audio, let the user play it
    if audio_data is not None:
        st.write("Your recording is ready. Click the play button below to listen.")
        st.audio(audio_data, format="audio/wav")

if __name__ == "__main__":
    main()
