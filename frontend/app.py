import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Autonomous QA Agent",
    layout="wide"
)

st.title("🤖 Autonomous QA Agent")
st.markdown("Generate test cases and Selenium scripts from your project documentation")

if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'generated_scripts' not in st.session_state:
    st.session_state.generated_scripts = {}
if 'html_uploaded' not in st.session_state:
    st.session_state.html_uploaded = False
if 'kb_built' not in st.session_state:
    st.session_state.kb_built = False

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Upload")
    st.subheader("1. Upload Documentation")
    uploaded_docs = st.file_uploader(
        "Upload support documents (PDF, MD, TXT, JSON)",
        type=['pdf', 'md', 'txt', 'json'],
        accept_multiple_files=True,
        help="Upload product specs, UI guides, API docs, etc.",
        key="docs_uploader"
    )
    
    if uploaded_docs and st.button("Upload Documents"):
        with st.spinner("Uploading documents..."):
            files = [("files", (file.name, file.getvalue(), file.type)) 
                    for file in uploaded_docs]
            response = requests.post(f"{BACKEND_URL}/upload-documents", files=files)        
            if response.status_code == 200:
                st.success("✅ Documents uploaded successfully!")
            else:
                st.error("❌ Failed to upload documents")

    st.subheader("2. Build Knowledge Base")
    if st.button("Build Knowledge Base"):
        with st.spinner("Building knowledge base..."):
            response = requests.post(f"{BACKEND_URL}/build-knowledge-base")
            if response.status_code == 200:
                st.success("✅ Knowledge base built successfully!")
                st.session_state.kb_built = True
            else:
                st.error("❌ Failed to build knowledge base")
    st.divider()
    st.subheader("3. Upload HTML File")
    uploaded_html = st.file_uploader(
        "Upload HTML file",
        type=['html'],
        help="Upload the HTML file for accurate selector extraction",
        key="html_uploader"
    )
    if uploaded_html and st.button("Upload HTML"):
        with st.spinner("Uploading HTML file..."):
            files = [("file", (uploaded_html.name, uploaded_html.getvalue(), "text/html"))]
            response = requests.post(f"{BACKEND_URL}/upload-html", files=files)    
            if response.status_code == 200:
                st.success("✅ HTML file uploaded successfully!")
                st.session_state.html_uploaded = True
            else:
                st.error("❌ Failed to upload HTML file")
    st.divider()
    st.subheader("Status")
    st.write(f"📚 Knowledge Base: {'✅ Built' if st.session_state.kb_built else '❌ Not Built'}")
    st.write(f"📄 HTML File: {'✅ Uploaded' if st.session_state.html_uploaded else '❌ Not Uploaded'}")

tab1, tab2 = st.tabs(["Test Case Generation", "Script Generation"])
with tab1:
    st.header("Generate Test Cases")
    if not st.session_state.kb_built:
        st.warning("⚠️ Please upload documents and build the knowledge base first!")
    query = st.text_area(
        "Enter your test generation query:",
        placeholder="e.g., Generate all positive and negative test cases for the discount code feature...",
        height=100
    )
    if st.button("Generate Test Cases", type="primary", disabled=not st.session_state.kb_built):
        if not query:
            st.warning("Please enter a query")
        else:
            with st.spinner("Generating test cases..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate-test-cases",
                    params={"query": query}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.test_cases = data.get("test_cases", [])
                    st.success(f"✅ Generated {len(st.session_state.test_cases)} test cases!")
                else:
                    st.error("❌ Failed to generate test cases")

    if st.session_state.test_cases:
        st.header("Generated Test Cases")
        
        for i, test_case in enumerate(st.session_state.test_cases):
            with st.expander(f"🧪 {test_case.get('test_id', f'TC-{i+1:03d}')} - {test_case.get('feature', 'Feature')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(test_case.get('feature', 'Feature'))
                    st.write(f"**Scenario:** {test_case.get('test_scenario', 'N/A')}")
                    
                    st.write("**Test Steps:**")
                    for j, step in enumerate(test_case.get('test_steps', []), 1):
                        st.write(f"{j}. {step}")
                    st.write(f"**Expected Result:** {test_case.get('expected_result', 'N/A')}")
                    st.write(f"**Type:** {test_case.get('test_type', 'N/A')}")
                    st.write(f"**Source:** {test_case.get('grounded_in', 'N/A')}")
                
                with col2:
                    if not st.session_state.html_uploaded:
                        st.warning("⚠️ Upload HTML file first")
                    if st.button("Generate Script", key=f"script_{i}", disabled=not st.session_state.html_uploaded):
                        with st.spinner("Generating Selenium script..."):
                            script_response = requests.post(
                                f"{BACKEND_URL}/generate-script",
                                json=test_case
                            )
                            if script_response.status_code == 200:
                                script_data = script_response.json()
                                st.session_state.generated_scripts[test_case.get('test_id', f'TC-{i+1:03d}')] = script_data.get('script', '')
                                st.success("✅ Script generated!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to generate script")

with tab2:
    st.header("Generated Selenium Scripts")
    if not st.session_state.generated_scripts:
        st.info("ℹ️ No scripts generated yet. Generate test cases first, upload HTML, then click 'Generate Script' buttons.")
    else:
        for test_id, script in st.session_state.generated_scripts.items():
            with st.expander(f"📜 Script for {test_id}", expanded=True):
                st.code(script, language='python')
                
                # Download button
                st.download_button(
                    label=f"📥 Download {test_id}.py",
                    data=script,
                    file_name=f"{test_id}.py",
                    mime="text/x-python",
                    key=f"download_{test_id}"
                )