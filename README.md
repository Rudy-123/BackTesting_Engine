⚡ BackTesting Engine
Quantitative Strategy Backtesting Framework with Cloud-Native Data Pipeline
📖 Project Overview
BackTesting Engine is a high-performance, config-driven quantitative backtesting framework designed to evaluate trading strategies at scale. It executes grid search across 64+ strategy parameter combinations using batched multiprocessing with a shared-nothing architecture.

The system transitioned from a naive crossover approach to a Regime-Aware Strategy, transforming a -$39,000 baseline loss into a potential +$17,800 profit through advanced risk management, volatility filtering, and momentum validation.

The system ingests live and historical BTCUSDT 15-minute candle data from the Binance API through a fully automated, event-driven AWS pipeline — using Lambda, EventBridge, and S3 — and feeds it into a Dockerized backtesting engine for reproducible, deterministic experimentation.

🏗️ System Architecture
The system follows a two-stage architecture: an automated cloud data ingestion pipeline, and a local Dockerized backtesting engine that consumes the collected data.

High-Level Architecture Flow
mermaid
graph TD
    classDef cloud fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px
    classDef aws fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef engine fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef output fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#b71c1c,stroke-width:2px
    subgraph Cloud Pipeline
        EB["⏰ EventBridge Scheduler"]:::aws
        Lambda["⚙️ AWS Lambda"]:::aws
        Binance["📡 Binance API"]:::cloud
        S3["🪣 S3 Bucket"]:::aws
    end
    subgraph Local Machine
        Sync["🔄 AWS CLI Sync"]:::data
        Scripts["🛠️ Data Processing Scripts"]:::data
        Parquet["📦 Parquet Dataset"]:::data
    end
    subgraph Dockerized Engine
        Config["📋 YAML Config"]:::engine
        Factory["🏭 Strategy Factory"]:::engine
        JobBuilder["🔧 Job Builder"]:::engine
        BatchRunner["⚡ Batch Runner"]:::engine
        Workers["👷 Parallel Workers"]:::engine
        BTE["🧠 Backtesting Engine"]:::engine
    end
    subgraph Reporting
        JSON["📄 JSON Results"]:::output
        CSV["📊 Summary CSV"]:::output
        Plots["📈 Equity & Drawdown Plots"]:::output
    end
    EB -->|"Cron Trigger"| Lambda
    Lambda -->|"Fetch 15m Candles"| Binance
    Binance -->|"OHLCV Data"| Lambda
    Lambda -->|"Store CSV"| S3
    S3 -->|"aws s3 sync"| Sync
    Sync --> Scripts
    Scripts -->|"Merge + Clean"| Parquet
    Parquet --> Config
    Config --> Factory
    Factory --> JobBuilder
    JobBuilder --> BatchRunner
    BatchRunner -->|"Multiprocessing Pool"| Workers
    Workers --> BTE
    BTE --> JSON
    BTE --> CSV
    BTE --> Plots
📊 Results & Performance
The engine's primary objective was to optimize a standard Moving Average crossover into a robust, tradeable strategy.

The PnL Turnaround
Original baseline strategies often yielded significant losses due to "choppy" markets. By implementing Regime Filtering and Dynamic Stop Losses, we achieved a major performance shift:

Metric	Naive Strategy (Baseline)	Optimized Regime-Aware
Total PnL	-$39,120	+$17,855
Win Rate	21.0%	28.3%
Max Drawdown	-$41,881	-$11,406
Stop Loss	Fixed 1.0%	Dynamic 2.5x ATR
Top Performing Strategy (Summary)
Data extracted from latest 64-run grid search (
results/summary.csv
)

Strategy ID	Short/Long	Total PnL	Max Drawdown	PnL/DD Ratio
ma_25_110	25 / 110	$17,855.17	-$11,406	1.56
ma_25_120	25 / 120	$13,130.36	-$9,846	1.33
ma_20_110	20 / 110	$12,012.50	-$14,460	0.83
⚙️ Strategy Logic: "The Regime SNIPER"
The strategy doesn't just look for crosses; it validates them against the current market "regime" to avoid false signals in flat markets.

1. The 4-Stage Entry Filter
Before a BUY signal is issued, the market must pass four strict tests:

EMA 200 Slope (The Trend): Today's EMA must be higher than 10 candles ago (Ensures a real uptrend).
ATR Volatility Filter (The Wake-Up): Today's range (ATR) must be > 80% of the 20-period average (Market must be "awake").
RSI Momentum (Hype Meter): RSI-14 must be between 50 and 75 (Strong pulse, not yet overbought).
Strict Crossover: Fast MA must cross above Slow MA on the current candle, not just be above it.
2. The Dynamic Safety Net (ATR Stop Loss)
Instead of a fixed percentage, the strategy uses Average True Range (ATR) to set volatility-adjusted stops: Stop Price = Entry Price - (2.5 * ATR) This allows the trade room to breathe during high volatility and tightens up during steady trends.

☁️ Cloud Data Ingestion Pipeline
The data pipeline is fully serverless, designed for zero-maintenance continuous data collection.

Pipeline Flow
mermaid
sequenceDiagram
    participant EB as EventBridge
    participant Lambda as AWS Lambda
    participant Binance as Binance API
    participant S3 as S3 Bucket
    participant Local as Local Machine
    EB->>Lambda: Trigger every 15 minutes
    Lambda->>Binance: GET /api/v3/klines (BTCUSDT, 15m)
    Binance-->>Lambda: OHLCV candle data
    Lambda->>S3: PUT object (partitioned CSV)
    Note over S3: s3://project-backtesting-data/raw/symbol=BTCUSDT/
    Local->>S3: aws s3 sync
    S3-->>Local: Download new candle files
⚡ Engineering & Optimization
High-Performance Runner
Shared-Nothing Multiprocessing: Each worker process is completely isolated, loading its own data to avoid GIL (Global Interpreter Lock) contention.
Batched Execution: Jobs are chunked into batches matching CPU core counts for 100% hardware utilization.
Runtime Reduction: Achieved ~65% reduction in total execution time compared to serial processing.
Data Efficiency
Parquet Adoption: Data loading speed increased by ~60% by switching from CSV to Snappy-compressed Parquet.
Year-Partitioning: Enables selective reading for specific year segments, slashing I/O overhead.
~65% Storage Reduction: Columnar Parquet format significantly reduces disk footprint compared to raw CSV.
📁 Project Structure
BackTesting_Engine/
├── Engine/                          # Core backtesting engine
│   ├── backtesting_engine.py        # Main event loop
│   ├── data_loader.py               # Format-agnostic data loader
│   ├── datafeed.py                  # Candle-by-candle iterator
│   ├── execution.py                 # Slippage + commission simulator
│   ├── portfolio.py                 # Position & risk management
│   └── metrics.py                   # PnL, win rate, drawdown
│
├── Strategies/                      # Trading strategy implementations
│   ├── basic_strategy.py            # Abstract base strategy
│   └── ma_crossover.py             # MA Crossover with EMA regime filter
│
├── Runner/                          # Parallel execution framework
│   ├── config_loader.py             # YAML config parser
│   ├── strategy_factory.py          # Parameter grid generator
│   ├── job_builder.py               # Isolated engine builder per job
│   ├── batch_runner.py              # Batched multiprocessing dispatcher
│   ├── parallel_runner.py           # Direct parallel runner
│   └── worker.py                    # Shared-nothing worker process
│
├── reporting/                       # Output & analytics pipeline
│   ├── result_writer.py             # JSON + CSV result persistence
│   ├── plots.py                     # Equity & drawdown curve generator
│   └── analytics.py                 # Post-run enrichment & ranking
│
├── Scripts/                         # Data processing utilities
│   ├── build_final_dataset.py       # Bootstrap + live data merger
│   ├── bootstrap_merge.py           # Historical data format handler
│   ├── csv_to_parquet.py            # CSV → Parquet converter
│   └── csv_to_partitioned_parquet.py# Year-partitioned Parquet builder
│
├── tools/
│   └── generate_report.py           # Clean + run + report pipeline
│
├── config/
│   └── experiment.yaml              # Strategy grid & engine configuration
│
├── data/                            # Market data (Raw S3 + Processed Parquet)
├── results/                         # Ranked CSVs & Equity Curve PNGs
├── Dockerfile                       # Container specification
├── main.py                          # Entry point
└── requirements.txt                 # Python dependencies
🚀 Getting Started
1. Sync Market Data from S3
bash
aws s3 sync s3://project-backtesting-data/raw/ ./data/raw/
2. Build & Merge Dataset
bash
python Scripts/build_final_dataset.py
3. Run Backtesting Engine
bash
python main.py
4. Check Results
Check 
results/summary.csv
 for the top-ranked strategy variants.
Visual equity and drawdown curves can be found in results/plots/.
📄 License
This project is licensed under the MIT License.

⭐ Acknowledgements
BackTesting Engine was built to explore quantitative strategy evaluation, cloud-native data pipelines, high-performance parallel computation, and reproducible research environments using modern Python and AWS infrastructure.

