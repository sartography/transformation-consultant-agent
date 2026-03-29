"""
Streamlit GUI for the Transformation Consultant Agent.

Provides a web interface for analyzing business process transcripts,
generating BPMN diagrams, and producing optimization recommendations.
"""

import streamlit as st
import logging
import queue
import threading
import time
from pathlib import Path

from src.main import create_full_pipeline

st.set_page_config(
    page_title="Transformation Consultant",
    page_icon="\u2699\ufe0f",
    layout="wide",
)

SAMPLE_DIR = Path("data/sample-transcripts")


# --- Logging capture for pipeline progress ---

class QueueHandler(logging.Handler):
    """Logging handler that pushes formatted messages to a queue."""

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(self.format(record))


def run_pipeline(api_key, transcript, business_context, log_queue, result_container):
    """Run the transformation pipeline in a background thread."""
    handler = QueueHandler(log_queue)
    handler.setLevel(logging.INFO)
    pipeline_logger = logging.getLogger("src.pipeline")
    pipeline_logger.addHandler(handler)
    pipeline_logger.setLevel(logging.INFO)

    try:
        pipeline = create_full_pipeline(api_key=api_key)
        if business_context:
            pipeline.component_configs[2]["business_context"] = business_context
        result = pipeline.execute(transcript)
        result_container["result"] = result
    except Exception as e:
        result_container["error"] = str(e)
    finally:
        pipeline_logger.removeHandler(handler)


# --- Sidebar ---

st.sidebar.title("Configuration")

api_key = st.sidebar.text_input("Anthropic API Key", type="password")

sample_files = sorted(SAMPLE_DIR.glob("*.txt")) if SAMPLE_DIR.exists() else []
sample_options = ["-- None --"] + [f.stem for f in sample_files]
sample_choice = st.sidebar.selectbox("Load sample transcript", sample_options)

business_context = st.sidebar.text_area(
    "Business context (optional)",
    placeholder="e.g. Manufacturing industry, $50M revenue, 200 employees",
    height=100,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**About**: Analyzes business process transcripts, generates BPMN 2.0 "
    "diagrams, and provides automation recommendations with ROI analysis."
)

# --- Main area ---

st.title("Transformation Consultant")
st.markdown("Upload or paste a business process transcript to get started.")

# Input tabs
tab_upload, tab_paste, tab_sample = st.tabs(["Upload file", "Paste text", "Sample transcript"])

with tab_upload:
    uploaded_file = st.file_uploader("Upload a transcript (.txt)", type=["txt"])

with tab_paste:
    pasted_text = st.text_area("Paste transcript text", height=300)

with tab_sample:
    if sample_choice != "-- None --":
        sample_path = SAMPLE_DIR / f"{sample_choice}.txt"
        sample_text = sample_path.read_text(encoding="utf-8") if sample_path.exists() else ""
        st.text_area("Sample transcript (read-only)", value=sample_text, height=300, disabled=True)
    else:
        sample_text = ""
        st.info("Select a sample transcript from the sidebar.")

# Resolve transcript input (priority: upload > paste > sample)
transcript = None
if uploaded_file is not None:
    transcript = uploaded_file.getvalue().decode("utf-8")
elif pasted_text.strip():
    transcript = pasted_text.strip()
elif sample_choice != "-- None --" and sample_text:
    transcript = sample_text

# --- Execution ---

if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "running" not in st.session_state:
    st.session_state.running = False

run_button = st.button("Run Transformation", type="primary", disabled=st.session_state.running)

if run_button:
    if not api_key:
        st.warning("Please enter your Anthropic API key in the sidebar.")
    elif not transcript or len(transcript) < 100:
        st.warning("Please provide a transcript with at least 100 characters.")
    else:
        st.session_state.running = True
        st.session_state.pipeline_result = None

        log_queue = queue.Queue()
        result_container = {}

        thread = threading.Thread(
            target=run_pipeline,
            args=(api_key, transcript, business_context, log_queue, result_container),
        )

        with st.status("Running transformation pipeline...", expanded=True) as status:
            thread.start()
            while thread.is_alive():
                try:
                    msg = log_queue.get(timeout=0.5)
                    st.write(msg)
                except queue.Empty:
                    pass
            thread.join()

            # Drain remaining log messages
            while not log_queue.empty():
                st.write(log_queue.get_nowait())

            if "error" in result_container:
                status.update(label="Pipeline failed", state="error")
                st.error(f"Pipeline error: {result_container['error']}")
            elif "result" in result_container:
                result = result_container["result"]
                st.session_state.pipeline_result = result
                if result.success:
                    status.update(label="Pipeline complete!", state="complete")
                else:
                    status.update(label="Pipeline completed with errors", state="error")
            else:
                status.update(label="Pipeline failed", state="error")
                st.error("Pipeline returned no result.")

        st.session_state.running = False

# --- Results display ---

result = st.session_state.pipeline_result

if result is not None:
    if result.errors:
        for err in result.errors:
            st.error(err)

    outputs = result.outputs or {}

    tab_analysis, tab_bpmn, tab_recs, tab_meta = st.tabs(
        ["Analysis", "BPMN Diagram", "Recommendations", "Metadata"]
    )

    with tab_analysis:
        analysis = outputs.get("Transcript Analysis", "")
        if analysis:
            st.markdown(analysis)
        else:
            st.info("No analysis output available.")

    with tab_bpmn:
        bpmn_xml = outputs.get("BPMN Generation", "")
        if bpmn_xml:
            st.code(bpmn_xml, language="xml")
            st.download_button(
                label="Download .bpmn file",
                data=bpmn_xml,
                file_name="process.bpmn",
                mime="application/xml",
            )
        else:
            st.info("No BPMN output available.")

    with tab_recs:
        recommendations = outputs.get("Process Optimization", "")
        if recommendations:
            st.markdown(recommendations)
        else:
            st.info("No recommendations output available.")

    with tab_meta:
        st.json(result.metadata)
        total_cost = result.metadata.get("total_cost_usd", 0)
        st.metric("Total API Cost", f"${total_cost:.4f}")
