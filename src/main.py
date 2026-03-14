from src.agents import PlannerAgent, ResearcherAgent, WriterAgent, ReviewerAgent
from src.tools import search_web, format_search_results
import os
from datetime import datetime

def run_research(topic: str) -> dict:
    """
    Main orchestrator that chains all 4 agents together.
    Returns a dict with all outputs from each agent.
    """
    results = {
        "topic": topic,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plan": "",
        "findings": "",
        "report": "",
        "review": "",
        "status": "started"
    }

    print(f"\n{'='*60}")
    print(f" RESEARCH ASSISTANT STARTED")
    print(f" Topic: {topic}")
    print(f"{'='*60}\n")

    # Step 1: Planner creates research plan
    print("[Step 1/4] Planning...")
    planner = PlannerAgent()
    results["plan"] = planner.run(topic)

    # Step 2: Extract search queries from plan + run searches
    print("\n[Step 2/4] Searching the web...")
    search_queries = extract_search_queries(results["plan"], topic)
    all_search_results = ""
    for query in search_queries:
        print(f"  Searching: {query}")
        raw = search_web(query, max_results=5)
        all_search_results += f"\n\n--- Results for: {query} ---"
        all_search_results += format_search_results(raw)

    # Step 3: Researcher analyzes search results
    print("\n[Step 3/4] Analyzing findings...")
    researcher = ResearcherAgent()
    results["findings"] = researcher.run(topic, results["plan"], all_search_results)

    # Step 4: Writer drafts the report
    print("\n[Step 4/4] Writing report...")
    writer = WriterAgent()
    results["report"] = writer.run(topic, results["plan"], results["findings"])

    # Step 5: Reviewer checks quality
    print("\n[Step 5/5] Reviewing quality...")
    reviewer = ReviewerAgent()
    results["review"] = reviewer.run(topic, results["report"])

    # Save report to outputs folder
    results["status"] = "completed"
    save_report(results)

    print(f"\n{'='*60}")
    print(f" RESEARCH COMPLETED SUCCESSFULLY")
    print(f"{'='*60}\n")

    return results


def extract_search_queries(plan: str, topic: str) -> list:
    """
    Extracts search queries from the planner's output.
    Falls back to basic queries if parsing fails.
    """
    queries = []
    lines = plan.split("\n")
    in_queries_section = False

    for line in lines:
        if "Search Queries" in line:
            in_queries_section = True
            continue
        if in_queries_section and line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
            query = line.strip()[2:].strip()
            if query:
                queries.append(query)
        if in_queries_section and line.startswith("###") and "Search" not in line:
            break

    # Fallback if parsing fails
    if not queries:
        queries = [
            f"{topic} overview",
            f"{topic} latest developments",
            f"{topic} key statistics",
            f"{topic} future trends",
            f"{topic} challenges and opportunities"
        ]

    return queries[:5]  # Max 5 searches


def save_report(results: dict):
    """Saves the final report to the outputs folder."""
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = results["topic"].replace(" ", "_")[:50]
    filename = f"outputs/{safe_topic}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Research Report: {results['topic']}\n")
        f.write(f"*Generated: {results['timestamp']}*\n\n")
        f.write("---\n\n")
        f.write(results["report"])
        f.write("\n\n---\n\n")
        f.write("## Quality Review\n\n")
        f.write(results["review"])

    print(f"\n Report saved: {filename}")
    results["filename"] = filename