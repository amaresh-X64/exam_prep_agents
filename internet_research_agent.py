from langchain_core.runnables import RunnableLambda
from serpapi import GoogleSearch
import time

def build_internet_research_agent(api_key, max_retries=3, retry_delay=2):
    cache = {}

    def research_topics(topics_text: str) -> str:
        lines = [line.strip("- .\n") for line in topics_text.split("\n") if line.strip()]
        summaries = []

        for topic in lines:
            if topic in cache:
                snippet = cache[topic]
            else:
                params = {
                    "api_key": api_key,
                    "q": topic,
                    "num": "3",
                    "hl": "en",
                    "gl": "us",
                }

                retries = 0
                snippet = ""
                while retries < max_retries:
                    try:
                        search = GoogleSearch(params)
                        results = search.get_dict()
                        if "organic_results" in results and results["organic_results"]:
                            snippet = results["organic_results"][0].get("snippet", "")
                        break
                    except Exception as e:
                        retries += 1
                        print(f"⚠️ Retry {retries} for topic '{topic}' due to error: {e}")
                        time.sleep(retry_delay)

                cache[topic] = snippet

            summaries.append(f"Topic: {topic}\nSummary: {snippet}\n")

        return "\n".join(summaries)

    return RunnableLambda(research_topics)
