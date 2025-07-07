from langchain_core.runnables import RunnableLambda

def build_slide_summarizer_agent(llm):
    def summarize_slides(inputs: dict) -> str:
        slides = inputs.get("slides", [])
        roadmap = inputs.get("roadmap", "")
        internet = inputs.get("internet", "")

        joined_slides = "\n\n".join(slides[:15])  # limit for speed

        prompt = f"""
You are an expert summarizer.

You will be given:
- A roadmap of topics/subtopics
- Extra context gathered from the internet
- The original slide content

Use the roadmap to guide the structure of your summary.
Enrich it with the internet info, and draw supporting content from the slides.

Make the summary well-structured and grouped by main topic & subtopic.

---
📌 Roadmap:
{roadmap}

🌐 Internet Info:
{internet}

📄 Slides:
{joined_slides}
"""

        return llm.invoke(prompt)

    return RunnableLambda(summarize_slides)
