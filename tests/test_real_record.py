import gzip
import json

from src.search_engine.preprocessing.cleaner import clean_record


DATA_FILE = (
    "data/raw/listings/metadata/listings_0.json.gz"
)


def test_clean_real_record():
    with gzip.open(DATA_FILE, "rt", encoding="utf-8") as file:
        raw_record = json.loads(file.readline())

    result = clean_record(raw_record)

    assert result["item_id"]
    assert result["title"]
    assert result["product_type"]
    assert result["listing_id"]

    print("\nCleaned record:")
    print(json.dumps(result, indent=2, ensure_ascii=False))