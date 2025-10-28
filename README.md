# OmniLearnAI: Multi-Source Learning Platform

**🚀 Learn from everywhere - An intelligent AI assistant that helps you learn from documents, web pages, and videos with complete citation grounding**

Built with FastAPI, Streamlit, smolagents, Qdrant, and Gemini 2.0 Flash

---

## 🌟 Features

**Tagline:** *"Learn from everywhere"*

- ✅ **Multi-Source Support**: Upload PDFs, DOCX, PPT, web URLs, and YouTube videos
- ✅ **Agentic AI**: Powered by smolagents with specialized tools for each content type
- ✅ **Complete Grounding**: Every answer includes page numbers/timestamps with source citations
- ✅ **Multi-Modal**: Understands text, images, audio, and video using Gemini 2.0 Flash
- ✅ **Vector Search**: Lightning-fast semantic search with Qdrant
- ✅ **Interactive UI**: Clean Streamlit interface with source selection and chat
- ✅ **Production Ready**: Docker-based deployment with proper separation of concerns

---

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Google AI API Key (Get from https://makersuite.google.com/app/apikey)

---

## 🚀 Quick Start

### 1. Clone/Download Project

Download all files and organize them according to the structure in `GroundRAG-Setup-Guide.pdf`

### 2. Configure API Key

```bash
# Backend
cd backend
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Frontend  
cd ../frontend
cp .env.example .env
```

### 3. Start with Docker (Recommended)

```bash
docker-compose up --build
```

Wait for all services to start, then access:
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000/docs
- **Qdrant**: http://localhost:6333/dashboard

### 4. Start Locally (Development)

**Terminal 1 - Qdrant:**
```bash
docker run -p 6333:6333 qdrant/qdrant:latest
```

**Terminal 2 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Terminal 3 - Frontend:**
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 📖 Usage

### Upload Sources

1. **Documents**: Upload PDF, DOCX, or PPT files
2. **Web Pages**: Enter any URL
3. **Videos**: Paste YouTube URL

### Chat with Sources

1. Select sources using checkboxes
2. Type your question
3. Get answers with complete citations

### Citation Format

Answers include inline citations like:
> "Linear algebra is the study of vectors [Source: Math_Textbook.pdf, Page: 5]"

Click/hover on citations to see source preview.

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Streamlit  │────▶│   FastAPI    │────▶│   Qdrant    │
│   Frontend  │     │   Backend    │     │  Vector DB  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  smolagents  │
                    │  + Gemini AI │
                    └──────────────┘
```

**Components:**
- **Frontend**: Streamlit (Python web UI)
- **Backend**: FastAPI (REST APIs)
- **Agent**: smolagents (Agentic orchestration)
- **Vector DB**: Qdrant (Semantic search)
- **LLM**: Gemini 2.0 Flash (Multi-modal AI)

---

## 📂 Project Structure

```
omnilearn/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # API entrypoint
│   │   ├── agents/      # smolagents setup
│   │   ├── api/         # REST endpoints
│   │   ├── services/    # Business logic
│   │   ├── models/      # Pydantic models
│   │   └── db/          # Qdrant client
│   └── requirements.txt
│
├── frontend/            # Streamlit frontend
│   ├── app.py          # Main UI
│   ├── components/     # UI components
│   └── services/       # API client
│
└── docker-compose.yml  # Multi-container setup
```

---

## 🔧 Configuration

### Environment Variables (backend/.env)

```bash
GOOGLE_API_KEY=your_key_here
QDRANT_HOST=localhost
QDRANT_PORT=6333
LLM_MODEL=gemini/gemini-2.0-flash
CHUNK_SIZE=1500
CHUNK_OVERLAP=200
```

### Environment Variables (frontend/.env)

```bash
BACKEND_API_URL=http://localhost:8000
```

---

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Upload Test Document

```bash
curl -X POST "http://localhost:8000/api/v1/upload/file" \
  -F "file=@test.pdf"
```

### Test Chat

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is linear algebra?", "source_ids": []}'
```

---

## 📚 Documentation

- **Setup Guide**: `OmniLearnAI-Setup-Guide.pdf` (Complete installation instructions)
- **Implementation Guide**: `OmniLearnAI-Implementation-Guide.pdf` (Full code documentation)
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

---

## 🤝 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | FastAPI | 0.115+ |
| Frontend Framework | Streamlit | 1.40+ |
| Agentic AI | smolagents | 0.3+ |
| LLM Provider | LiteLLM | 1.52+ |
| LLM Model | Gemini 2.0 Flash | Latest |
| Vector Database | Qdrant | 1.12+ |
| Document Processing | LangChain | 0.3+ |
| Embeddings | Google AI | text-embedding-004 |

---

## 🔑 Key Features Explained

### 1. Agentic AI with smolagents

Uses tool-calling agents that automatically select the right tool:
- `RetrieverTool`: Search documents
- `ImageUnderstandingTool`: Analyze images
- `AudioUnderstandingTool`: Analyze audio
- `YouTubeVideoUnderstandingTool`: Analyze videos

### 2. Complete Grounding

Every answer includes:
- Source document name
- Page number or timestamp
- Preview text from original source
- Confidence score

### 3. Multi-Modal Understanding

Gemini 2.0 Flash natively supports:
- Text documents
- Images (OCR, object detection)
- Audio files (transcription, analysis)
- YouTube videos (understanding, Q&A)

---

## 🛠️ Development

### Add New Tool

1. Create tool in `backend/app/agents/tools/`
2. Add to agent in `backend/app/agents/masa_agent.py`
3. Test with sample inputs

### Modify UI

1. Edit components in `frontend/components/`
2. Update `frontend/app.py` if needed
3. Streamlit auto-reloads

### Change LLM

Edit `backend/.env`:
```bash
LLM_MODEL=gpt-4o  # or claude-3-5-sonnet, etc.
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check `GOOGLE_API_KEY` in `.env`
- Verify Qdrant is running
- Check port 8000 is free

### Frontend connection error
- Verify backend is running at port 8000
- Check `BACKEND_API_URL` in frontend `.env`

### No citations in responses
- Ensure documents have page metadata
- Check chunking configuration
- Review agent system prompt

---

## 📦 Deployment

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment

1. **Qdrant**: Use Qdrant Cloud
2. **Backend**: Deploy to AWS/GCP/Azure
3. **Frontend**: Deploy to Streamlit Cloud
4. **Environment**: Set production env vars
5. **HTTPS**: Configure SSL certificates

---

## 🎯 Roadmap

- [ ] Advanced citation UI with hover previews
- [ ] Multi-user support with authentication
- [ ] Chat history persistence
- [ ] Export conversations
- [ ] Custom model fine-tuning
- [ ] Advanced filtering and search
- [ ] Mobile-responsive UI
- [ ] API rate limiting
- [ ] Monitoring dashboard

---

## 📄 License

Apache 2.0 License

---

## 🙏 Acknowledgments

- **MASA Project** (Kaggle): Reference implementation
- **HuggingFace**: smolagents framework
- **Google AI**: Gemini 2.0 Flash API
- **Qdrant**: Vector database
- **FastAPI**: Web framework
- **Streamlit**: UI framework

---

## 📞 Support

For issues or questions:
1. Check `OmniLearnAI-Setup-Guide.pdf`
2. Review troubleshooting section
3. Check API logs: `docker-compose logs -f`

---

**Built with ❤️ for learners everywhere - students, researchers, and knowledge workers**

*"Learn from everywhere"* - Start with `docker-compose up`! 🚀
