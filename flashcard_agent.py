from langchain_core.runnables import RunnableLambda

def build_flashcard_agent(llm):
    def generate_flashcards(inputs: dict) -> str:
        slides = inputs.get("slides", [])
        roadmap = inputs.get("roadmap", "")
        joined_slides = "\n\n".join(slides[:15])

        prompt = f"""
You're a flashcard generator AI.

Create question-answer style flashcards from the following slides. Use the roadmap to guide what topics to focus on.
Each flashcard should cover a specific concept from the roadmap.

Format:
Q: [Question]
A: [Answer]

Only include 5–10 high-quality flashcards.

---
📌 Roadmap:
{roadmap}

📄 Slides:
{joined_slides}
"""
        return llm.invoke(prompt)

    return RunnableLambda(generate_flashcards)
