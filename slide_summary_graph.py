from langgraph.graph import StateGraph, END



def build_slide_summary_graph(topic_agent, internet_agent, summary_agent, flashcard_agent, mcq_agent):
    # Step 1: Define input/output state (dict-based)
    def run_topic_agent(state):
        state["topics"] = topic_agent.invoke(state["slides"])
        return state

    def run_internet_agent(state):
        state["enriched_info"] = internet_agent.invoke(state["topics"])
        return state

    def run_summary_agent(state):
        roadmap = state.get("topics", "")
        internet_info = state.get("enriched_info", "")
        slides = state["slides"]

        # We pass a structured input to the summarizer now
        state["summary"] = summary_agent.invoke({
            "slides": slides,
            "roadmap": roadmap,
            "internet": internet_info
        })
        return state


    def run_flashcard_agent(state):
        state["flashcards"] = flashcard_agent.invoke({
            "slides": state["slides"],
            "roadmap": state["topics"]
        })
        return state

    def run_mcq_agent(state):
        state["mcqs"] = mcq_agent.invoke({
            "slides": state["slides"],
            "roadmap": state["topics"]
        })
        return state

    # Step 2: Define the graph
    builder = StateGraph(dict)
    builder.add_node("extract_topics", run_topic_agent)
    builder.add_node("research", run_internet_agent)
    builder.add_node("summarize", run_summary_agent)
    builder.add_node("flashcards", run_flashcard_agent)
    builder.add_node("mcqs", run_mcq_agent)

    # Step 3: Define the sequence
    builder.set_entry_point("extract_topics")
    builder.add_edge("extract_topics", "research")
    builder.add_edge("research", "summarize")
    builder.add_edge("summarize", "flashcards")
    builder.add_edge("flashcards", "mcqs")
    builder.add_edge("mcqs", END)

    graph = builder.compile()
    return graph
