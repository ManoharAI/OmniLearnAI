"""
Upload panel component for Streamlit
"""
import streamlit as st

def render_upload_panel():
    """Render the upload panel UI"""

    # File uploader
    st.markdown("#### 📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "pptx"],
        help="Upload PDF, Word, or PowerPoint files",
        key="file_uploader"
    )

    if uploaded_file:
        if st.button("Process Document", key="process_doc"):
            with st.spinner("Processing document..."):
                try:
                    response = st.session_state.api_client.upload_file(uploaded_file)
                    if response:
                        if response.get('status') == 'already_exists':
                            st.warning(f"⚠️ {response.get('message', 'Document already exists')}")
                        else:
                            st.success(f"✅ Uploaded: {response['filename']} ({response.get('chunks_created', 0)} chunks)")
                            # Refresh sources
                            sources_data = st.session_state.api_client.get_sources()
                            if sources_data:
                                st.session_state.sources = sources_data.get("sources", [])
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    st.markdown("---")

    # URL input
    st.markdown("#### 🌐 Add Web Page")
    web_url = st.text_input(
        "Enter URL",
        placeholder="https://example.com/article",
        key="web_url"
    )

    if web_url and st.button("Process URL", key="process_url"):
        with st.spinner("Processing web page..."):
            try:
                response = st.session_state.api_client.upload_url(web_url)
                if response:
                    if response.get('status') == 'already_exists':
                        st.warning(f"⚠️ {response.get('message', 'URL already exists')}")
                    else:
                        # Get page title from response
                        metadata = response.get("metadata", {})
                        page_title = metadata.get("page_title", web_url)
                        chunks = response.get('chunks_created', 0)
                        
                        st.success(f"✅ Added: {page_title}")
                        st.info(f"📄 {chunks} chunks created")
                        
                        # Refresh sources
                        sources_data = st.session_state.api_client.get_sources()
                        if sources_data:
                            st.session_state.sources = sources_data.get("sources", [])
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    st.markdown("---")

    # Video URL input
    st.markdown("#### 🎥 Add YouTube Video")
    video_url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://youtube.com/watch?v=...",
        key="video_url"
    )

    if video_url and st.button("Process Video", key="process_video"):
        with st.spinner("Processing video..."):
            try:
                response = st.session_state.api_client.upload_video(video_url)
                if response:
                    # Get metadata from response
                    metadata = response.get("metadata", {})
                    title = metadata.get("title", "Unknown")
                    channel = metadata.get("channel", "Unknown")
                    duration = metadata.get("duration", "Unknown")
                    
                    st.success(f"✅ Added: {title}")
                    st.info(f"📺 {channel} • ⏱️ {duration}")
                    
                    # Refresh sources to get updated list
                    sources_data = st.session_state.api_client.get_sources()
                    if sources_data:
                        st.session_state.sources = sources_data.get("sources", [])
                    
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    st.markdown("---")
    
    # Upload tips
    st.info("""
    💡 **Tips:**
    - Supported formats: PDF, DOCX, PPTX
    - Web pages are automatically scraped
    - YouTube videos can be analyzed
    - Duplicate sources are automatically detected
    """)
