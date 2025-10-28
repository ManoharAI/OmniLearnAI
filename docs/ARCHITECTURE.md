# OmniLearnAI - System Architecture

**Version:** 1.0  
**Last Updated:** October 2025  
**Tagline:** *"Learn from everywhere"*

---

## System Overview

OmniLearnAI is a Multi-Source Learning Platform that enables users to learn from documents, web pages, and videos using AI with proper citations. The platform helps learners access knowledge from any source with intelligent AI assistance and complete citation grounding.

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                    (Streamlit Frontend)                         │
│  - Upload Panel  - Sources Panel  - Chat Panel                 │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend API Layer                          │
│                        (FastAPI)                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Upload  │  │  Chat    │  │  Sources │  │  Health  │      │
│  │  Routes  │  │  Routes  │  │  Routes  │  │  Routes  │      │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘  └──────────┘      │
└────────┼────────────┼─────────────┼─────────────────────────────┘
         │            │             │
         ▼            ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │   Ingestion    │  │  Chat Service  │  │  Source Service  │ │
│  │    Service     │  │                │  │                  │ │
│  │  - Document    │  │  - Query       │  │  - List sources  │ │
│  │  - Web URL     │  │    processing  │  │  - Delete source │ │
│  │  - Video       │  │  - Session mgmt│  │                  │ │
│  └────────┬───────┘  └───────┬────────┘  └──────────────────┘ │
└───────────┼──────────────────┼──────────────────────────────────┘
            │                  │
            ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent & Tools Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MASA Agent (smolagents)                     │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │ Retriever  │  │   Image    │  │   Audio    │        │  │
│  │  │    Tool    │  │    Tool    │  │    Tool    │        │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  │  ┌────────────┐  ┌────────────┐                        │  │
│  │  │   Video    │  │   Final    │                        │  │
│  │  │    Tool    │  │   Answer   │                        │  │
│  │  └────────────┘  └────────────┘                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data & Storage Layer                         │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │  Qdrant Vector   │              │   Gemini 2.0     │        │
│  │     Database     │              │      Flash       │        │
│  │  - documents     │              │   (via LiteLLM)  │        │
│  │  - web_pages     │              │                  │        │
│  │  - videos        │              │                  │        │
│  └──────────────────┘              └──────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit 1.40+ | User interface |
| Backend | FastAPI 0.115+ | REST API server |
| Agent Framework | smolagents 0.3+ | Agentic orchestration |
| LLM | Gemini 2.0 Flash | Language model |
| Vector DB | Qdrant 1.12+ | Semantic search |
| Embeddings | Google AI text-embedding-004 | Document embeddings |
| Document Processing | LangChain 0.3+ | Text splitting, loading |
| Containerization | Docker & Docker Compose | Deployment |

---

## Data Flow

### Document Upload Flow

```
1. User uploads file via Streamlit
2. Frontend sends POST to /api/v1/upload/file
3. Backend IngestionService:
   a. Loads document using LangChain loaders
   b. Splits into chunks (1500 chars, 200 overlap)
   c. Generates embeddings via Google AI
   d. Stores in Qdrant vector database
4. Returns source_id and metadata to frontend
5. Frontend refreshes sources list
```

### Chat Query Flow

```
1. User types question and selects sources
2. Frontend sends POST to /api/v1/chat
3. Backend ChatService:
   a. Gets/creates session for source combination
   b. Initializes MASA agent with tools
   c. Agent autonomously:
      - Calls retriever tool to search vector DB
      - Analyzes results
      - Calls specialized tools if needed
      - Formulates answer with citations
   d. Extracts citations from answer
   e. Stores in session history
4. Returns answer with citations to frontend
5. Frontend displays formatted response
```

---

## Key Design Decisions

### 1. Why smolagents?
- Lightweight and fast
- Native tool-calling support
- Works with any LLM via LiteLLM
- Easy to add custom tools

### 2. Why Qdrant?
- Fast semantic search
- Easy Docker deployment
- Good Python client
- Supports metadata filtering

### 3. Why Gemini 2.0 Flash?
- Multi-modal (text, image, audio, video)
- Fast response times
- Cost-effective
- Good citation quality

### 4. Session Management
- Cache agent instances per source combination
- Agent initialization is expensive (~3-5 seconds)
- Improves response time significantly

### 5. Retry Strategy
- 3 retries with exponential backoff (2s, 4s, 8s)
- Handles 503 (overloaded) and 429 (rate limit) errors
- Improves reliability

### 6. Chunking Strategy
- 1500 characters with 200 overlap
- Balances context vs. precision
- Works well for most document types

---

## Security Considerations

1. **API Keys**: Stored in .env files (not in version control)
2. **CORS**: Configured for frontend access only
3. **Input Validation**: All API endpoints validate inputs
4. **File Upload**: Limited to specific formats and sizes
5. **Rate Limiting**: Should be implemented for production

---

## Scalability

### Current Limits
- Single backend instance
- In-memory session storage
- No load balancing

### Scaling Strategy
1. **Horizontal Scaling**: Deploy multiple backend instances
2. **Session Storage**: Move to Redis
3. **Qdrant Cluster**: Distributed vector search
4. **Load Balancer**: Distribute requests
5. **Caching**: Add Redis for frequently accessed data

---

## Monitoring & Observability

### Key Metrics
- Query response time (target: < 5s)
- Upload processing time (target: < 30s)
- API error rate (target: < 1%)
- Memory usage
- Disk usage (Qdrant)

### Logging
- Structured logging with timestamps
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized log aggregation recommended

---

## Future Enhancements

1. Multi-user support with authentication
2. Chat history persistence
3. Advanced citation UI
4. Export conversations
5. Mobile-responsive design
6. API rate limiting
7. Monitoring dashboard
8. Multi-language support
