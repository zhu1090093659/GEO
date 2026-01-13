# Notes: 分析引擎

## Sentiment Analysis Prompt

```
Analyze the sentiment towards the brand "{brand}" in the following AI response.

Response:
{response}

Please provide:
1. Overall sentiment score (-1 to 1, where -1 is very negative, 0 is neutral, 1 is very positive)
2. Sentiment label (positive/neutral/negative)
3. Key phrases that indicate the sentiment
4. Brief explanation

Output as JSON:
{
  "score": 0.5,
  "label": "positive",
  "key_phrases": ["reliable", "recommended"],
  "explanation": "..."
}
```

## Topic Extraction Prompt

```
Analyze the following user queries to AI assistants and extract the main topics and keywords.

Queries:
{queries}

Please identify:
1. Main topics (categories)
2. Trending keywords
3. User intent patterns

Output as JSON:
{
  "topics": [
    {"name": "product comparison", "count": 15, "keywords": ["best", "vs", "compare"]}
  ],
  "keywords": [
    {"word": "best", "count": 20, "trend": "rising"}
  ]
}
```

## Competitor Analysis Logic

1. Identify competitors from user input or industry defaults
2. Query visibility scores for all competitors
3. Calculate relative rankings
4. Identify differentiating factors
5. Generate comparison report

## API Design

### GET /api/analysis/competitors

Query params:
- brand: string (required)
- competitors: string[] (optional, comma-separated)

Response:
```json
{
  "brand": "example",
  "competitors": [
    {
      "name": "competitor1",
      "visibility_score": 75.0,
      "mention_count": 100,
      "rank": 2
    }
  ],
  "brand_rank": 1,
  "brand_score": 85.0
}
```

### GET /api/analysis/sentiment

Query params:
- brand: string (required)
- start_date: date
- end_date: date

Response:
```json
{
  "brand": "example",
  "overall_sentiment": 0.65,
  "sentiment_distribution": {
    "positive": 60,
    "neutral": 30,
    "negative": 10
  },
  "trend": [...]
}
```

## Links & Resources

- Sentiment Analysis Best Practices: TBD
- Topic Modeling with LLMs: TBD
