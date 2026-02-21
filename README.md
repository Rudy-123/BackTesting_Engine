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
