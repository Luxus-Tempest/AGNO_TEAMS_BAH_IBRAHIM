from agno.agent import Agent
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.models.openai import OpenAIChat
from textwrap import dedent
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Data Fetching Agent
news_agent = Agent(
    name="NewsFetcher",
    role="Fetch recent news articles about major tech stocks (AAPL, MSFT, GOOGL, AMZN, TSLA).",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[DuckDuckGoTools()],
    instructions=dedent("""
        Retrieve recent stock news from reliable sources (last 7 days) focusing on:
        - Earnings reports
        - Product announcements
        - Executive changes
        - Regulatory developments
        Include publication dates, sources, and key details.
    """).strip(),
    markdown=True,
)

# Analysis Agent
analysis_agent = Agent(
    name="AnalysisAgent",
    role="Analyze news articles to extract market sentiment, fundamental insights, and technical cues.",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[ReasoningTools()],
    instructions=dedent("""
        Analyze news for:
        1. Market sentiment (bullish vs bearish, confidence indicators)
        2. Fundamental analysis (financial performance, growth prospects, competitive positioning)
        3. Technical insights (price movements, trading volume patterns, support/resistance)
        Provide quantitative sentiment scores (1-10) where possible.
    """).strip(),
    markdown=True,
)

# Report Writer Agent
writer_agent = Agent(
    name="ReportWriter",
    role="Write detailed stock market analysis reports based on collected and analyzed news.",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    instructions=dedent("""
        Create a professional investment research report including:
        1. Executive Summary: Key highlights, market sentiment, top recommendations
        2. Market News Digest: Major developments by company, earnings, product updates
        3. Sentiment Analysis: Market mood, bullish vs bearish factors, risk assessment
        4. Strategic Insights: Investment implications, sector trends, timing considerations
        5. Action Items: Watch list recommendations, key dates, risk management
        Format with headers, bullet points, tables, and include disclaimer about investment risks.
    """).strip(),
    markdown=True,
)

# Data Visualizer Agent
visualizer_agent = Agent(
    name="DataVisualizer",
    role="Generate visualizations for sentiment, trends, and key metrics from the analyzed news.",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    instructions=dedent("""
        From the analyzed news and sentiment scores, create:
        - Charts showing bullish vs bearish sentiment over time
        - Trend graphs of stock-specific news impact
        - Tables or visuals summarizing key metrics (earnings, product launches, executive changes)
        Format visuals clearly and make them easy to interpret for investors in the terminal.
    """).strip(),
    markdown=True,
)

# Team Coordination
stock_analysis_team = Team(
    name="StockMarketAnalysisTeam",
    members=[news_agent, analysis_agent, writer_agent, visualizer_agent],
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    instructions=dedent("""
        Execute a coordinated stock market analysis workflow:

        Phase 1 - Data Collection:
        - NewsFetcher gathers recent news for major stocks
        - Ensure data quality and credibility

        Phase 2 - Analysis:
        - AnalysisAgent processes news for sentiment, fundamentals, and technical insights
        - Quantify sentiment where possible

        Phase 3 - Reporting:
        - ReportWriter synthesizes findings into actionable report
        - Include clear investment thesis, recommendations, and risk disclaimers

        Phase 4 - Visualization:
        - DataVisualizer generates charts, graphs, and tables for key insights
        - Ensure visuals are clear, informative, and easy to interpret

        Collaborate effectively; ensure smooth information flow between all phases.
    """).strip(),
    markdown=True,
)

# Main Prompt
MAIN_PROMPT = "Prepare me a report on the latest Apple product announcements with visualizations."

if __name__ == "__main__":
    stock_analysis_team.print_response(
        MAIN_PROMPT,
        stream=True
    )
