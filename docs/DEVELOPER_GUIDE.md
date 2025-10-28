# OmniLearnAI - Developer Guide

**Version:** 1.0  
**Last Updated:** October 2025  
**Tagline:** *"Learn from everywhere"*  
**Target Audience:** Developers joining the project

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Adding New Features](#adding-new-features)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Common Tasks](#common-tasks)

---

## Getting Started

### Prerequisites

```bash
# Required
- Python 3.11+
- Docker & Docker Compose
- Git
- VS Code (recommended)

# Optional
- Postman (API testing)
- Qdrant dashboard access
```

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd StudyAgent

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant:latest

# 5. Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 6. Frontend setup (new terminal)
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 7. Start frontend
streamlit run app.py
```

### Verify Setup

```bash
# Test backend health
curl http://localhost:8000/health

# Test Qdrant
curl http://localhost:6333/health

# Access frontend
# Open browser: http://localhost:8501
```

---

## Project Structure

```
StudyAgent/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── agents/            # Agentic AI components
│   │   │   ├── masa_agent.py  # Main agent setup
│   │   │   └── tools/         # Custom tools
│   │   │       ├── retriever_tool.py
│   │   │       ├── image_tool.py
│   │   │       ├── audio_tool.py
│   │   │       └── video_tool.py
│   │   ├── api/               # REST API endpoints
│   │   │   └── v1/
│   │   │       ├── upload.py  # Upload endpoints
│   │   │       ├── chat.py    # Chat endpoints
│   │   │       └── sources.py # Source management
│   │   ├── config/            # Configuration
│   │   │   └── settings.py    # App settings
│   │   ├── db/                # Database clients
│   │   │   └── qdrant_client.py
│   │   ├── models/            # Pydantic models
│   │   │   └── response_models.py
│   │   ├── services/          # Business logic
│   │   │   ├── ingestion_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── session_manager.py
│   │   │   ├── vector_service.py
│   │   │   └── source_service.py
│   │   └── utils/             # Utilities
│   ├── .env                   # Environment variables
│   ├── .env.example           # Example env file
│   ├── Dockerfile             # Backend container
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # Streamlit frontend
│   ├── components/            # UI components
│   │   ├── upload_panel.py
│   │   ├── sources_panel.py
│   │   └── chat_panel.py
│   ├── services/              # API client
│   │   └── api_client.py
│   ├── app.py                 # Main UI entry point
│   ├── .env                   # Environment variables
│   ├── Dockerfile             # Frontend container
│   └── requirements.txt       # Python dependencies
│
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # System architecture
│   ├── DEVELOPER_GUIDE.md     # This file
│   └── API_REFERENCE.md       # API documentation
│
├── utils/                     # Utility scripts
│   ├── clear_old_videos.py    # Cleanup script
│   └── test_metadata.py       # Testing script
│
├── docker-compose.yml         # Multi-container setup
├── .gitignore                 # Git ignore rules
└── README.md                  # Project overview
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow code style guidelines
- Add comments for complex logic
- Update documentation if needed

### 3. Test Locally

```bash
# Backend tests
cd backend
python -m pytest

# Manual testing
# - Test API endpoints
# - Test UI functionality
# - Check error handling
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
# Create pull request on GitHub
```

---

## Code Style Guidelines

### Python Style (PEP 8)

```python
"""
Module docstring explaining purpose.

This module handles document ingestion and processing.
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class IngestionService:
    """
    Service for processing and storing uploaded documents.
    
    This class handles document loading, chunking, embedding generation,
    and storage in the vector database.
    
    Attributes:
        text_splitter: LangChain text splitter instance
        vector_manager: Vector database manager
    """
    
    def __init__(self):
        """Initialize ingestion service with required components."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200
        )
        self.vector_manager = VectorStoreManager()
    
    async def process_document(
        self,
        file_path: str,
        source_name: str
    ) -> Dict[str, Any]:
        """
        Process uploaded document and store in vector database.
        
        This method performs the following steps:
        1. Load document using appropriate loader
        2. Split into chunks
        3. Generate embeddings
        4. Store in Qdrant
        
        Args:
            file_path: Absolute path to uploaded file
            source_name: Display name for the source
            
        Returns:
            Dict containing:
                - source_id: Unique identifier for the source
                - chunks_created: Number of chunks created
                
        Raises:
            ValueError: If file format is unsupported
            IOError: If file cannot be read
            
        Example:
            >>> result = await service.process_document(
            ...     "/tmp/file.pdf",
            ...     "Research Paper.pdf"
            ... )
            >>> print(result["chunks_created"])
            15
        """
        try:
            # Load document
            loader = self._get_loader(file_path)
            docs = loader.load()
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(docs)
            
            # Generate unique source ID
            source_id = str(uuid.uuid4())
            
            # Prepare documents with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                documents.append({
                    "content": chunk.page_content,
                    "metadata": {
                        "source_id": source_id,
                        "source_name": source_name,
                        "source_type": "document",
                        "chunk_index": i,
                        "page_number": chunk.metadata.get("page", 0)
                    }
                })
            
            # Store in vector database
            await self.vector_manager.add_documents(
                "documents",
                documents
            )
            
            logger.info(
                f"Processed document: {source_name} "
                f"({len(chunks)} chunks)"
            )
            
            return {
                "source_id": source_id,
                "chunks_created": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
```

### Key Principles

1. **Type Hints**: Always use type hints
2. **Docstrings**: Google-style docstrings for all public methods
3. **Comments**: Explain WHY, not WHAT
4. **Naming**: Descriptive names (no abbreviations)
5. **Line Length**: Max 100 characters
6. **Imports**: Organized (stdlib, third-party, local)

### Bad vs Good Examples

**❌ Bad:**
```python
def proc_doc(fp, sn):
    l = Loader(fp)
    d = l.load()
    c = splitter.split(d)
    return len(c)
```

**✅ Good:**
```python
async def process_document(
    self,
    file_path: str,
    source_name: str
) -> Dict[str, Any]:
    """Process uploaded document and store in vector database."""
    loader = self._get_loader(file_path)
    docs = loader.load()
    chunks = self.text_splitter.split_documents(docs)
    
    return {
        "source_id": str(uuid.uuid4()),
        "chunks_created": len(chunks)
    }
```

---

## Adding New Features

### Adding a New Tool

**1. Create tool file:**
```python
# backend/app/agents/tools/my_tool.py

"""
Custom tool for specific functionality.

This tool handles [describe purpose].
"""

from smolagents import Tool
import logging

logger = logging.getLogger(__name__)


class MyCustomTool(Tool):
    """
    Tool for [specific purpose].
    
    This tool is used by the agent to [describe when/why it's used].
    """
    
    name = "my_custom_tool"
    description = """
    Use this tool when you need to [describe use case].
    
    Args:
        input_param: Description of parameter
        
    Returns:
        Description of return value
    """
    inputs = {
        "input_param": {
            "type": "string",
            "description": "What this parameter does"
        }
    }
    output_type = "string"
    
    def forward(self, input_param: str) -> str:
        """
        Execute the tool logic.
        
        Args:
            input_param: Input parameter description
            
        Returns:
            Result of tool execution
        """
        try:
            # Tool logic here
            result = self._process(input_param)
            
            logger.info(f"Tool executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Tool error: {str(e)}")
            return f"Error: {str(e)}"
    
    def _process(self, input_param: str) -> str:
        """Private method for processing logic."""
        # Implementation
        pass
```

**2. Register tool in agent:**
```python
# backend/app/agents/masa_agent.py

from app.agents.tools.my_tool import MyCustomTool

def create_agent(vector_store_manager) -> ToolCallingAgent:
    """Create agent with all tools."""
    # ... existing tools ...
    my_tool = MyCustomTool()
    
    tools = [
        retriever_tool,
        image_tool,
        audio_tool,
        video_tool,
        my_tool,  # Add new tool
        final_answer_tool
    ]
    
    # ... rest of agent setup ...
```

**3. Test the tool:**
```python
# Test script
from app.agents.tools.my_tool import MyCustomTool

tool = MyCustomTool()
result = tool.forward("test input")
print(result)
```

### Adding a New API Endpoint

**1. Create endpoint:**
```python
# backend/app/api/v1/my_endpoint.py

"""
API endpoints for [feature name].

This module provides REST endpoints for [describe purpose].
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/my-endpoint")
async def my_endpoint(
    param1: str,
    param2: int
) -> Dict[str, Any]:
    """
    Endpoint description.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
        
    Returns:
        Dict containing result data
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        # Validate inputs
        if not param1:
            raise HTTPException(
                status_code=400,
                detail="param1 is required"
            )
        
        # Process request
        result = process_data(param1, param2)
        
        logger.info(f"Endpoint executed successfully")
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
```

**2. Register router:**
```python
# backend/app/main.py

from app.api.v1 import my_endpoint

app.include_router(
    my_endpoint.router,
    prefix="/api/v1",
    tags=["my-feature"]
)
```

**3. Test endpoint:**
```bash
curl -X POST "http://localhost:8000/api/v1/my-endpoint" \
  -H "Content-Type: application/json" \
  -d '{"param1": "test", "param2": 123}'
```

### Adding a Frontend Component

**1. Create component:**
```python
# frontend/components/my_component.py

"""
Custom UI component for [feature name].

This component provides [describe purpose].
"""

import streamlit as st
from typing import Dict, Any


def render_my_component(data: Dict[str, Any]) -> None:
    """
    Render custom component.
    
    Args:
        data: Data to display in component
    """
    st.markdown("### My Component")
    
    # Component logic
    with st.container():
        st.write(data.get("title", "No title"))
        
        if st.button("Action Button"):
            # Handle button click
            handle_action(data)


def handle_action(data: Dict[str, Any]) -> None:
    """Handle component action."""
    try:
        # Action logic
        result = process_action(data)
        st.success(f"Action completed: {result}")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

**2. Use in main app:**
```python
# frontend/app.py

from components.my_component import render_my_component

# In main app
if some_condition:
    render_my_component(data)
```

---

## Testing

### Manual Testing Checklist

**Upload Flow:**
- [ ] Upload PDF file
- [ ] Upload DOCX file
- [ ] Upload PPT file
- [ ] Upload web URL
- [ ] Upload YouTube video
- [ ] Verify metadata displays correctly
- [ ] Check sources list updates

**Chat Flow:**
- [ ] Select single source
- [ ] Select multiple sources
- [ ] Ask question
- [ ] Verify citations in response
- [ ] Test "Strictly Bound" mode
- [ ] Check error handling (503, 429)

**Source Management:**
- [ ] View sources list
- [ ] Delete source
- [ ] Refresh sources
- [ ] Verify source selection persists

### API Testing with Postman

**1. Health Check:**
```
GET http://localhost:8000/health
```

**2. Upload Document:**
```
POST http://localhost:8000/api/v1/upload/file
Body: form-data
  file: [select file]
```

**3. Chat Query:**
```
POST http://localhost:8000/api/v1/chat
Body: JSON
{
  "query": "What is machine learning?",
  "source_ids": ["uuid-here"],
  "chat_history": []
}
```

---

## Debugging

### Enable Debug Logging

```python
# backend/app/main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s - %(message)s'
)
```

### Common Debugging Scenarios

**1. Agent not calling tools:**
```python
# Add logging in masa_agent.py
logger.debug(f"Agent tools: {[t.name for t in tools]}")
logger.debug(f"Agent running with query: {query}")
```

**2. Vector search returns no results:**
```python
# Add logging in vector_service.py
logger.debug(f"Search query: {query}")
logger.debug(f"Search results: {len(results)}")
logger.debug(f"First result: {results[0] if results else 'None'}")
```

**3. Citations not extracted:**
```python
# Add logging in chat_service.py
logger.debug(f"Raw answer: {result}")
logger.debug(f"Extracted citations: {citations}")
```

### Using Python Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use VS Code debugger
# Set breakpoint in IDE
```

---

## Common Tasks

### Update Dependencies

```bash
# Backend
cd backend
pip install --upgrade package-name
pip freeze > requirements.txt

# Frontend
cd frontend
pip install --upgrade package-name
pip freeze > requirements.txt
```

### Clear Qdrant Data

```bash
# Delete all collections
curl -X DELETE http://localhost:6333/collections/documents
curl -X DELETE http://localhost:6333/collections/web_pages
curl -X DELETE http://localhost:6333/collections/videos
```

### View Qdrant Collections

```bash
# List collections
curl http://localhost:6333/collections

# Get collection info
curl http://localhost:6333/collections/documents
```

### Restart Services

```bash
# Docker
docker-compose restart backend
docker-compose restart frontend

# Local
# Ctrl+C and restart uvicorn/streamlit
```

### View Logs

```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Local
# Check terminal output
```

---

## Best Practices

1. **Always test locally** before pushing
2. **Write descriptive commit messages**
3. **Keep functions small** (< 50 lines)
4. **Use type hints** everywhere
5. **Add logging** for important operations
6. **Handle errors gracefully**
7. **Document complex logic**
8. **Follow existing patterns**
9. **Ask questions** if unsure
10. **Review your own code** before PR

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Streamlit Docs**: https://docs.streamlit.io
- **smolagents Docs**: https://huggingface.co/docs/smolagents
- **Qdrant Docs**: https://qdrant.tech/documentation
- **LangChain Docs**: https://python.langchain.com

---

## Getting Help

1. Check this guide
2. Review existing code
3. Check logs for errors
4. Ask team members
5. Consult official documentation

---

**Happy Coding! 🚀**
