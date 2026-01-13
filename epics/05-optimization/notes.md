# Notes: 优化建议系统

## Optimization Advisor Prompt

```
You are a GEO (Generative Engine Optimization) expert. Based on the following analysis data, provide actionable optimization recommendations.

Brand: {brand}
Current Visibility Score: {score}
Competitor Analysis: {competitor_data}
Sentiment Analysis: {sentiment_data}
Citation Analysis: {citation_data}

Please provide:
1. Top 5 optimization recommendations
2. For each recommendation:
   - Category (content/structure/technical)
   - Priority (P0/P1/P2)
   - Specific action steps
   - Expected impact
   - Estimated effort

Output as JSON:
{
  "recommendations": [
    {
      "id": 1,
      "title": "...",
      "category": "content",
      "priority": "P0",
      "description": "...",
      "action_steps": ["..."],
      "expected_impact": "...",
      "effort": "low/medium/high"
    }
  ]
}
```

## llms.txt Format

Based on https://llmstxt.org/:

```
# {Site Name}

> {Brief description}

## About

{Detailed description of the site/organization}

## Main Sections

- [Section 1](/path1): Description
- [Section 2](/path2): Description

## Key Topics

- Topic 1
- Topic 2

## Contact

- Website: {url}
- Email: {email}
```

## API Design

### GET /api/optimization/recommendations

Query params:
- brand: string (required)

Response:
```json
{
  "brand": "example",
  "generated_at": "2026-01-13T10:00:00Z",
  "recommendations": [
    {
      "id": 1,
      "title": "Improve product page content",
      "category": "content",
      "priority": "P0",
      "description": "Add more detailed product descriptions...",
      "action_steps": [
        "Review current product descriptions",
        "Add key features and benefits",
        "Include comparison with alternatives"
      ],
      "expected_impact": "15-20% visibility improvement",
      "effort": "medium"
    }
  ]
}
```

### POST /api/optimization/llms-txt

Request:
```json
{
  "url": "https://example.com",
  "site_name": "Example Corp",
  "description": "...",
  "auto_generate": true
}
```

Response:
```json
{
  "content": "# Example Corp\n\n> ...",
  "preview_url": "/preview/llms-txt/abc123",
  "download_url": "/download/llms-txt/abc123"
}
```

## Recommendation Categories

| Category | Examples |
|----------|----------|
| Content | Improve descriptions, add FAQs, update outdated info |
| Structure | Add schema markup, improve navigation, create sitemap |
| Technical | Improve page speed, add llms.txt, fix broken links |

## Links & Resources

- llms.txt Specification: https://llmstxt.org/
- Schema.org Markup: https://schema.org/
