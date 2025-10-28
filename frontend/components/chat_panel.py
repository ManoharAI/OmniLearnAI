"""
Chat panel component for Streamlit
"""
import streamlit as st
import re

def format_message_with_citations(content: str, citations: list) -> str:
    """Convert [Source: X, Page: Y] to inline citation symbols with tooltips"""
    if not citations:
        return content
    
    # Replace [Source: filename, Page: X] with superscript numbers
    citation_pattern = r'\[Source: ([^,]+), (?:Page|Time): ([^\]]+)\]'
    
    def replace_citation(match):
        source_name = match.group(1).strip()
        location = match.group(2).strip()
        
        # Find citation number
        for i, cit in enumerate(citations, 1):
            if source_name in cit.get('source_name', ''):
                # Create tooltip HTML
                tooltip = f"{source_name}, {location}"
                return f'<sup><span title="{tooltip}" style="color: #1a73e8; cursor: help; font-weight: bold;">[{i}]</span></sup>'
        
        return match.group(0)
    
    formatted_content = re.sub(citation_pattern, replace_citation, content)
    return formatted_content

def render_chat_panel():
    """Render the chat interface"""

    # Show selected sources
    if st.session_state.selected_sources:
        selected_count = len(st.session_state.selected_sources)
        st.success(f"✅ Chatting with **{selected_count}** selected source{'s' if selected_count > 1 else ''}")
    elif st.session_state.sources:
        st.warning("⚠️ Please select at least one source from the sidebar to start chatting!")
    else:
        st.info("📤 Upload sources first to start chatting!")

    st.markdown("---")

    # Display chat history
    chat_container = st.container()

    with chat_container:
        if not st.session_state.chat_history:
            st.info("👋 Hello! I'm GroundRAG. Upload some sources and ask me questions. "
                   "I'll provide answers with complete citations!")

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                # Display message content with inline citations
                citations = message.get("citations", [])
                formatted_content = format_message_with_citations(message["content"], citations)
                st.markdown(formatted_content, unsafe_allow_html=True)

                # Display processing time for assistant messages
                if message["role"] == "assistant" and message.get("processing_time"):
                    st.caption(f"⏱️ Response time: {message['processing_time']:.2f}s")

                # Display citations if available
                if citations:
                    with st.expander("📎 View All Citations"):
                        for citation in citations:
                            st.markdown(
                                f"**[{citation['citation_id']}] {citation['source_name']}** "
                                f"- {citation['location']}"
                            )
                            if citation.get('preview_text'):
                                st.caption(f"_{citation['preview_text'][:200]}..._")

    # Chat input
    user_query = st.chat_input(
        "Ask a question about your sources...",
        key="chat_input"
    )

    if user_query:
        # Check if sources are selected
        if not st.session_state.selected_sources:
            st.error("❌ Please select at least one source before asking questions!")
            return

        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_query
        })

        # Get response from API
        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.api_client.chat(
                    query=user_query,
                    source_ids=list(st.session_state.selected_sources),
                    chat_history=[]  # Backend manages history per session
                )

                # Add assistant response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "citations": response.get("citations", []),
                    "processing_time": response.get("processing_time", 0)
                })

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"I apologize, but I encountered an error: {str(e)}",
                    "citations": []
                })

        # Rerun to update UI
        st.rerun()

    # Clear chat button
    if st.session_state.chat_history:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
