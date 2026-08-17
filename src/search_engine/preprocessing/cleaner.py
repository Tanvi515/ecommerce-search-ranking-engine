import re


def extract_values(field):
    """Extract text values from an ABO list of dictionaries."""
    if not isinstance(field, list):
        return []

    values = []

    for item in field:
        if isinstance(item, dict):
            value = item.get("value")

            if value is not None:
                values.append(str(value).strip())

    return values


def extract_first_value(field):
    """Return the first extracted value from an ABO field."""
    values = extract_values(field)

    return values[0] if values else None


def extract_category(record):
    """Extract the first category name from the ABO node field."""
    nodes = record.get("node", [])

    if not isinstance(nodes, list):
        return None

    for node in nodes:
        if isinstance(node, dict):
            category = node.get("node_name")

            if category:
                return str(category).strip()

    return None


def extract_language(record):
    """Extract the language tag from the first multilingual field."""
    multilingual_fields = [
        "item_name",
        "brand",
        "bullet_point",
        "color",
        "item_keywords",
    ]

    for field_name in multilingual_fields:
        field = record.get(field_name, [])

        if isinstance(field, list):
            for item in field:
                if isinstance(item, dict):
                    language = item.get("language_tag")

                    if language:
                        return language

    return None

def repair_encoding(text):
    """Repair common UTF-8 text that was incorrectly decoded as Latin-1."""
    if text is None:
        return None

    text = str(text)

    mojibake_markers = (
        "Ã",
        "Â",
        "â€",
        "ðŸ",
    )

    if any(marker in text for marker in mojibake_markers):
        try:
            repaired = text.encode("latin1").decode("utf-8")
            return repaired
        except (UnicodeEncodeError, UnicodeDecodeError):
            return text

    return text

def normalize_text(text):
    """Repair common encoding issues and normalize whitespace."""
    if text is None:
        return None

    text = repair_encoding(text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def build_listing_id(record, language):
    """Create a deterministic identifier for a marketplace listing."""
    item_id = record.get("item_id", "")
    marketplace = record.get("marketplace", "")
    country = record.get("country", "")

    parts = [
        item_id,
        marketplace,
        country,
        language or "",
    ]

    return "::".join(
        normalize_text(part) or ""
        for part in parts
    )


def clean_record(record):
    """Convert one raw ABO record into our canonical product schema."""
    language = extract_language(record)

    cleaned_record = {
        "listing_id": build_listing_id(record, language),
        "item_id": record.get("item_id"),
        "title": extract_first_value(record.get("item_name")),
        "brand": extract_first_value(record.get("brand")),
        "bullet_points": extract_values(record.get("bullet_point")),
        "keywords": extract_values(record.get("item_keywords")),
        "product_type": extract_first_value(record.get("product_type")),
        "category": extract_category(record),
        "color": extract_first_value(record.get("color")),
        "style": extract_first_value(record.get("style")),
        "material": extract_first_value(record.get("material")),
        "model_name": extract_first_value(record.get("model_name")),
        "model_number": extract_first_value(record.get("model_number")),
        "country": record.get("country"),
        "marketplace": record.get("marketplace"),
        "domain_name": record.get("domain_name"),
        "language": language,
    }

    # Normalize text fields.
    text_fields = [
        "title",
        "brand",
        "product_type",
        "category",
        "color",
        "style",
        "material",
        "model_name",
        "model_number",
        "country",
        "marketplace",
        "domain_name",
        "language",
    ]

    for field in text_fields:
        cleaned_record[field] = normalize_text(
            cleaned_record[field]
        )

    cleaned_record["bullet_points"] = [
        normalize_text(value)
        for value in cleaned_record["bullet_points"]
    ]

    cleaned_record["keywords"] = [
        normalize_text(value)
        for value in cleaned_record["keywords"]
    ]

    return cleaned_record