# 🎙️ YouTube RAG Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to analyze YouTube videos by generating transcripts, creating vector embeddings, producing summaries, and asking questions about video content using local and cloud-based Large Language Models (LLMs).

## 🚀 Features

* Download audio directly from YouTube videos and Shorts
* Transcribe audio using Faster Whisper
* Generate concise video summaries
* Create embeddings using Sentence Transformers
* Store and retrieve knowledge using FAISS vector search
* Ask questions about video content using RAG
* Support for both:

  * LM Studio (Local LLM)
  * Grok API (Cloud LLM)
* Interactive Streamlit user interface

---

## 🏗️ Tech Stack

### Frontend

* Streamlit

### Audio Processing

* yt-dlp
* FFmpeg
* Faster Whisper

### Embeddings & Vector Search

* Sentence Transformers (`all-MiniLM-L6-v2`)
* FAISS

### Large Language Models

* LM Studio (Local Inference)
* Grok API (xAI)

### Backend

* Python
* Requests
* Python Dotenv

---

## 📂 Project Structure

```text
youtube-rag-assistant/
│
├── app.py
│
├── backend/
│   ├── transcribe.py
│   ├── summarizer.py
│   ├── qa.py
│   └── llm.py
│
├── rag/
│   ├── embedder.py
│   ├── retriever.py
│   └── vectorstore.py
│
├── utils/
│   └── chunker.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### Step 1: Download Audio

The application downloads audio from a YouTube video using `yt-dlp`.

### Step 2: Speech-to-Text

Audio is transcribed using Faster Whisper.

### Step 3: Chunking

The transcript is split into smaller chunks for efficient retrieval.

### Step 4: Embedding Generation

Each chunk is converted into vector embeddings using:

```text
all-MiniLM-L6-v2
```

### Step 5: Vector Storage

Embeddings are stored in a FAISS vector database.

### Step 6: Retrieval

When a user asks a question:

* The question is embedded
* Similar transcript chunks are retrieved
* Retrieved context is passed to the selected LLM

### Step 7: Answer Generation

The answer is generated using either:

* LM Studio (local model)
* Grok API (cloud model)

---

## 🧠 Supported LLMs

### LM Studio

Local inference using models such as:

* Llama 3.2 3B Instruct
* Mistral
* Gemma
* Other OpenAI-compatible local models

Example configuration:

```env
LM_STUDIO_URL=http://127.0.0.1:1234/v1/chat/completions
LM_MODEL=llama-3.2-3b-instruct
```

---

### Grok API

Cloud-based inference using xAI's Grok models.

Example configuration:

```env
GROK_API_KEY=your_grok_api_key
GROK_MODEL=grok-beta
```

---

## 🔧 Installation

### Clone Repository

```bash
git clone <repository-url>
cd youtube-rag-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎬 FFmpeg Setup

Install FFmpeg and add its `bin` directory to your system PATH.

Verify installation:

```bash
ffmpeg -version
```

---

## ▶️ Running the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser automatically.

---

## 💡 Usage

1. Paste a YouTube video URL.
2. Click **Generate Knowledge Base**.
3. Wait for:

   * Audio download
   * Transcription
   * Embedding generation
   * Summary creation
4. Ask questions about the video.
5. Choose between:

   * LM Studio
   * Grok API

---

## 📌 Example Use Cases

* YouTube video summarization
* Podcast analysis
* Educational video Q&A
* Content research
* Knowledge extraction from long videos
* Video-based AI assistant

---

## 🔒 Environment Variables

Create a `.env` file:

```env
LM_STUDIO_URL=http://127.0.0.1:1234/v1/chat/completions
LM_MODEL=llama-3.2-3b-instruct

GROK_API_KEY=your_grok_api_key
GROK_MODEL=grok-beta
```

---

## 📈 Future Improvements

* Multi-video knowledge base
* Persistent chat history
* Streaming responses
* PDF export
* Video timestamp citations
* Hybrid search (semantic + keyword)
* Cloud deployment

---

## 👨‍💻 Author
shakila thasneem

Developed as a Retrieval-Augmented Generation (RAG) project using Streamlit, Faster Whisper, FAISS, LM Studio, and Grok API.

---

## ⭐ Acknowledgements

* Streamlit
* Faster Whisper
* Sentence Transformers
* FAISS
* LM Studio
* xAI Grok API
* yt-dlp
* FFmpeg

License

This project is created for educational and portfolio purposes.
