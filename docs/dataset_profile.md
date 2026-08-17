# ABO Dataset Profile

## Dataset

Amazon Berkeley Objects (ABO)

## Records

- Metadata shards: 16
- Total records: 147,702
- Unique item IDs: 145,615
- Duplicate item ID occurrences: 2,087
- Exact duplicate records found: 0

## Important Fields

The primary fields selected for search are:

- item_id
- item_name
- brand
- product_type
- node
- bullet_point
- item_keywords
- model_number
- color

Optional fields:

- model_name
- material
- style
- item_weight
- item_dimensions

## Duplicate Handling

Duplicate `item_id` values are not automatically removed.

Inspection showed that duplicate records can represent different:

- marketplaces
- countries
- languages

Therefore, `item_id` alone will not be treated as the complete processed-record identity.

## Dataset Quality

Highly complete fields:

- item_id
- item_name
- product_type
- country
- marketplace
- domain_name
- brand

Highly sparse fields such as `product_description`, `finish_type`, `pattern`, `model_year`, and `3dmodel_id` will not be primary search fields.

## License

Amazon Berkeley Objects is distributed under the Creative Commons Attribution 4.0 International Public License (CC BY 4.0).

Dataset source:

https://amazon-berkeley-objects.s3.amazonaws.com/index.html