#!/usr/bin/env python3
"""
AI Agent Workflow Example
==========================
Example showing how an AI agent can use TradingAgents.

This demonstrates the workflow:
1. Run analysis on a ticker/date
2. Read the generated reports
3. Feed reports to your AI assistant for further processing
"""

import subprocess
import sys
import json
import os

# Add scripts directory to path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

from read_reports import parse_reports


def run_analysis_and_get_reports(ticker: str, date: str, provider: str = "minimax"):
    """
    Run TradingAgents analysis and return all reports as a dictionary.
    """
    # Step 1: Run the analysis
    print(f"Running TradingAgents analysis for {ticker} on {date}...")
    run_script = os.path.join(scripts_dir, "run_analysis.py")

    result = subprocess.run(
        [sys.executable, run_script, ticker, date, "--provider", provider],
        capture_output=False
    )

    if result.returncode != 0:
        return {"error": f"Analysis failed with code {result.returncode}"}

    # Step 2: Read the reports
    date_formatted = date.replace("-", "")  # Convert YYYY-MM-DD to YYYYMMDD
    reports_dir = os.path.join(os.path.dirname(scripts_dir), "reports")

    reports = parse_reports(ticker, date_formatted, reports_dir)
    return reports


def main():
    # Example: Analyze TSMC on a specific date
    ticker = "2330.TW"
    date = "2026-06-11"

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         TradingAgents AI Agent Workflow Example               ║
╚══════════════════════════════════════════════════════════════╝

This example shows how an AI agent can:
1. Trigger TradingAgents analysis
2. Read all generated reports
3. Process them for further use

""")

    # Run analysis and get reports
    reports = run_analysis_and_get_reports(ticker, date)

    if "error" in reports:
        print(f"Error: {reports['error']}")
        return

    # Now you can feed these reports to your AI assistant
    print("\n" + "="*60)
    print("AVAILABLE REPORTS FOR AI PROCESSING:")
    print("="*60)

    for report_name, content in reports["reports"].items():
        print(f"\n--- {report_name} ---")
        print(content[:500] if content else "[Empty]")
        if content and len(content) > 500:
            print(f"... (truncated, {len(content)} chars total)")


if __name__ == "__main__":
    main()