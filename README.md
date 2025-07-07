# 📚 Document Summarizer & Study Aid Generator

A powerful AI-powered tool to **summarize PDF slide decks**, extract topic roadmaps, generate flashcards, and create MCQs for study—all with a beautiful Streamlit frontend.

---

## ✨ Features

- **PDF Slide Extraction:** Reads and parses your slide decks.
- **Topic Roadmap:** Extracts the top 3 main topics and their key subtopics.
- **Internet-Enriched Summaries:** Fetches web context for deeper understanding.
- **Structured Summaries:** Groups content by topic and subtopic.
- **Flashcard Generator:** Creates high-quality Q&A flashcards.
- **MCQ Generator:** Produces multiple-choice questions for self-testing.
- **Interactive Streamlit App:** Upload PDFs, browse results, and download your study pack.

---

## 🗂️ Project Structure

```
main.py
test.py
slide_summarizer_agents/
    .env
    .gitignore
    app.py
    examples.pdf
    flashcard_agent.py
    gemini_llm.py
    internet_research_agent.py
    mcq_agent.py
    pdf_utils.py
    requirements.txt
    run_graph.py
    slide_summarizer_agent.py
    slide_summary_graph.py
    topic_agent.py
```

---

## 🚀 Getting Started

### 1. **Clone the Repository**

```sh
git clone <your-repo-url>
cd document_summarizer
```

### 2. **Install Dependencies**

```sh
cd slide_summarizer_agents
pip install -r requirements.txt
```

### 3. **Set Up API Keys**

- Copy `.env` to your project root or edit `slide_summarizer_agents/.env`.
- Add your [Google Gemini API key](https://ai.google.dev/) and [SerpAPI key](https://serpapi.com/):

```
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_KEY=your_serpapi_key
```

### 4. **Run the Streamlit Frontend**

```sh
cd slide_summarizer_agents
streamlit run app.py
```

- Open the link shown in your terminal to access the web app.
- Upload a PDF slide deck and explore the AI-generated study aids!

---

## 🧑‍💻 Usage (CLI)

- **Topic Roadmap (CLI):**
    ```sh
    python main.py
    ```
    - Edit `main.py` to set your PDF filename.

- **Full Pipeline (CLI):**
    ```sh
    python slide_summarizer_agents/run_graph.py
    ```
    - Outputs all results to the console.

---

## 🛠️ Core Components

- **[gemini_llm.py](slide_summarizer_agents/gemini_llm.py):** Gemini LLM API wrapper.
- **[pdf_utils.py](slide_summarizer_agents/pdf_utils.py):** PDF text extraction.
- **[topic_agent.py](slide_summarizer_agents/topic_agent.py):** Topic roadmap extraction.
- **[internet_research_agent.py](slide_summarizer_agents/internet_research_agent.py):** Web search enrichment.
- **[slide_summarizer_agent.py](slide_summarizer_agents/slide_summarizer_agent.py):** Structured summarization.
- **[flashcard_agent.py](slide_summarizer_agents/flashcard_agent.py):** Flashcard generation.
- **[mcq_agent.py](slide_summarizer_agents/mcq_agent.py):** MCQ generation.
- **[slide_summary_graph.py](slide_summarizer_agents/slide_summary_graph.py):** Orchestrates the multi-step workflow.
- **[app.py](slide_summarizer_agents/app.py):** Streamlit frontend.

---

## 📦 Output

- **Topic Roadmap:** Main topics and subtopics (Markdown).
- **Enriched Info:** Internet summaries for each topic.
- **Summary:** Structured, topic-guided summary.
- **Flashcards:** Q&A pairs for study.
- **MCQs:** Multiple-choice questions with answers.
- **Downloadable ZIP:** All outputs in one click from the app.

---

## 📝 Example

1. **Upload a PDF in the Streamlit app.**
2. **Get:**
    - Interactive topic roadmap
    - Internet-enriched context
    - Structured summary
    - Flashcards (with navigation)
    - MCQs (with instant feedback)
    - Download all as a study pack

---

## 🧪 Testing

- Run `test.py` to test Gemini LLM connectivity.

---

## 🛡️ License

MIT License

---

## 🙏 Credits

- [Google Gemini](https://ai.google.dev/)
- [SerpAPI](https://serpapi.com/)
- [LangChain](https://python.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

---

## 💡 Tips

- For best results, use clear, text-rich slide decks.
- API usage may incur costs—monitor your usage on Gemini and SerpAPI dashboards.

---

Enjoy your AI-powered
