from langchain_core.runnables import RunnableLambda

def build_topic_extractor_agent(llm):
    """
    Extracts top 3 most important topics from slides,
    with no more than 2–3 prioritized subtopics per topic.
    """

    def extract_topics(slides: list[str]) -> str:
        joined_slides = "\n\n".join(slides[:15])  # Limit to 15 slides for speed

        prompt = f"""
You are a slide deck analyzer.

From the given slides, identify the **top 3 most important main topics**.
For each main topic, include only **2–3 subtopics** that are the most relevant or representative.

Avoid repeating or overlapping topics. Prioritize coverage and depth.

Format strictly like this:

1. [Main Topic 1]
   - Subtopic A
   - Subtopic B

2. [Main Topic 2]
   - Subtopic C
   - Subtopic D

3. [Main Topic 3]
   - Subtopic E
   - Subtopic F

Slides:
{joined_slides}
"""

        return llm.invoke(prompt)

    return RunnableLambda(extract_topics)
