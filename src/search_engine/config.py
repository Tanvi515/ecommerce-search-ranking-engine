from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Main project directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Search configuration
DEFAULT_TOP_K = 10