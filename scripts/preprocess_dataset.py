import re
import gzip
import json
from pathlib import Path

from src.search_engine.preprocessing.cleaner import clean_record


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Raw ABO metadata
METADATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "listings"
    / "metadata"
)

# Processed dataset output
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "products.jsonl"


def get_metadata_files():
    """Return all ABO metadata shard files."""
    return sorted(METADATA_DIR.glob("listings_*.json.gz"))


def preprocess_dataset():
    """Clean all ABO records and write them as JSONL."""
    files = get_metadata_files()

    if not files:
        print("No ABO metadata files found.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_records = 0
    processed_records = 0
    failed_records = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as output_file:

        for file_path in files:
            print(f"Processing: {file_path.name}")

            with gzip.open(file_path, "rt", encoding="utf-8") as input_file:

                for line in input_file:
                    total_records += 1

                    try:
                        raw_record = json.loads(line)
                        cleaned_record = clean_record(raw_record)
                        print("DEBUG CATEGORY:", repr(cleaned_record["category"]))

                        output_file.write(
                            json.dumps(
                                cleaned_record,
                                ensure_ascii=False,
                            )
                            + "\n"
                        )

                        processed_records += 1

                    except (json.JSONDecodeError, TypeError, ValueError) as error:
                        failed_records += 1

                        print(
                            f"Failed record in {file_path.name}: {error}"
                        )

    print("\n" + "=" * 50)
    print("PREPROCESSING COMPLETE")
    print("=" * 50)

    print(f"Input records:     {total_records}")
    print(f"Processed records: {processed_records}")
    print(f"Failed records:    {failed_records}")
    print(f"Output:            {OUTPUT_FILE}")


if __name__ == "__main__":
    preprocess_dataset()