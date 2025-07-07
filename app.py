import streamlit as st
from pdf_utils import extract_text_from_pdf
from gemini_llm import GeminiFlashLLM
from topic_agent import build_topic_extractor_agent
from internet_research_agent import build_internet_research_agent
from slide_summarizer_agent import build_slide_summarizer_agent
from flashcard_agent import build_flashcard_agent
from mcq_agent import build_mcq_agent
from slide_summary_graph import build_slide_summary_graph
import tempfile
import os
import io
import zipfile
from dotenv import load_dotenv
import re

st.set_page_config(page_title="📚 AI Slide Summarizer & Study Aid", layout="wide")
st.title("📚 AI Slide Summarizer & Study Aid")
st.markdown("Upload your PDF slide deck and get a topic roadmap, summary, flashcards, and MCQs—powered by Gemini LLM and internet research!")

with st.sidebar:
    st.header("✨ How it works")
    st.write("""
        1. Upload a PDF of your slides.
        2. The AI extracts topics, fetches web context, summarizes, and generates study aids.
        3. Download your study pack 📦!
    """)

# ---------- Utility Functions ----------
def parse_roadmap_to_tree(roadmap_text):
    lines = [l for l in roadmap_text.strip().splitlines() if l.strip()]
    tree = []
    current_main = None
    for line in lines:
        main_match = re.match(r"^\s*\d+\.\s*(.+)", line)
        sub_match = re.match(r"^\s*[-*]\s*(.+)", line)
        if main_match:
            current_main = {"name": main_match.group(1).strip(), "children": []}
            tree.append(current_main)
        elif sub_match and current_main:
            current_main["children"].append({"name": sub_match.group(1).strip(), "children": []})
    return tree

def render_tree(tree):
    for node in tree:
        with st.expander(node["name"]):
            for child in node["children"]:
                st.markdown(f"- {child['name']}")

def highlight_summary(summary):
    return re.sub(r"^## .*$", lambda m: f'<div style="background:#e0e7ff;padding:8px;border-radius:6px;margin:8px 0;font-weight:bold;font-size:1.1em;">{m.group(0)}</div>', summary, flags=re.MULTILINE)

def parse_flashcards(text):
    return [c.strip() for c in text.strip().split("\n\n") if c.strip()]

def parse_mcqs(text):
    mcqs = []
    for block in text.strip().split("\n\n"):
        lines = block.strip().splitlines()
        if not lines: continue
        q = lines[0]
        options = [l for l in lines[1:] if l.strip() and not l.lower().startswith("answer")]
        answer = next((l.split(":")[-1].strip() for l in lines if l.lower().startswith("answer")), None)
        if q and options:
            mcqs.append({"question": q, "options": options, "answer": answer})
    return mcqs

def make_zip_file(topics, enriched_info, summary, flashcards, mcqs):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipf:
        zipf.writestr("topic_roadmap.md", topics)
        zipf.writestr("enriched_info.md", enriched_info)
        zipf.writestr("summary.md", summary)
        zipf.writestr("flashcards.txt", "\n\n".join(flashcards))
        mcq_dump = "\n\n".join(f"{m['question']}\n" + "\n".join(m['options']) + f"\nAnswer: {m['answer']}" for m in mcqs)
        zipf.writestr("mcqs.txt", mcq_dump)
    buffer.seek(0)
    return buffer

# ---------- Main App Logic ----------
uploaded_file = st.file_uploader("Upload a PDF slide deck", type=["pdf"])

if uploaded_file:
    if "last_uploaded_filename" not in st.session_state or st.session_state.last_uploaded_filename != uploaded_file.name:
        st.session_state.last_uploaded_filename = uploaded_file.name
        st.session_state.llm_results = None
        st.session_state.flashcard_idx = 0
        st.session_state.mcq_idx = 0

    if st.session_state.llm_results is None:
        with st.spinner("🔍 Extracting slides and running AI pipeline..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name
            try:
                slides = extract_text_from_pdf(pdf_path)
                load_dotenv()
                llm = GeminiFlashLLM()
                topic_agent = build_topic_extractor_agent(llm)
                internet_agent = build_internet_research_agent(os.getenv("SERPAPI_KEY"))
                summary_agent = build_slide_summarizer_agent(llm)
                flashcard_agent = build_flashcard_agent(llm)
                mcq_agent = build_mcq_agent(llm)
                graph = build_slide_summary_graph(topic_agent, internet_agent, summary_agent, flashcard_agent, mcq_agent)
                final_state = graph.invoke({"slides": slides})
                st.session_state.llm_results = final_state
            finally:
                os.remove(pdf_path)

    final_state = st.session_state.llm_results
    st.success("Done! Explore your results below:")

    # Roadmap
    st.subheader("🧭 Topic Roadmap")
    roadmap_tree = parse_roadmap_to_tree(final_state["topics"])
    if roadmap_tree and any(n["children"] for n in roadmap_tree):
        render_tree(roadmap_tree)
    else:
        st.markdown("#### Raw Roadmap Output")
        st.markdown(f"```markdown\n{final_state['topics']}\n```")
    st.download_button("📅 Download Roadmap", final_state["topics"], file_name="topic_roadmap.md", mime="text/markdown")

    # Enriched Info
    with st.expander("🌐 Enriched Internet Info"):
        st.markdown(f"```markdown\n{final_state['enriched_info']}\n```") 
        st.download_button("📅 Download Enriched Info", final_state["enriched_info"], file_name="enriched_info.md", mime="text/markdown")

    # Summary
    st.subheader("📝 Summary")
    st.markdown(highlight_summary(final_state["summary"]), unsafe_allow_html=True)
    st.download_button("📅 Download Summary", final_state["summary"], file_name="summary.md", mime="text/markdown")

    # Flashcards
    st.subheader("🎓 Flashcards")
    flashcards = parse_flashcards(final_state["flashcards"])
    st.download_button("📅 Download Flashcards", "\n\n".join(flashcards), file_name="flashcards.txt", mime="text/plain")
    fc_idx = st.session_state.flashcard_idx
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button("Previous Flashcard", key="prev_fc", disabled=fc_idx == 0, on_click=lambda: st.session_state.update(flashcard_idx=fc_idx - 1))
    with col2:
        if flashcards:
            st.info(flashcards[fc_idx])
            st.caption(f"Card {fc_idx + 1} of {len(flashcards)}")
    with col3:
        st.button("Next Flashcard", key="next_fc", disabled=fc_idx >= len(flashcards) - 1, on_click=lambda: st.session_state.update(flashcard_idx=fc_idx + 1))

    # MCQs
    st.subheader("🧪 MCQs")
    mcqs = parse_mcqs(final_state["mcqs"])
    st.download_button("📅 Download MCQs", "\n\n".join(
        f"{m['question']}\n" + "\n".join(m['options']) + f"\nAnswer: {m['answer']}" for m in mcqs),
        file_name="mcqs.txt", mime="text/plain"
    )
    mcq_idx = st.session_state.get("mcq_idx", 0)
    mcq_idx = max(0, min(mcq_idx, len(mcqs) - 1))
    st.session_state.mcq_idx = mcq_idx

    if mcqs and 0 <= mcq_idx < len(mcqs):
        mcq = mcqs[mcq_idx]
        st.markdown(f"**Q{mcq_idx + 1}: {mcq['question']}**")
        selected = st.radio("Choose your answer:", mcq["options"], key=f"radio_{mcq_idx}")
        if st.button("Submit Answer", key=f"submit_{mcq_idx}"):
            st.session_state[f"mcq_selected_{mcq_idx}"] = selected
        if st.session_state.get(f"mcq_selected_{mcq_idx}") is not None:
            selected_value = st.session_state[f"mcq_selected_{mcq_idx}"]
            answer_value = mcq["answer"]
            # Compare full string and also allow for letter-only answer keys
            selected_letter = re.match(r"([A-Da-d])", selected_value)
            answer_letter = re.match(r"([A-Da-d])", answer_value)
            is_correct = False
            if selected_value.strip().lower() == answer_value.strip().lower():
                is_correct = True
            elif selected_letter and answer_letter and selected_letter.group(1).lower() == answer_letter.group(1).lower():
                is_correct = True
            if is_correct:
                st.success("Correct! 🎉")
            else:
                st.error(f"Incorrect. Correct answer: {mcq['answer']}")

        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous MCQ", key="prev_mcq", disabled=mcq_idx == 0, on_click=lambda: st.session_state.update(mcq_idx=mcq_idx - 1))
        with col2:
            st.button("Next MCQ", key="next_mcq", disabled=mcq_idx >= len(mcqs) - 1, on_click=lambda: st.session_state.update(mcq_idx=mcq_idx + 1))
        st.caption(f"Question {mcq_idx + 1} of {len(mcqs)}")

    # Download All
    st.subheader("📦 Download All as ZIP")
    zip_buffer = make_zip_file(
        final_state["topics"],
        final_state["enriched_info"],
        final_state["summary"],
        flashcards,
        mcqs
    )
    st.download_button("📦 Download Study Pack", data=zip_buffer, file_name="study_pack.zip", mime="application/zip")

else:
    st.info("👆 Upload a PDF to get started!")
