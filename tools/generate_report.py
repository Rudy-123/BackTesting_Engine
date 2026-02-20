import shutil
from pathlib import Path
import sys

# Make sure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from main import main


def clean_results():
    results_path = PROJECT_ROOT / "results"

    if not results_path.exists():
        results_path.mkdir(parents=True, exist_ok=True)
        return

    # Delete contents inside results folder, not the folder itself
    for item in results_path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def run():
    print("Cleaning old results folder...")
    clean_results()

    print("Running full backtesting + reporting pipeline...\n")
    main()

    print("\nReport generation complete.")
    print("Check the 'results/' folder for JSON, CSV, and plots.")


if __name__ == "__main__":
    run()
