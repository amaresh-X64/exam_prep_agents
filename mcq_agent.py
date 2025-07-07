from langchain_core.runnables import RunnableLambda

def build_mcq_agent(llm):
    def generate_mcqs(inputs: dict) -> str:
        slides = inputs.get("slides", [])
        roadmap = inputs.get("roadmap", "")
        joined_slides = "\n\n".join(slides[:15])

        prompt = f"""
You're an expert quiz maker.

Generate 5 multiple-choice questions (MCQs) based on the roadmap and slide content.
Each question must test understanding of a key topic or subtopic.

Format:
Q: [Question]
A) Option A
B) Option B
C) Option C
D) Option D
Answer: [Correct Option Letter]

Ensure the MCQs are non-trivial and varied in scope.

---
📌 Roadmap:
{roadmap}

📄 Slides:
{joined_slides}
"""
        return llm.invoke(prompt)

    return RunnableLambda(generate_mcqs)
