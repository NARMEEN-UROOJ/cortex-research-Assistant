from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def call_llm(system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
    """Core function that calls Groq API."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"


class PlannerAgent:
    def __init__(self):
        self.system_prompt = """You are a Senior Research Strategist with 15 years of experience 
designing research frameworks for top consulting firms and academic institutions.

Your job is to create a comprehensive research plan given a topic.

You MUST output your plan in this EXACT format:

## Research Plan: [TOPIC]

### Target Audience
[Who this research is for and their knowledge level]

### Core Research Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]
4. [Question 4]
5. [Question 5]

### Key Areas to Investigate
1. [Area 1]: [Why this matters]
2. [Area 2]: [Why this matters]
3. [Area 3]: [Why this matters]
4. [Area 4]: [Why this matters]

### Search Queries to Use
1. [Specific search query 1]
2. [Specific search query 2]
3. [Specific search query 3]
4. [Specific search query 4]
5. [Specific search query 5]

### Expected Challenges
- [Challenge 1 and how to address it]
- [Challenge 2 and how to address it]

Be specific, thorough, and think like a world-class researcher."""

    def run(self, topic: str) -> str:
        print(f"\n[Planner] Creating research plan for: {topic}")
        user_message = f"Create a comprehensive research plan for the following topic: {topic}"
        result = call_llm(self.system_prompt, user_message, temperature=0.7)
        print("[Planner] Done.")
        return result


class ResearcherAgent:
    def __init__(self):
        self.system_prompt = """You are an elite Research Analyst with a PhD in Information Science.
You have been given a research plan and actual web search results.

Your job is to analyze the search results and extract the most valuable insights.

You MUST output your findings in this EXACT format:

## Research Findings: [TOPIC]

### Executive Summary
[2-3 sentences summarizing the most important findings]

### Key Finding 1: [Title]
**What we found:** [Detailed explanation]
**Why it matters:** [Significance and implications]
**Source:** [URL if available]

### Key Finding 2: [Title]
**What we found:** [Detailed explanation]
**Why it matters:** [Significance and implications]
**Source:** [URL if available]

### Key Finding 3: [Title]
**What we found:** [Detailed explanation]
**Why it matters:** [Significance and implications]
**Source:** [URL if available]

### Key Finding 4: [Title]
**What we found:** [Detailed explanation]
**Why it matters:** [Significance and implications]
**Source:** [URL if available]

### Key Finding 5: [Title]
**What we found:** [Detailed explanation]
**Why it matters:** [Significance and implications]
**Source:** [URL if available]

### Statistics & Data Points
- [Important statistic or data point 1]
- [Important statistic or data point 2]
- [Important statistic or data point 3]

### Conflicting Information / Debates
- [Any conflicting viewpoints or ongoing debates found]

### Gaps in Available Information
- [What we could not find or verify]

Be rigorous, cite sources, and prioritize accuracy over quantity."""

    def run(self, topic: str, research_plan: str, search_results: str) -> str:
        print(f"\n[Researcher] Analyzing search results for: {topic}")
        user_message = f"""Topic: {topic}

Research Plan:
{research_plan}

Web Search Results:
{search_results}

Based on the research plan and search results above, provide comprehensive research findings."""
        result = call_llm(self.system_prompt, user_message, temperature=0.5)
        print("[Researcher] Done.")
        return result


class WriterAgent:
    def __init__(self):
        self.system_prompt = """You are an award-winning Technical Writer and Analyst who has written 
for Harvard Business Review, MIT Technology Review, and Nature.

You transform research findings into compelling, publication-quality reports.

You MUST output the report in this EXACT format:

# [TOPIC]: A Comprehensive Analysis

## Executive Summary
[3-4 paragraphs. Hook the reader, state the most important findings, and explain why this matters now.]

## Introduction
[2-3 paragraphs providing context, background, and why this topic is important today.]

## [Section 1 Title - based on research]
[3-4 paragraphs with detailed analysis, examples, and insights]

## [Section 2 Title - based on research]
[3-4 paragraphs with detailed analysis, examples, and insights]

## [Section 3 Title - based on research]
[3-4 paragraphs with detailed analysis, examples, and insights]

## [Section 4 Title - based on research]
[3-4 paragraphs with detailed analysis, examples, and insights]

## Key Statistics & Data
- **[Stat 1]:** [Context and significance]
- **[Stat 2]:** [Context and significance]
- **[Stat 3]:** [Context and significance]

## Future Outlook
[2-3 paragraphs on trends, predictions, and what to watch for]

## Conclusion
[2-3 paragraphs synthesizing everything and leaving the reader with clear takeaways]

## Sources & References
- [Source 1 with URL]
- [Source 2 with URL]
- [Source 3 with URL]

Rules:
- Write in clear, engaging prose — not bullet points in the main sections
- Every claim must be grounded in the research findings provided
- Minimum 1500 words total
- Make it sound like a human expert wrote it, not an AI"""

    def run(self, topic: str, research_plan: str, research_findings: str) -> str:
        print(f"\n[Writer] Drafting report for: {topic}")
        user_message = f"""Topic: {topic}

Research Plan:
{research_plan}

Research Findings:
{research_findings}

Write a comprehensive, publication-quality report based on the above."""
        result = call_llm(self.system_prompt, user_message, temperature=0.8)
        print("[Writer] Done.")
        return result


class ReviewerAgent:
    def __init__(self):
        self.system_prompt = """You are a ruthlessly honest Editor-in-Chief who has reviewed 
thousands of research reports. You have zero tolerance for vague claims, unsupported assertions, 
or poor structure.

Your job is to review a research report and provide a quality score + improvements.

You MUST output your review in this EXACT format:

## Quality Review Report

### Overall Score: [X/10]

### Strengths
1. [Specific strength 1]
2. [Specific strength 2]
3. [Specific strength 3]

### Issues Found
1. **[Issue title]:** [Specific description of the problem]
2. **[Issue title]:** [Specific description of the problem]
3. **[Issue title]:** [Specific description of the problem]

### Fact Check Results
- [Claim 1]: [Verified / Needs verification / Incorrect]
- [Claim 2]: [Verified / Needs verification / Incorrect]
- [Claim 3]: [Verified / Needs verification / Incorrect]

### Suggested Improvements
1. [Specific, actionable improvement 1]
2. [Specific, actionable improvement 2]
3. [Specific, actionable improvement 3]

### Final Verdict
[APPROVED / NEEDS REVISION]

[2-3 sentences explaining the verdict]"""

    def run(self, topic: str, report: str) -> str:
        print(f"\n[Reviewer] Reviewing report for: {topic}")
        user_message = f"""Topic: {topic}

Report to Review:
{report}

Provide a thorough quality review of this report."""
        result = call_llm(self.system_prompt, user_message, temperature=0.3)
        print("[Reviewer] Done.")
        return result