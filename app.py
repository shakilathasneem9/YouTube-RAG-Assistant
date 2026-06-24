import streamlit as st
import yt_dlp
import glob

from backend.transcribe import transcribe_audio
from backend.summarizer import summarize_text
from backend.qa import answer_question

from utils.chunker import chunk_text
from rag.embedder import create_embedding
from rag.vectorstore import add_document
from rag.retriever import retrieve


# ---------------------------
# SESSION STATE
# ---------------------------
if "ready" not in st.session_state:
    st.session_state["ready"] = False

if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""


# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="YouTube RAG Assistant",
    page_icon="🎙️"
)

st.title("🎙️ YouTube RAG Assistant")
st.write("Paste a YouTube URL, generate transcript, and ask questions.")


# ---------------------------
# DOWNLOAD AUDIO
# ---------------------------
def download_audio(video_url):

    try:
        if "youtube.com/shorts/" in video_url:
            video_id = video_url.split("/")[-1].split("?")[0]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "noplaylist": True,
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        files = glob.glob("audio.*")
        return files[0] if files else None

    except Exception as e:
        st.error(f"Download failed: {e}")
        return None


# ---------------------------
# INPUT URL
# ---------------------------
url = st.text_input("Paste YouTube URL")


# ---------------------------
# BUILD KNOWLEDGE BASE
# ---------------------------
if st.button("Generate Knowledge Base"):

    if not url:
        st.error("Please enter a YouTube URL.")
        st.stop()

    if "youtube.com" not in url and "youtu.be" not in url:
        st.error("Invalid YouTube URL.")
        st.stop()

    # Download audio
    with st.spinner("Downloading audio..."):
        audio_file = download_audio(url)

    if not audio_file:
        st.error("Audio download failed.")
        st.stop()

    st.write(f"Audio file created: {audio_file}")

    # Transcription
    with st.spinner("Transcribing..."):
        try:
            transcript = transcribe_audio(audio_file)
        except Exception as e:
            st.error(f"Transcription failed: {e}")
            st.stop()

    if not transcript or not transcript.strip():
        st.error("No speech detected.")
        st.stop()

    st.session_state["transcript"] = transcript

    # ---------------------------
    # CHUNK + EMBED + STORE
    # ---------------------------
    with st.spinner("Creating embeddings..."):
        chunks = chunk_text(transcript)

        stored_chunks = 0

        for chunk in chunks:
            text = chunk.get("text") if isinstance(chunk, dict) else chunk

            if not text or not text.strip():
                continue

            embedding = create_embedding(text)
            add_document(text, embedding)
            stored_chunks += 1

    st.write(f"Stored chunks: {stored_chunks}")

    # ---------------------------
    # SUMMARY
    # ---------------------------
    with st.spinner("Generating summary..."):
        summary = summarize_text(transcript[:8000])

    st.subheader("Summary")
    st.write(summary)

    st.session_state["ready"] = True

    with st.expander("Transcript"):
        st.write(transcript)


# ---------------------------
# Q&A SECTION
# ---------------------------
if st.session_state.get("ready", False):

    st.subheader("Ask Questions")

    question = st.text_input("Ask something about the video")

    if st.button("Ask"):

        if not question.strip():
            st.warning("Enter a question.")
            st.stop()

        try:
            contexts = retrieve(question)

            # 🔥 SAFE GUARD (IMPORTANT)
            if not contexts:
                st.error("No relevant context found. Rebuild knowledge base.")
                st.stop()

            context = "\n\n".join(contexts)

            answer = answer_question(question, context)

            st.subheader("Answer")
            st.write(answer)

            with st.expander("Retrieved Context"):
                st.write(context)

        except Exception as e:
            st.error(f"Q&A failed: {e}")