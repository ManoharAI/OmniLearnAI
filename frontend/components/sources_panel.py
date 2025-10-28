"""
Sources panel component for displaying indexed sources
"""
import streamlit as st

def render_sources_panel():
    """Render the sources list panel"""
    
    if not st.session_state.sources:
        st.info("📭 No sources yet. Upload documents to get started!")
        return
    
    # Group sources by type
    documents = [s for s in st.session_state.sources if s.get("source_type") == "document"]
    web_pages = [s for s in st.session_state.sources if s.get("source_type") == "web_page"]
    videos = [s for s in st.session_state.sources if s.get("source_type") == "video"]
    
    # Display documents
    if documents:
        st.markdown(f"### 📄 Documents ({len(documents)})")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✓ Select All", key="sel_all_docs", use_container_width=True, type="secondary"):
                for doc in documents:
                    st.session_state.selected_sources.add(doc.get('source_id'))
                st.rerun()
        with col2:
            if st.button("✗ Clear All", key="clear_all_docs", use_container_width=True, type="secondary"):
                for doc in documents:
                    st.session_state.selected_sources.discard(doc.get('source_id'))
                st.rerun()
        
        st.markdown("")  # Spacing
        
        for source in documents:
            source_id = source.get('source_id')
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                is_selected = st.checkbox(
                    f"{source.get('source_name', 'Unknown')[:35]}",
                    value=source_id in st.session_state.selected_sources,
                    key=f"sel_doc_{source_id}"
                )
                if is_selected:
                    st.session_state.selected_sources.add(source_id)
                else:
                    st.session_state.selected_sources.discard(source_id)
            with col2:
                if st.button("🗑️", key=f"del_doc_{source_id}", help="Delete"):
                    delete_source(source_id, source.get('source_name'))
            st.caption(f"   {source.get('chunk_count', 0)} chunks")
        st.markdown("---")
    
    # Display web pages
    if web_pages:
        st.markdown(f"### 🌐 Web Pages ({len(web_pages)})")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✓ Select All", key="sel_all_web", use_container_width=True, type="secondary"):
                for page in web_pages:
                    st.session_state.selected_sources.add(page.get('source_id'))
                st.rerun()
        with col2:
            if st.button("✗ Clear All", key="clear_all_web", use_container_width=True, type="secondary"):
                for page in web_pages:
                    st.session_state.selected_sources.discard(page.get('source_id'))
                st.rerun()
        
        st.markdown("")  # Spacing
        
        for source in web_pages:
            source_id = source.get('source_id')
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                is_selected = st.checkbox(
                    f"{source.get('source_name', 'Unknown')[:35]}",
                    value=source_id in st.session_state.selected_sources,
                    key=f"sel_web_{source_id}"
                )
                if is_selected:
                    st.session_state.selected_sources.add(source_id)
                else:
                    st.session_state.selected_sources.discard(source_id)
            with col2:
                if st.button("🗑️", key=f"del_web_{source_id}", help="Delete"):
                    delete_source(source_id, source.get('source_name'))
            st.caption(f"   {source.get('chunk_count', 0)} chunks")
        st.markdown("---")
    
    # Display videos
    if videos:
        st.markdown(f"### 🎥 Videos ({len(videos)})")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✓ Select All", key="sel_all_vid", use_container_width=True, type="secondary"):
                for vid in videos:
                    st.session_state.selected_sources.add(vid.get('source_id'))
                st.rerun()
        with col2:
            if st.button("✗ Clear All", key="clear_all_vid", use_container_width=True, type="secondary"):
                for vid in videos:
                    st.session_state.selected_sources.discard(vid.get('source_id'))
                st.rerun()
        
        st.markdown("")  # Spacing
        
        for source in videos:
            source_id = source.get('source_id')
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                is_selected = st.checkbox(
                    f"{source.get('source_name', 'Unknown')[:35]}",
                    value=source_id in st.session_state.selected_sources,
                    key=f"sel_vid_{source_id}"
                )
                if is_selected:
                    st.session_state.selected_sources.add(source_id)
                else:
                    st.session_state.selected_sources.discard(source_id)
            with col2:
                if st.button("🗑️", key=f"del_vid_{source_id}", help="Delete"):
                    delete_source(source_id, source.get('source_name'))
            
            # Show channel and duration for videos
            channel = source.get('metadata', {}).get('channel', 'Unknown')
            duration = source.get('metadata', {}).get('duration', 'Unknown')
            st.caption(f"   📺 {channel} • ⏱️ {duration}")
        st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh Sources", use_container_width=True):
        try:
            sources_data = st.session_state.api_client.get_sources()
            if sources_data:
                st.session_state.sources = sources_data.get("sources", [])
                st.success("✅ Sources refreshed!")
                st.rerun()
        except Exception as e:
            st.error(f"Failed to refresh: {str(e)}")

def delete_source(source_id: str, source_name: str):
    """Delete a source from backend and UI"""
    with st.spinner(f"Deleting {source_name}..."):
        try:
            success = st.session_state.api_client.delete_source(source_id)
            if success:
                # Remove from session state
                st.session_state.sources = [
                    s for s in st.session_state.sources 
                    if s.get('source_id') != source_id
                ]
                st.session_state.selected_sources.discard(source_id)
                st.success(f"✅ Deleted: {source_name}")
                st.rerun()
            else:
                st.error("❌ Failed to delete source")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
