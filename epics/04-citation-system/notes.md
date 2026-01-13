# Notes: 引文系统

## Citation Extraction Patterns

### URL Patterns

```python
URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'
DOMAIN_PATTERN = r'(?:according to |source: |from )([a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z]{2,})+)'
```

### Citation Types

1. **Explicit URL**: Direct URL in response
2. **Domain Reference**: "According to example.com..."
3. **Named Source**: "According to Wikipedia..."
4. **Implicit**: Content clearly from a source but not cited

## Source Authority Scoring

| Source Type | Base Score |
|-------------|------------|
| Official .gov/.edu | 90 |
| Major news outlets | 80 |
| Wikipedia | 75 |
| Industry publications | 70 |
| Blogs/Personal sites | 50 |
| Social media | 40 |

## Website Analysis API

### POST /api/citation/analyze

Request:
```json
{
  "url": "https://example.com",
  "depth": 1  // pages to analyze
}
```

Response:
```json
{
  "url": "https://example.com",
  "analysis_id": "abc123",
  "status": "processing",
  "estimated_time": 30
}
```

### GET /api/citation/analyze/{analysis_id}

Response:
```json
{
  "url": "https://example.com",
  "status": "completed",
  "results": {
    "citation_count": 15,
    "citation_contexts": [
      {
        "query": "best CRM software",
        "response_snippet": "...example.com recommends...",
        "sentiment": 0.8
      }
    ],
    "recommendations": [
      "Add more structured data markup",
      "Improve content on topic X"
    ]
  }
}
```

## Links & Resources

- URL Regex Patterns: https://mathiasbynens.be/demo/url-regex
- Web Scraping Best Practices: TBD
