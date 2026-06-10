#!/usr/bin/env python3
"""
TradingAgents Simple Runner
===========================
A simple wrapper for TradingAgents that only requires ticker and date.
Outputs reports to a predictable location for AI agents to consume.

Usage:
    python run_analysis.py 2330.TW 2026-06-11
    python run_analysis.py 2330.TW 2026-06-11 --provider minimax
    python run_analysis.py 2330.TW 2026-06-11 --deep-model MiniMax-M2.7 --quick-model MiniMax-M2.7-highspeed

Environment variables:
    MINIMAX_API_KEY, OPENAI_API_KEY, etc. - Set based on chosen provider
"""

import argparse
import os
import sys
from datetime import datetime

# Add TradingAgents to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run TradingAgents analysis on a ticker for a specific date."
    )
    parser.add_argument(
        "ticker",
        help="Ticker symbol (e.g., 2330.TW, AAPL, BTC-USD)"
    )
    parser.add_argument(
        "date",
        help="Analysis date in YYYY-MM-DD format (e.g., 2026-06-11)"
    )
    parser.add_argument(
        "--provider",
        default=os.environ.get("TRADINGAGENTS_LLM_PROVIDER", "minimax"),
        help=f"LLM provider (default: minimax). Options: openai, google, anthropic, minimax, etc."
    )
    parser.add_argument(
        "--deep-model",
        help="Model for deep/complex reasoning (default: from config or MiniMax-M2.7)"
    )
    parser.add_argument(
        "--quick-model",
        help="Model for quick/simple tasks (default: from config or MiniMax-M2.7-highspeed)"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for reports (default: ./reports)"
    )
    parser.add_argument(
        "--max-debate-rounds",
        type=int,
        default=1,
        help="Number of debate rounds between researchers (default: 1)"
    )
    parser.add_argument(
        "--language",
        default="繁體中文",
        help="Output language (default: 繁體中文)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Validate date format
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.")
        sys.exit(1)

    # Build config
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = args.provider
    config["output_language"] = args.language
    config["max_debate_rounds"] = args.max_debate_rounds

    # Set models if provided
    if args.deep_model:
        config["deep_think_llm"] = args.deep_model
    if args.quick_model:
        config["quick_think_llm"] = args.quick_model

    # Set output directory
    output_dir = args.output_dir or os.path.join(os.getcwd(), "reports")
    config["results_dir"] = output_dir

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║              TradingAgents Analysis Runner                   ║
╠══════════════════════════════════════════════════════════════╣
║  Ticker: {args.ticker:<50}║
║  Date:   {args.date:<50}║
║  Provider: {args.provider:<47}║
║  Deep Model: {config.get('deep_think_llm', 'default'):<44}║
║  Quick Model: {config.get('quick_think_llm', 'default'):<43}║
║  Output: {output_dir:<49}║
╚══════════════════════════════════════════════════════════════╝
""")

    # Initialize and run
    print("Initializing TradingAgents graph...")
    ta = TradingAgentsGraph(debug=True, config=config)

    print(f"\nRunning analysis for {args.ticker} on {args.date}...")
    print("(This may take several minutes...)\n")

    try:
        _, decision = ta.propagate(args.ticker, args.date)
        print(f"\n{'='*60}")
        print("FINAL DECISION:")
        print(f"{'='*60}")
        print(decision)
    except Exception as e:
        print(f"\nError during analysis: {e}")
        sys.exit(1)

    # Report output location
    report_path = os.path.join(
        output_dir,
        f"{args.ticker}_{args.date.replace('-', '')}"
    )
    print(f"\n{'='*60}")
    print(f"Reports saved to: {report_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()