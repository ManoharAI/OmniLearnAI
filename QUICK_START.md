# OmniLearnAI - Quick Start Guide

**Tagline:** *"Learn from everywhere"* 🌐

Get started with OmniLearnAI in 5 minutes!

---

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- Docker & Docker Compose installed
- Google AI API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Steps

**1. Configure API Key**
```bash
# Backend
cd backend
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Frontend
cd ../frontend
cp .env.example .env
```

**2. Start All Services**
```bash
# From project root
docker-compose up --build
```

**3. Access the Application**
- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs
- **Qdrant Dashboard:** http://localhost:6333/dashboard

**4. Start Learning!**
- Upload a PDF document
- Add a YouTube video URL
- Paste a web page URL
- Ask questions and get cited answers!

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.11+
- Docker (for Qdrant)
- Google AI API Key

### Backend Setup
```bash
# 1. Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant:latest

# 2. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env and add GOOGLE_API_KEY

# 4. Start backend
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
# In new terminal
cd frontend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env

# Start frontend
streamlit run app.py
```

---

## 📚 First Steps

### 1. Upload Your First Source

**Option A: Document**
- Click "📄 Add Document"
- Upload a PDF, DOCX, or PPT file
- Wait for processing

**Option B: YouTube Video**
- Click "🎥 Add YouTube Video"
- Paste video URL
- Get instant title and metadata

**Option C: Web Page**
- Click "🌐 Add Web Page"
- Paste URL
- Content extracted automatically

### 2. Ask Your First Question

- Select sources from sidebar
- Type your question
- Get AI-powered answer with citations!

**Example:**
```
Question: "What are the main topics covered?"
Answer: "The document covers three main topics: 
1. Machine Learning [Source: ML_Guide.pdf, Page: 5]
2. Deep Learning [Source: ML_Guide.pdf, Page: 12]
3. Neural Networks [Source: ML_Guide.pdf, Page: 18]"
```

---

## 🎯 Key Features

### Multi-Source Learning
- ✅ PDFs, DOCX, PPT
- ✅ YouTube videos
- ✅ Web pages
- ✅ All in one place!

### AI-Powered Insights
- ✅ Natural language questions
- ✅ Intelligent answers
- ✅ Context-aware responses

### Complete Citations
- ✅ Page numbers for documents
- ✅ Timestamps for videos
- ✅ Source references for web pages

### Multi-Modal Understanding
- ✅ Text extraction
- ✅ Image analysis
- ✅ Video understanding
- ✅ Audio transcription

---

## 🔧 Configuration

### Backend (.env)
```bash
# Required
GOOGLE_API_KEY=your_key_here
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Optional (with defaults)
LLM_MODEL=gemini/gemini-2.0-flash
LLM_TEMPERATURE=0.1
CHUNK_SIZE=1500
CHUNK_OVERLAP=200
```

### Frontend (.env)
```bash
BACKEND_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Qdrant is running
curl http://localhost:6333/health

# Check API key is set
cat backend/.env | grep GOOGLE_API_KEY
```

### Frontend connection error
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check frontend .env
cat frontend/.env
```

### 503 Service Unavailable
- This is Google's Gemini API being temporarily overloaded
- System will auto-retry 3 times
- Wait 1-2 minutes and try again

---

## 📖 Learn More

- **Full Documentation:** See `docs/` folder
- **Architecture:** Read `docs/ARCHITECTURE.md`
- **Developer Guide:** Read `docs/DEVELOPER_GUIDE.md`
- **Setup Guide:** See `OmniLearnAI-Setup-Guide.pdf`

---

## 💡 Tips

1. **Select Relevant Sources:** Only select sources related to your question
2. **Be Specific:** Ask specific questions for better answers
3. **Check Citations:** Click citations to see source context
4. **Upload Quality Content:** Better sources = better answers
5. **Use "Strictly Bound":** Add "strictly bound" to your question to only use uploaded sources

---

## 🎓 Example Use Cases

### For Students
```
Upload: Lecture notes, textbook PDFs, course videos
Ask: "Explain the concept of X from my notes"
Get: Cited explanations from your materials
```

### For Researchers
```
Upload: Research papers, articles, conference videos
Ask: "What are the key findings about Y?"
Get: Synthesized insights with citations
```

### For Professionals
```
Upload: Documentation, tutorials, training videos
Ask: "How do I implement Z?"
Get: Step-by-step guidance with references
```

---

## 🚀 Next Steps

1. ✅ Start the application
2. ✅ Upload your first source
3. ✅ Ask a question
4. ✅ Explore more features
5. ✅ Read full documentation

---

## 📞 Need Help?

1. Check `docs/` folder for detailed guides
2. Review troubleshooting section above
3. Check logs: `docker-compose logs -f`
4. Read `PROJECT_OVERVIEW.md` for project details

---

**OmniLearnAI - Learn from everywhere** 🌐

*Ready to start learning? Run `docker-compose up` and visit http://localhost:8501!*

---

**Version:** 1.0  
**Last Updated:** October 2025
