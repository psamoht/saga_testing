import streamlit as st
import streamlit.components.v1 as components
import base64

# -------------------------------------------------------------------
# 1. Define the custom component with embedded HTML/JS
# -------------------------------------------------------------------
# We’ll embed raw JavaScript that uses the MediaRecorder API to:
# - Prompt for microphone permission
# - Start/Stop recording
# - Convert the result to a WAV blob
# - Base64-encode it and send to Streamlit via Streamlit.setComponentValue()
# 
# The component returns that base64 string to Python when recording stops.

recorder_component = components.declare_component(
    "simple_audio_recorder",
    """
    <div style="text-align:center">
      <button id="startBtn">Start Recording</button>
      <button id="stopBtn" style="margin-left: 10px;">Stop Recording</button>
      <p id="status" style="margin-top: 10px; color: green;"></p>
    </div>
    <script>
    (function() {
      const startBtn = document.getElementById('startBtn');
      const stopBtn = document.getElementById('stopBtn');
      const statusEl = document.getElementById('status');

      let mediaRecorder;
      let audioChunks = [];

      // Request mic access up front so user sees prompt.
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          mediaRecorder = new MediaRecorder(stream);

          mediaRecorder.ondataavailable = e => {
            audioChunks.push(e.data);
          };

          mediaRecorder.onstop = e => {
            statusEl.textContent = "Processing...";

            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = []; // reset for next recording

            // Convert Blob -> Base64
            const reader = new FileReader();
            reader.onloadend = () => {
              // e.g. "data:audio/wav;base64,SUQzBAAA..."
              const base64Data = reader.result.split(',')[1];
              // Send back to Python
              Streamlit.setComponentValue(base64Data);
              statusEl.textContent = "Recording complete! You can record again.";
            };
            reader.readAsDataURL(audioBlob);
          };

          startBtn.onclick = () => {
            audioChunks = [];
            mediaRecorder.start();
            statusEl.textContent = "Recording...";
          };

          stopBtn.onclick = () => {
            if (mediaRecorder.state !== "inactive") {
              mediaRecorder.stop();
              statusEl.textContent = "Stopped.";
            }
          };
        })
        .catch(err => {
          statusEl.textContent = "Microphone access denied or error: " + err;
          statusEl.style.color = "red";
          console.error(err);
        });
    })();
    </script>
    """,
)

# -------------------------------------------------------------------
# 2. Streamlit App: use the custom component, then decode & play audio
# -------------------------------------------------------------------
def main():
    st.title("Simple Browser Audio Recorder")

    # Insert our custom recorder component into the app
    base64_wav = recorder_component()

    st.write("Click Start/Stop above to record from your mic.")

    # If we receive a base64 string back, convert to raw bytes and let user play
    if base64_wav:
        st.write("Playback of your last recording:")
        wav_bytes = base64.b64decode(base64_wav)
        st.audio(wav_bytes, format="audio/wav")

    st.write("---")
    st.write("No external libraries, no WebRTC complexities. Just the MediaRecorder API in JS.")

if __name__ == "__main__":
    main()
