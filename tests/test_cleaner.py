from src.search_engine.preprocessing.cleaner import clean_record


def test_clean_record():
    raw_record = {
        "item_id": "B123456",
        "item_name": [
            {
                "language_tag": "en_US",
                "value": "  Test Product  ",
            }
        ],
        "brand": [
            {
                "language_tag": "en_US",
                "value": "Test Brand",
            }
        ],
        "bullet_point": [
            {
                "language_tag": "en_US",
                "value": "First feature",
            },
            {
                "language_tag": "en_US",
                "value": "Second feature",
            },
        ],
        "item_keywords": [
            {
                "language_tag": "en_US",
                "value": "test product",
            }
        ],
        "product_type": [
            {
                "value": "TEST_PRODUCT",
            }
        ],
        "node": [
            {
                "node_id": 123,
                "node_name": "/Categories/Test",
            }
        ],
        "color": [
            {
                "language_tag": "en_US",
                "value": "Blue",
            }
        ],
        "style": [],
        "material": [],
        "model_name": [],
        "model_number": [],
        "country": "US",
        "marketplace": "Amazon",
        "domain_name": "amazon.com",
    }

    result = clean_record(raw_record)

    assert result["item_id"] == "B123456"
    assert result["title"] == "Test Product"
    assert result["brand"] == "Test Brand"
    assert result["product_type"] == "TEST_PRODUCT"
    assert result["category"] == "/Categories/Test"
    assert result["color"] == "Blue"
    assert result["language"] == "en_US"

    assert result["bullet_points"] == [
        "First feature",
        "Second feature",
    ]

    assert result["keywords"] == ["test product"]

    assert result["style"] is None
    assert result["material"] is None
    assert result["model_name"] is None
    assert result["model_number"] is None

    assert result["listing_id"] == (
        "B123456::Amazon::US::en_US"
    )