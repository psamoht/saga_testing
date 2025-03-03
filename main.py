import streamlit as st
import base64

def record_audio_html():
    """Generates HTML and JavaScript for browser-based audio recording."""
    audio_rec_js = """
    <script>
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.onload = () => {
                    const base64Audio = reader.result.split(',')[1];
                    const event = new CustomEvent("audio_available", { detail: base64Audio });
                    document.dispatchEvent(event);
                };
                reader.readAsDataURL(audioBlob);

            });

            document.getElementById("recordButton").onclick = () => {
                audioChunks.length = 0; // Clear previous recording
                mediaRecorder.start();
                document.getElementById("recordButton").disabled = true;
                document.getElementById("stopButton").disabled = false;
            };

            document.getElementById("stopButton").onclick = () => {
                mediaRecorder.stop();
                document.getElementById("recordButton").disabled = false;
                document.getElementById("stopButton").disabled = true;

            };
        });
    </script>
    <button id="recordButton">Record</button>
    <button id="stopButton" disabled>Stop</button>
    """
    return audio_rec_js

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
    audio_base64_from_js = components.html(
        """<script>
        document.addEventListener('audio_available', function(event) {
            Streamlit.setComponentValue(event.detail);
        });
        </script>""",
        height=0,
    )

    if audio_base64_from_js:
        receive_audio({'detail': audio_base64_from_js})

if __name__ == "__main__":
    main()
