# AI Study Assistant 📚

Turn any lecture video or recording into study notes — a title, summary, action items, key decisions, open questions, and a chat you can ask follow-up questions in.

## What it does

1. **Input** — paste a YouTube link or point to a local video/audio file
2. **Transcription** — a local Whisper model converts speech to text
3. **Understanding** — an LLM (Groq) reads the transcript and generates:
   - A title
   - A summary
   - Action items
   - Key decisions
   - Open questions
4. **Study chat** — a retrieval-based (RAG) chat, grounded only in that transcript, so you can ask follow-up questions
5. **Export** — download your notes as `.txt`, Word (`.docx`), or PDF

## Tech stack

| Area | Tools |
|---|---|
| Audio/video acquisition | `yt-dlp`, `pydub`, `ffmpeg` |
| Speech-to-text | OpenAI Whisper (runs locally) |
| LLM orchestration | LangChain + Groq API |
| RAG / vector search | ChromaDB, HuggingFace embeddings |
| UI | Streamlit |
| Export | `python-docx`, `fpdf2` |

## Project structure

```
AI Agent/
├── app.py                  # Streamlit UI
├── main.py                 # CLI entry point
├── core/
│   ├── transcriber.py      # Whisper transcription
│   ├── summarizer.py       # Title + summary generation
│   ├── extractor.py        # Action items / decisions / questions
│   ├── rag_engine.py       # Study chat (RAG)
│   └── vector_store.py     # ChromaDB vector store
├── utils/
│   └── audio_processor.py  # YouTube download + audio chunking
└── Requirements.txt
```

## Setup

1. Clone the repo:
   ```
   git clone https://github.com/RathoreRakshita21/ai-study-agent.git
   cd ai-study-agent
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1        # Windows PowerShell
   pip install -r Requirements.txt
   ```

3. Install [FFmpeg](https://ffmpeg.org/) and add it to your PATH (required by `pydub`/`yt-dlp`).

4. Install [Deno](https://deno.land/) (used by `yt-dlp` to solve YouTube's JS challenge) and add it to your PATH.

5. Create a `.env` file in the project root with your Groq API key:
   ```
   GROQ_API_KEY=your_key_here
   ```
   Get a free key at [console.groq.com/keys](https://console.groq.com/keys).

6. (If downloading from YouTube fails with a "not a bot" error) export your browser's YouTube cookies to `www.youtube.com_cookies.txt` in the project root, using a browser extension like *Get cookies.txt LOCALLY*.

## Running it

**Web UI (recommended):**
```
streamlit run app.py
```

**CLI:**
```
python main.py
```

## Notable engineering decisions

- **Switched LLM provider from Mistral to Groq** — Mistral's free tier only allows 1 request/second, which the pipeline's multiple sequential LLM calls (title, summary, extraction, chat) exceeded. Groq's free tier is more generous and better suited to this workload.
- **Retry + backoff on every LLM call** — using `tenacity`, so a rate-limit response is retried automatically instead of crashing the pipeline.
- **YouTube bot-detection workaround** — downloads authenticate using exported browser cookies, and `yt-dlp` uses Deno as a JavaScript runtime to solve YouTube's anti-bot challenge.

## Roadmap

- [ ] Support multiple videos / playlists in one study set
- [ ] Auto-generate a quiz from the transcript
- [ ] Cache transcripts so re-processing the same video is instant
- [ ] Public deployment (Streamlit Community Cloud)
