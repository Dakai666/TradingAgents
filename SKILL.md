# TradingAgents AI Agent Integration

## Overview

This skill enables AI agents to use TradingAgents for multi-agent financial trading analysis. The workflow requires only a ticker symbol and date, making it ideal for automated AI assistants.

## Prerequisites

```bash
# Install from your fork
pip install git+https://github.com/Dakai666/TradingAgents.git

# Or install locally
cd /path/to/TradingAgents
pip install .

# Set your LLM API key
export MINIMAX_API_KEY=your_key_here
```

## Scripts

### 1. run_analysis.py - Execute Analysis

Run TradingAgents analysis with only ticker and date.

```bash
python scripts/run_analysis.py <TICKER> <DATE> [OPTIONS]

# Examples
python scripts/run_analysis.py 2330.TW 2026-06-11
python scripts/run_analysis.py 2330.TW 2026-06-11 --provider minimax
python scripts/run_analysis.py AAPL 2026-06-11 --deep-model MiniMax-M2.7 --quick-model MiniMax-M2.7-highspeed
```

**Arguments:**
- `ticker` - Stock ticker (e.g., `2330.TW`, `AAPL`, `BTC-USD`)
- `date` - Analysis date in `YYYY-MM-DD` format

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--provider` | LLM provider | `minimax` |
| `--deep-model` | Model for complex reasoning | MiniMax-M2.7 |
| `--quick-model` | Model for quick tasks | MiniMax-M2.7-highspeed |
| `--output-dir` | Report output directory | `./reports` |
| `--max-debate-rounds` | Debate rounds | 1 |
| `--language` | Output language | 繁體中文 |

**Supported Tickers:**
- Taiwan: `2330.TW`, `2317.TW`, etc.
- US: `AAPL`, `TSLA`, `SPY`, etc.
- Hong Kong: `0700.HK`
- Japan: `7203.T`
- Crypto: `BTC-USD`, `ETH-USD`

### 2. read_reports.py - Read Analysis Reports

Read generated reports and output as JSON for AI agents.

```bash
python scripts/read_reports.py <TICKER> <DATE> [OPTIONS]

# Examples
python scripts/read_reports.py 2330.TW 20260611
python scripts/read_reports.py 2330.TW 20260611 --reports-dir ./reports --json
```

**Arguments:**
- `ticker` - Stock ticker (e.g., `2330.TW`)
- `date` - Date in `YYYYMMDD` format (note: no dashes)

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--reports-dir` | Base reports directory | `./reports` |
| `--json` | Output as JSON | False (text summary) |

## Output Structure

Reports are saved to:
```
{output_dir}/{TICKER}_{YYYYMMDD}/reports/
├── final_trade_decision.md      # Final trading decision (BUY/HOLD/SELL)
├── fundamentals_report.md       # Company fundamentals analysis
├── market_report.md             # Technical analysis & market data
├── news_report.md               # News analysis
├── sentiment_report.md          # Sentiment analysis (social media)
├── investment_plan.md           # Investment plan
└── trader_investment_plan.md    # Trader's investment plan
```

## AI Agent Workflow

### Basic Integration

```python
import subprocess
import sys
import os

scripts_dir = "/path/to/TradingAgents/scripts"
sys.path.insert(0, scripts_dir)
from read_reports import parse_reports

def run_trading_analysis(ticker: str, date: str, provider: str = "minimax") -> dict:
    """
    Run TradingAgents analysis and return all reports.

    Args:
        ticker: Stock ticker (e.g., "2330.TW")
        date: Analysis date in YYYY-MM-DD format (e.g., "2026-06-11")
        provider: LLM provider (default: "minimax")

    Returns:
        Dictionary containing all reports
    """
    # Run analysis
    run_script = os.path.join(scripts_dir, "run_analysis.py")
    subprocess.run(
        [sys.executable, run_script, ticker, date, "--provider", provider],
        check=True
    )

    # Read reports
    date_formatted = date.replace("-", "")  # YYYY-MM-DD -> YYYYMMDD
    reports_dir = os.path.join(os.path.dirname(scripts_dir), "reports")
    reports = parse_reports(ticker, date_formatted, reports_dir)

    return reports

# Usage
reports = run_trading_analysis("2330.TW", "2026-06-11")

# Feed to your AI assistant
for report_name, content in reports["reports"].items():
    if content and not content.startswith("["):
        print(f"=== {report_name.upper()} ===")
        print(content[:1000])  # First 1000 chars
```

### JSON Output for AI

```bash
# Get all reports as JSON
python scripts/read_reports.py 2330.TW 20260611 --reports-dir ./reports --json
```

Output format:
```json
{
  "ticker": "2330.TW",
  "date": "20260611",
  "report_path": "./reports/2330.TW_20260611/reports",
  "reports": {
    "final_trade_decision": "## Final Trade Decision\n\n**Action**: HOLD\n\n**Reasoning**: ...",
    "fundamentals_report": "## Fundamentals Report\n\n...",
    "market_report": "## Market Report\n\n...",
    "news_report": "## News Report\n\n...",
    "sentiment_report": "## Sentiment Report\n\n...",
    "investment_plan": "## Investment Plan\n\n...",
    "trader_investment_plan": "## Trader Investment Plan\n\n..."
  }
}
```

## Environment Variables

| Variable | Description | Provider |
|----------|-------------|----------|
| `MINIMAX_API_KEY` | MiniMax global API | minimax |
| `MINIMAX_CN_API_KEY` | MiniMax China API | minimax-cn |
| `OPENAI_API_KEY` | OpenAI API | openai |
| `GOOGLE_API_KEY` | Google API | google |
| `ANTHROPIC_API_KEY` | Anthropic API | anthropic |
| `TRADINGAGENTS_LLM_PROVIDER` | Default provider | - |
| `TRADINGAGENTS_RESULTS_DIR` | Reports output directory | - |

## Two-Stage AI Pipeline

For advanced AI assistants, combine TradingAgents with custom analysis:

### Stage 1: TradingAgents Base Analysis
```
Input: ticker + date
↓
TradingAgents (5 agents + debate)
↓
Output: Multi-agent analysis reports
```

### Stage 2: Custom AI Enhancement
```
Input: Base reports + user context
↓
Your AI Assistant analyzes and enhances
↓
Output: Personalized action guide
```

Example Stage 2 prompts:
- "Based on these reports and my 80% portfolio position, should I follow the BUY signal?"
- "Given my stop-loss at 32.50, what does this risk assessment mean for me?"
- "Combine this with current macro conditions: [macro analysis]"

## Error Handling

```python
import subprocess

try:
    result = subprocess.run(
        [sys.executable, "scripts/run_analysis.py", ticker, date],
        capture_output=True,
        text=True,
        check=True
    )
    print("Analysis completed successfully")
except subprocess.CalledProcessError as e:
    print(f"Analysis failed: {e.stderr}")
except FileNotFoundError:
    print("TradingAgents not installed or scripts not found")
```

## Notes

- Analysis typically takes 3-10 minutes depending on complexity
- Reports are saved locally; no data is sent to external servers except LLM providers
- The `end_date` fix ensures the specified date's data is included (yfinance exclusive end date bug fixed)
- For Windows, reports are saved to `C:\Users\{user}\reports\{ticker}_{date}`