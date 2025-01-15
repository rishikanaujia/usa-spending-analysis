# API Improvement Proposals
These improvements focus on:
1. Reducing the number of API calls needed for common operations
2. Making the API more intuitive and consistent
3. Providing better error handling and guidance
4. Enhancing documentation with practical examples

## Overview

Based on implementation experience with the USASpending API, this document proposes improvements to enhance usability and efficiency according to the assignment requirements.

## 1. New Routes

### Combined State Analytics Endpoint
```http
GET /api/v2/recipient/state/analytics/{state_code}/
```

Purpose:
- Combine population and award data in single request
- Reduce API calls for common analyses
- Provide pre-calculated metrics

Example Response:
```json
{
  "fiscal_year": 2023,
  "state": {
    "name": "Texas",
    "code": "48",
    "population": 29527941
  },
  "awards": {
    "grants": {
      "amount": 1000000000,
      "count": 5000,
      "per_capita": 33.87
    },
    "loans": {
      "amount": 2000000000,
      "count": 7500,
      "per_capita": 67.73
    }
  },
  "rankings": {
    "grants_per_capita": 15,
    "total_awards": 3
  }
}
```

### Agency Overview Endpoint
```http
GET /api/v2/agency/{agency_code}/overview/{fiscal_year}/
```

Purpose:
- Consolidate agency performance metrics
- Provide historical comparisons
- Include common calculations

Example Response:
```json
{
  "fiscal_year": 2024,
  "agency": {
    "code": "080",
    "name": "National Aeronautics and Space Administration",
    "abbreviation": "NASA"
  },
  "budget": {
    "total_resources": 25000000000,
    "obligations": 15000000000,
    "available_balance": 10000000000
  },
  "awards": {
    "new_count": 1500,
    "total_value": 15000000000,
    "average_value": 10000000
  },
  "metrics": {
    "resource_utilization_ratio": 0.6,
    "average_award_size": 10000000,
    "year_over_year_change": 0.05
  }
}
```

## 2. Renaming Input Parameters

### Standardize Date Parameters
Current Issues:
- Inconsistent use of `year` vs `fiscal_year`
- Ambiguity between calendar and fiscal years
- Missing time period specifications

Proposed Changes:
```diff
# Before
/api/v2/recipient/state/{fips}?year=2023
/api/v2/agency/{toptier_code}/awards/new/count/?fiscal_year=2023

# After
/api/v2/recipient/state/{state_code}?fiscal_year=2023
/api/v2/agency/{agency_code}/awards/new/count/?fiscal_year=2023
```

### Improve Identifier Parameters
```diff
# State Identifiers
- fips
+ state_code

# Agency Identifiers
- TOPTIER_AGENCY_CODE
+ agency_code

# Account Identifiers
- aid
+ account_id
- ata
+ transfer_agency_id
```


## 3. Output Data Format Adjustments

### Standardized Response Structure
```json
{
  "metadata": {
    "fiscal_year": 2024,
    "last_updated": "2024-01-15T00:00:00Z",
    "version": "2.0"
  },
  "data": {
    // Response-specific data
  },
  "pagination": {
    "page": 1,
    "total_pages": 10,
    "total_items": 100,
    "items_per_page": 10
  }
}
```

### Enhanced Error Responses
```json
{
  "error": {
    "code": "INVALID_FISCAL_YEAR",
    "message": "Fiscal year 2025 not available",
    "suggestion": "Available fiscal years: 2019-2024",
    "details": {
      "valid_range": {"min": 2019, "max": 2024},
      "documentation_url": "https://api.usaspending.gov/docs/fiscal-years"
    }
  }
}
```

## 4. Documentation Enhancements

### Interactive Examples
- Provide code samples in multiple languages
- Include common use case examples

Example:
```markdown
### Get State Awards Example

```python
import requests

# Get Texas awards for FY 2023
response = requests.get(
    "https://api.usaspending.gov/api/v2/recipient/state/awards/48/",
    params={"fiscal_year": 2023}
)
```

### Parameter Documentation
```markdown
fiscal_year:
  - Valid range: 2000-present
  - Default: Current fiscal year
  - Note: Data typically available 45 days after year end
```

### Use Case Documentation
- Document common API call sequences
- Include performance considerations
- Provide best practices

Example:
```markdown
Common Use Case: Per-capita Analysis
1. Get state FIPS code
2. Get state population
3. Get award data
Performance note: Use new /analytics endpoint for single-call solution
```

### Relationship Documentation
- Document endpoint relationships
- Explain data hierarchies
- Provide visual API maps

Example:
```markdown
Agency Hierarchy:
1. Toptier Agency
2. Sub-Agency
3. Federal Account
4. Program Activity
```

