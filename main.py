import streamlit as st
import numpy as np
import io
import wave
import tempfile
import base64

def record_audio_html():
    # ... (same as before)

def main():
    st.title("Browser-Based Voice Recorder and Player")

    audio_rec_html_str = record_audio_html()
    st.components.v1.html(audio_rec_html_str, height=100)

    audio_data_base64 = st.session_state.get("audio_base64")

    if audio_data_base64:
        audio_bytes = base64.b64decode(audio_data_base64)
        st.audio(audio_bytes, format='audio/wav')

        st.download_button(
            label="Download WAV",
            data=audio_bytes,
            file_name="recording.wav",
            mime="audio/wav"
        )

    def receive_audio(event):
        st.session_state["audio_base64"] = event.detail
        st.experimental_rerun()

    st.components.v1.html(f"""<script>
        document.addEventListener('audio_available', function(event) {{
            window.parent.postMessage({{
                'type': 'audio_available',
                'detail': event.detail
            }}, "*");
        }});

        window.addEventListener('message', function(event) {{
            if (event.data.type === 'audio_available') {{
                const event = new CustomEvent('audio_available', {{ detail: event.data.detail }});
                document.dispatchEvent(event);
            }}
        }});

    </script>""", height=0)

    import streamlit.components.v1 as components
    components.html(
        f"""
    <script>
    window.addEventListener('message', function(event) {{
        if (event.data.type === 'audio_available') {{
            Streamlit.setComponentValue(event.data.detail);
        }}
    }});
    </script>
    """,
        height=0,
    )

    audio_base64_from_js = components.html(
        """<script>
        document.addEventListener('audio_available', function(event) {
            Streamlit.setComponentValue(event.detail);
        });
        </script>""",
        height=0,
    )

    if audio_base64_from_js:  # Add this check
        receive_audio({'detail': audio_base64_from_js})

if __name__ == "__main__":
    main()
