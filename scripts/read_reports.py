#!/usr/bin/env python3
"""
TradingAgents Report Reader
===========================
Reads TradingAgents reports and outputs a JSON summary for AI agents.

Usage:
    python read_reports.py 2330.TW 20260611
    python read_reports.py 2330.TW 20260611 --reports-dir ./reports
"""

import argparse
import json
import os
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read TradingAgents reports and output as JSON."
    )
    parser.add_argument(
        "ticker",
        help="Ticker symbol (e.g., 2330.TW, AAPL)"
    )
    parser.add_argument(
        "date",
        help="Date in YYYYMMDD format (e.g., 20260611)"
    )
    parser.add_argument(
        "--reports-dir",
        default="./reports",
        help="Base directory containing reports (default: ./reports)"
    )
    return parser.parse_args()


def read_markdown_file(filepath: str) -> str:
    """Read a markdown file and return its contents."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"[File not found: {filepath}]"
    except Exception as e:
        return f"[Error reading file: {e}]"


def parse_reports(ticker: str, date: str, reports_dir: str) -> dict:
    """
    Parse all reports for a given ticker and date.
    Returns a dictionary with all report contents.
    """
    # Build the report directory path
    # Format: {ticker}_{date} e.g., 2330.TW_20260611
    report_subdir = f"{ticker}_{date}"
    report_path = os.path.join(reports_dir, report_subdir, "reports")

    if not os.path.exists(report_path):
        return {
            "error": f"Reports not found at: {report_path}",
            "ticker": ticker,
            "date": date,
            "reports_dir": reports_dir
        }

    # Define report files to read
    report_files = {
        "final_trade_decision": "final_trade_decision.md",
        "fundamentals_report": "fundamentals_report.md",
        "market_report": "market_report.md",
        "news_report": "news_report.md",
        "sentiment_report": "sentiment_report.md",
        "investment_plan": "investment_plan.md",
        "trader_investment_plan": "trader_investment_plan.md",
    }

    reports = {}
    for key, filename in report_files.items():
        filepath = os.path.join(report_path, filename)
        reports[key] = read_markdown_file(filepath)

    return {
        "ticker": ticker,
        "date": date,
        "report_path": report_path,
        "reports": reports
    }


def output_json(reports: dict):
    """Output reports as formatted JSON."""
    print(json.dumps(reports, ensure_ascii=False, indent=2))


def output_summary(reports: dict):
    """Output a simple text summary of available reports."""
    print(f"\n{'='*60}")
    print(f"Reports for {reports['ticker']} on {reports['date']}")
    print(f"{'='*60}")

    if "error" in reports:
        print(f"Error: {reports['error']}")
        return

    print(f"Location: {reports['report_path']}\n")

    for key, content in reports["reports"].items():
        preview = content[:200].replace('\n', ' ') if content else "[Empty]"
        if len(content) > 200:
            preview += "..."
        print(f"  {key}: {preview}")

    print(f"\nFull reports available at: {reports['report_path']}")


def main():
    args = parse_args()

    # Validate date format (should be YYYYMMDD)
    if len(args.date) != 8 or not args.date.isdigit():
        print(f"Error: Invalid date format '{args.date}'. Use YYYYMMDD (e.g., 20260611).")
        sys.exit(1)

    # Parse reports
    reports = parse_reports(args.ticker, args.date, args.reports_dir)

    # Output based on format
    if "--json" in sys.argv:
        output_json(reports)
    else:
        output_summary(reports)
        print("\n(Use --json flag to output full JSON for AI agents)")


if __name__ == "__main__":
    main()