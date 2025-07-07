from gemini_llm import GeminiFlashLLM
from pdf_utils import extract_text_from_pdf
from topic_agent import build_topic_extractor_agent
from internet_research_agent import build_internet_research_agent
from slide_summarizer_agent import build_slide_summarizer_agent
from flashcard_agent import build_flashcard_agent
from mcq_agent import build_mcq_agent
from slide_summary_graph import build_slide_summary_graph
import os
from dotenv import load_dotenv

load_dotenv()
slides = extract_text_from_pdf("examples.pdf")

llm = GeminiFlashLLM()
serpapi_key = os.getenv("SERPAPI_KEY")

# Build agents
topic_agent = build_topic_extractor_agent(llm)
internet_agent = build_internet_research_agent(serpapi_key)
summary_agent = build_slide_summarizer_agent(llm)
flashcard_agent = build_flashcard_agent(llm)
mcq_agent = build_mcq_agent(llm)

# Build graph
graph = build_slide_summary_graph(
    topic_agent,
    internet_agent,
    summary_agent,
    flashcard_agent,
    mcq_agent
)

# Initial state
state = {"slides": slides}

# Run graph
final_state = graph.invoke(state)

# Print results
print("\n📘 Final Output:")
print("\n🧭 Topics:\n", final_state["topics"])
print("\n🌐 Enriched Info:\n", final_state["enriched_info"])
print("\n📝 Summary:\n", final_state["summary"])
print("\n🎓 Flashcards:\n", final_state["flashcards"])
print("\n🧪 MCQs:\n", final_state["mcqs"])
