# OmniLearnAI - Project Structure & Organization

**Version:** 1.0  
**Last Updated:** October 2025  
**Tagline:** *"Learn from everywhere"*  
**Purpose:** Complete project organization reference

---

## Directory Structure

```
StudyAgent/
│
├── backend/                          # FastAPI Backend Service
│   ├── app/
│   │   ├── __init__.py              # Package initialization
│   │   ├── main.py                  # FastAPI app entry point
│   │   │
│   │   ├── agents/                  # Agentic AI Components
│   │   │   ├── __init__.py
│   │   │   ├── masa_agent.py        # Main agent orchestration
│   │   │   └── tools/               # Custom agent tools
│   │   │       ├── __init__.py
│   │   │       ├── retriever_tool.py      # Vector search tool
│   │   │       ├── image_tool.py          # Image analysis tool
│   │   │       ├── audio_tool.py          # Audio analysis tool
│   │   │       └── video_tool.py          # YouTube video tool
│   │   │
│   │   ├── api/                     # REST API Endpoints
│   │   │   ├── __init__.py
│   │   │   └── v1/                  # API version 1
│   │   │       ├── __init__.py
│   │   │       ├── upload.py        # File/URL upload endpoints
│   │   │       ├── chat.py          # Chat query endpoints
│   │   │       └── sources.py       # Source management endpoints
│   │   │
│   │   ├── config/                  # Configuration Management
│   │   │   ├── __init__.py
│   │   │   └── settings.py          # Application settings (env vars)
│   │   │
│   │   ├── db/                      # Database Clients
│   │   │   ├── __init__.py
│   │   │   └── qdrant_client.py     # Qdrant vector DB client
│   │   │
│   │   ├── models/                  # Data Models
│   │   │   ├── __init__.py
│   │   │   └── response_models.py   # Pydantic response models
│   │   │
│   │   ├── services/                # Business Logic Layer
│   │   │   ├── __init__.py
│   │   │   ├── ingestion_service.py    # Document processing
│   │   │   ├── chat_service.py         # Chat query handling
│   │   │   ├── session_manager.py      # Agent session management
│   │   │   ├── vector_service.py       # Vector DB operations
│   │   │   └── source_service.py       # Source CRUD operations
│   │   │
│   │   └── utils/                   # Utility Functions
│   │       └── __init__.py
│   │
│   ├── tests/                       # Unit & Integration Tests
│   │   └── (test files)
│   │
│   ├── .env                         # Environment variables (not in git)
│   ├── .env.example                 # Example environment file
│   ├── Dockerfile                   # Backend container definition
│   └── requirements.txt             # Python dependencies
│
├── frontend/                        # Streamlit Frontend Application
│   ├── components/                  # UI Components
│   │   ├── __init__.py
│   │   ├── upload_panel.py          # File/URL upload UI
│   │   ├── sources_panel.py         # Sources list & management UI
│   │   └── chat_panel.py            # Chat interface UI
│   │
│   ├── services/                    # Frontend Services
│   │   ├── __init__.py
│   │   └── api_client.py            # Backend API client
│   │
│   ├── app.py                       # Main Streamlit app
│   ├── .env                         # Frontend environment variables
│   ├── Dockerfile                   # Frontend container definition
│   └── requirements.txt             # Python dependencies
│
├── docs/                            # Documentation
│   ├── ARCHITECTURE.md              # System architecture
│   ├── DEVELOPER_GUIDE.md           # Developer onboarding guide
│   └── API_REFERENCE.md             # API documentation
│
├── utils/                           # Utility Scripts
│   ├── clear_old_videos.py          # Database cleanup script
│   ├── test_metadata.py             # Metadata testing script
│   └── CLEANUP_INSTRUCTIONS.md      # Cleanup guide
│
├── docker-compose.yml               # Multi-container orchestration
├── .gitignore                       # Git ignore rules
├── README.md                        # Project overview & quick start
├── PROJECT_STRUCTURE.md             # This file
└── OmniLearnAI-Setup-Guide.pdf      # Detailed setup guide

```

---

## Component Responsibilities

### Backend Components

#### 1. **main.py** - Application Entry Point
- Initializes FastAPI application
- Configures CORS middleware
- Registers API routers
- Handles startup/shutdown events
- Initializes Qdrant connection

#### 2. **agents/** - Agentic AI Layer
- **masa_agent.py**: Creates and configures smolagents agent
- **tools/**: Custom tools for different content types
  - Retriever: Searches vector database
  - Image: Analyzes images with Gemini
  - Audio: Processes audio files
  - Video: Analyzes YouTube videos

#### 3. **api/v1/** - REST API Endpoints
- **upload.py**: Handle file/URL uploads
  - POST /upload/file - Upload documents
  - POST /upload/url - Process web pages
  - POST /upload/video - Register YouTube videos
- **chat.py**: Handle chat queries
  - POST /chat - Process user questions
  - POST /chat/history - Get chat history
- **sources.py**: Manage uploaded sources
  - GET /sources - List all sources
  - DELETE /sources/{id} - Delete source
  - GET /sources/{id} - Get source details

#### 4. **services/** - Business Logic
- **ingestion_service.py**: Document processing pipeline
  - Load documents (PDF, DOCX, PPT)
  - Split into chunks
  - Generate embeddings
  - Store in vector database
- **chat_service.py**: Query processing
  - Session management
  - Agent execution with retry logic
  - Citation extraction
- **vector_service.py**: Vector database operations
  - Add documents
  - Semantic search
  - Delete by source
- **session_manager.py**: Agent session caching
  - Create/retrieve sessions
  - Maintain chat history
  - Cache agent instances

#### 5. **config/** - Configuration
- **settings.py**: Centralized configuration
  - Environment variables
  - API keys
  - Database settings
  - Model configurations

#### 6. **db/** - Database Clients
- **qdrant_client.py**: Qdrant operations
  - Initialize collections
  - CRUD operations
  - Search functionality

#### 7. **models/** - Data Models
- **response_models.py**: Pydantic models
  - Request/response schemas
  - Data validation
  - API documentation

### Frontend Components

#### 1. **app.py** - Main Application
- Streamlit page configuration
- Custom CSS styling
- Component orchestration
- Session state management

#### 2. **components/** - UI Components
- **upload_panel.py**: Upload interface
  - File upload widget
  - URL input fields
  - Upload progress indicators
- **sources_panel.py**: Source management
  - Source list display
  - Selection checkboxes
  - Delete buttons
  - Metadata display
- **chat_panel.py**: Chat interface
  - Message display
  - Citation formatting
  - Input field
  - Loading indicators

#### 3. **services/** - Frontend Services
- **api_client.py**: Backend communication
  - HTTP request handling
  - Error handling
  - Response parsing

---

## Data Flow

### 1. Document Upload Flow
```
User → upload_panel.py → api_client.py → upload.py → 
ingestion_service.py → vector_service.py → Qdrant
```

### 2. Chat Query Flow
```
User → chat_panel.py → api_client.py → chat.py → 
chat_service.py → session_manager.py → masa_agent.py → 
tools → vector_service.py → Qdrant → Gemini API
```

### 3. Source Management Flow
```
User → sources_panel.py → api_client.py → sources.py → 
source_service.py → qdrant_client.py → Qdrant
```

---

## Key Files Explained

### Backend

| File | Lines | Purpose | Key Functions |
|------|-------|---------|---------------|
| main.py | ~110 | App initialization | startup_event(), health_check() |
| masa_agent.py | ~110 | Agent setup | create_agent(), get_model() |
| ingestion_service.py | ~280 | Document processing | process_document(), process_web_url() |
| chat_service.py | ~140 | Query handling | process_query(), _run_agent_with_retry() |
| vector_service.py | ~200 | Vector operations | add_documents(), search(), search_all() |
| session_manager.py | ~120 | Session management | get_or_create_session() |
| qdrant_client.py | ~330 | Qdrant operations | init_qdrant(), upsert_documents() |

### Frontend

| File | Lines | Purpose | Key Functions |
|------|-------|---------|---------------|
| app.py | ~180 | Main UI | main(), custom CSS |
| upload_panel.py | ~110 | Upload UI | render_upload_panel() |
| sources_panel.py | ~160 | Sources UI | render_sources_panel() |
| chat_panel.py | ~130 | Chat UI | render_chat_panel() |
| api_client.py | ~160 | API client | upload_file(), chat(), get_sources() |

---

## Configuration Files

### Backend .env
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
EMBEDDING_MODEL=models/text-embedding-004
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend .env
```bash
BACKEND_API_URL=http://localhost:8000
```

### docker-compose.yml
- Orchestrates 3 services: qdrant, backend, frontend
- Defines networks and volumes
- Sets environment variables
- Configures port mappings

---

## Dependencies

### Backend (requirements.txt)
```
fastapi==0.115.0          # Web framework
uvicorn==0.32.0           # ASGI server
smolagents==0.3.4         # Agentic AI framework
litellm==1.52.5           # LLM provider abstraction
langchain==0.3.7          # Document processing
langchain-google-genai    # Google AI integration
qdrant-client==1.12.1     # Vector database client
python-multipart          # File upload support
pydantic==2.9.2           # Data validation
pydantic-settings         # Settings management
```

### Frontend (requirements.txt)
```
streamlit==1.40.1         # UI framework
requests==2.32.3          # HTTP client
python-dotenv==1.0.1      # Environment variables
```

---

## Environment Setup

### Development
1. Local Python virtual environments
2. Local Qdrant via Docker
3. Hot reload enabled
4. Debug logging

### Production
1. Docker containers for all services
2. Managed Qdrant (cloud or dedicated instance)
3. Production logging
4. Health monitoring

---

## Code Organization Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Layered Architecture**: API → Service → Database
3. **Dependency Injection**: Services receive dependencies
4. **Configuration Management**: Centralized in settings.py
5. **Error Handling**: Consistent error responses
6. **Logging**: Structured logging throughout
7. **Type Safety**: Type hints everywhere
8. **Documentation**: Docstrings for all public functions

---

## Testing Strategy

### Unit Tests
- Test individual functions
- Mock external dependencies
- Fast execution

### Integration Tests
- Test API endpoints
- Use test database
- Verify data flow

### Manual Testing
- UI functionality
- End-to-end workflows
- Error scenarios

---

## Deployment Architecture

### Docker Compose (Development/Staging)
```
┌─────────────┐
│   Qdrant    │ :6333
└─────────────┘
       ↑
       │
┌─────────────┐
│   Backend   │ :8000
└─────────────┘
       ↑
       │
┌─────────────┐
│  Frontend   │ :8501
└─────────────┘
```

### Production (Cloud)
```
┌─────────────┐
│  Load       │
│  Balancer   │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│ BE1 │ │ BE2 │  (Multiple backend instances)
└──┬──┘ └──┬──┘
   │       │
   └───┬───┘
       │
┌──────▼──────┐
│   Qdrant    │  (Managed/Cluster)
│   Cluster   │
└─────────────┘
```

---

## Maintenance & Operations

### Regular Tasks
- Monitor error logs
- Check API quota usage
- Verify disk space
- Update dependencies
- Backup Qdrant data

### Performance Monitoring
- Query response time
- Upload processing time
- API error rate
- Memory usage
- Disk usage

### Scaling Considerations
- Horizontal scaling: Multiple backend instances
- Vertical scaling: Increase resources
- Caching: Redis for sessions
- CDN: Static assets
- Database: Qdrant cluster

---

## Security Considerations

1. **API Keys**: Never commit to version control
2. **CORS**: Restrict origins in production
3. **Input Validation**: Validate all user inputs
4. **File Upload**: Limit size and types
5. **Rate Limiting**: Implement for production
6. **HTTPS**: Use SSL/TLS in production
7. **Authentication**: Add user auth for multi-user

---

## Future Enhancements

### Short-term
- Advanced citation UI
- Export conversations
- Multi-user support
- Chat history persistence

### Long-term
- Custom model fine-tuning
- Mobile app
- Voice interface
- Collaborative features
- Advanced analytics

---

## Resources

- **Documentation**: `/docs` folder
- **API Docs**: http://localhost:8000/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Logs**: `docker-compose logs -f`

---

## Getting Help

1. Check documentation in `/docs`
2. Review this structure guide
3. Check logs for errors
4. Consult API documentation
5. Ask team members

---

**Last Updated:** October 2025  
**Maintained By:** Development Team
