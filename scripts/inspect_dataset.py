# import gzip
# import json
# from pathlib import Path


# # Project root directory
# PROJECT_ROOT = Path(__file__).resolve().parents[1]

# # First ABO metadata file
# DATA_FILE = (
#     PROJECT_ROOT
#     / "data"
#     / "raw"
#     / "listings"
#     / "metadata"
#     / "listings_0.json.gz"
# )


# def inspect_first_record():
#     print(f"Reading: {DATA_FILE}")

#     with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
#         first_line = file.readline()

#     print(f"Read {len(first_line)} characters.")

#     record = json.loads(first_line)

#     print("\nRecord type:", type(record).__name__)
#     print("\nFields:")

#     for field in record.keys():
#         print(f" - {field}")


# if __name__ == "__main__":
#     inspect_first_record()

import gzip
import json
from collections import Counter
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ABO metadata directory
METADATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "listings"
    / "metadata"
)


def get_metadata_files():
    """Return all ABO metadata shard files."""
    return sorted(METADATA_DIR.glob("listings_*.json.gz"))


def inspect_dataset():
    files = get_metadata_files()

    if not files:
        print("No ABO metadata files found.")
        return

    total_records = 0
    item_ids = set()

    field_counter = Counter()
    missing_counter = Counter()
    brand_counter = Counter()
    product_type_counter = Counter()

    for file_path in files:
        print(f"Reading: {file_path.name}")

        with gzip.open(file_path, "rt", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)
                total_records += 1

                # Track item IDs
                item_id = record.get("item_id")

                if item_id:
                    item_ids.add(item_id)

                # Track fields and missing values
                for field in record:
                    field_counter[field] += 1

                    if not record[field]:
                        missing_counter[field] += 1

                # Track brands
                brands = record.get("brand", [])

                for brand in brands:
                    if isinstance(brand, dict):
                        value = brand.get("value")

                        if value:
                            brand_counter[value] += 1

                # Track product types
                product_types = record.get("product_type", [])

                for product_type in product_types:
                    if isinstance(product_type, dict):
                        value = product_type.get("value")

                        if value:
                            product_type_counter[value] += 1

    duplicate_count = total_records - len(item_ids)

    print("\n" + "=" * 50)
    print("ABO DATASET INSPECTION")
    print("=" * 50)

    print(f"\nMetadata files: {len(files)}")
    print(f"Total records: {total_records}")
    print(f"Unique item IDs: {len(item_ids)}")
    print(f"Duplicate item IDs: {duplicate_count}")

    print("\nFields:")
    for field in sorted(field_counter):
        print(f" - {field}")

    print("\nTop brands:")
    for brand, count in brand_counter.most_common(10):
        print(f" - {brand}: {count}")

    print("\nTop product types:")
    for product_type, count in product_type_counter.most_common(10):
        print(f" - {product_type}: {count}")

def inspect_duplicates():
    """Analyze duplicate item IDs across marketplaces and languages."""
    records_by_id = {}

    duplicate_records = []
    exact_duplicate_count = 0

    for file_path in get_metadata_files():
        with gzip.open(file_path, "rt", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)
                item_id = record.get("item_id")

                if not item_id:
                    continue

                if item_id not in records_by_id:
                    records_by_id[item_id] = record
                    continue

                original = records_by_id[item_id]

                if record == original:
                    exact_duplicate_count += 1
                else:
                    duplicate_records.append((original, record))

    print("\n" + "=" * 50)
    print("DUPLICATE ANALYSIS")
    print("=" * 50)

    print(f"\nDuplicate record pairs: {len(duplicate_records)}")
    print(f"Exact duplicate records: {exact_duplicate_count}")

    different_marketplace = 0
    different_country = 0
    different_language = 0

    for original, duplicate in duplicate_records:
        if original.get("marketplace") != duplicate.get("marketplace"):
            different_marketplace += 1

        if original.get("country") != duplicate.get("country"):
            different_country += 1

        original_languages = {
            item.get("language_tag")
            for field in original.values()
            if isinstance(field, list)
            for item in field
            if isinstance(item, dict) and item.get("language_tag")
        }

        duplicate_languages = {
            item.get("language_tag")
            for field in duplicate.values()
            if isinstance(field, list)
            for item in field
            if isinstance(item, dict) and item.get("language_tag")
        }

        if original_languages != duplicate_languages:
            different_language += 1

    print(f"Different marketplace: {different_marketplace}")
    print(f"Different country: {different_country}")
    print(f"Different language: {different_language}")

all_fields = set()

def inspect_missing_values():
    """Analyze missing values across all ABO product records."""

    total_records = 0
    field_counter = Counter()
    missing_counter = Counter()

    # First pass: discover every field in the dataset
    for file_path in get_metadata_files():
        with gzip.open(file_path, "rt", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)

                total_records += 1

                for field in record:
                    field_counter[field] += 1

    all_fields = set(field_counter)

    # Second pass: count fields that are absent or empty
    for file_path in get_metadata_files():
        with gzip.open(file_path, "rt", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)

                for field in all_fields:
                    value = record.get(field)

                    if value is None or value == [] or value == "":
                        missing_counter[field] += 1

    print("\n" + "=" * 50)
    print("MISSING VALUE ANALYSIS")
    print("=" * 50)

    print(f"\nTotal records: {total_records}")

    print("\nField completeness:")

    for field in sorted(all_fields):
        missing = missing_counter[field]
        present = total_records - missing
        percentage = (missing / total_records) * 100

        print(
            f" - {field}: "
            f"{missing} missing "
            f"({percentage:.2f}%) "
            f"| {present} present"
        )
# if __name__ == "__main__":
#     inspect_dataset()

# if __name__ == "__main__":
#     inspect_duplicates()

if __name__ == "__main__":
    inspect_missing_values()