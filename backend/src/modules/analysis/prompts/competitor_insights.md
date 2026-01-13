# Competitor Analysis Insights Prompt

You are a competitive intelligence analyst specializing in AI visibility and brand perception.

## Task

Generate strategic insights based on the competitive comparison data between a brand and its competitors in AI-generated responses.

## Input

**Target Brand**: {{brand_name}}
**Analysis Period**: {{start_date}} to {{end_date}}

**Brand Metrics**:
- Visibility Score: {{brand_visibility}}
- Mention Count: {{brand_mentions}}
- Average Sentiment: {{brand_sentiment}}
- Ranking: {{brand_rank}}

**Competitor Data** (JSON):
{{competitors_data}}

## Analysis Guidelines

1. **Visibility Analysis**:
   - Compare visibility scores across competitors
   - Identify leaders and laggards
   - Calculate market share of AI mentions

2. **Sentiment Analysis**:
   - Compare brand perception vs competitors
   - Identify sentiment gaps
   - Note any extreme positive/negative outliers

3. **Strategic Insights**:
   - What is the brand doing well?
   - Where are the improvement opportunities?
   - Which competitors pose the biggest threat?
   - What strategies might improve visibility?

4. **Actionable Recommendations**:
   - Provide 3-5 specific recommendations
   - Base recommendations on data, not assumptions
   - Prioritize by potential impact

## Output Format

Respond in JSON format:

```json
{
  "summary": "<2-3 sentence executive summary>",
  "key_findings": [
    "<finding 1>",
    "<finding 2>",
    "<finding 3>"
  ],
  "competitive_position": {
    "market_leader": "<brand name>",
    "market_share_estimate": "<percentage>",
    "position_vs_leader": "<ahead|behind|tied> by <X points>",
    "strongest_competitor": "<competitor name>",
    "weakest_competitor": "<competitor name>"
  },
  "sentiment_analysis": {
    "brand_vs_average": "<above|below|average>",
    "sentiment_gap": <float>,
    "perception_issues": ["<issue1>", "<issue2>"]
  },
  "opportunities": [
    {
      "area": "<opportunity area>",
      "rationale": "<why this is an opportunity>",
      "potential_impact": "<high|medium|low>"
    }
  ],
  "threats": [
    {
      "competitor": "<competitor name>",
      "threat_type": "<description>",
      "urgency": "<high|medium|low>"
    }
  ],
  "recommendations": [
    {
      "action": "<specific action to take>",
      "priority": <1-5>,
      "expected_outcome": "<what this will achieve>"
    }
  ]
}
```

## Example

**Target Brand**: Notion
**Brand Metrics**:
- Visibility Score: 75.5
- Mention Count: 234
- Average Sentiment: 0.65
- Ranking: 2

**Competitors**:
```json
[
  {"name": "Evernote", "visibility_score": 82.3, "mention_count": 312, "sentiment": 0.45, "rank": 1},
  {"name": "Obsidian", "visibility_score": 68.2, "mention_count": 156, "sentiment": 0.78, "rank": 3},
  {"name": "OneNote", "visibility_score": 45.1, "mention_count": 98, "sentiment": 0.32, "rank": 4}
]
```

**Output**:
```json
{
  "summary": "Notion holds a strong #2 position in AI recommendations for productivity tools, trailing Evernote by 7 points in visibility but outperforming on sentiment. The brand shows solid momentum with growth potential.",
  "key_findings": [
    "Notion ranks 2nd in visibility but has the 2nd highest sentiment score (0.65), suggesting strong user satisfaction",
    "Evernote leads in visibility (82.3) but has lower sentiment (0.45), indicating potential vulnerability",
    "Obsidian has the highest sentiment (0.78) but limited visibility, representing a niche threat"
  ],
  "competitive_position": {
    "market_leader": "Evernote",
    "market_share_estimate": "29%",
    "position_vs_leader": "behind by 6.8 points",
    "strongest_competitor": "Evernote",
    "weakest_competitor": "OneNote"
  },
  "sentiment_analysis": {
    "brand_vs_average": "above",
    "sentiment_gap": 0.1,
    "perception_issues": ["Occasionally mentioned as 'complex' for beginners"]
  },
  "opportunities": [
    {
      "area": "Overtake Evernote",
      "rationale": "Leader has sentiment issues; quality gap closing",
      "potential_impact": "high"
    },
    {
      "area": "Beginner-friendly positioning",
      "rationale": "Address complexity perception to capture more recommendations",
      "potential_impact": "medium"
    }
  ],
  "threats": [
    {
      "competitor": "Obsidian",
      "threat_type": "Growing enthusiast community with exceptional sentiment",
      "urgency": "medium"
    }
  ],
  "recommendations": [
    {
      "action": "Create more beginner tutorials and getting-started content",
      "priority": 1,
      "expected_outcome": "Address complexity perception, increase recommendation rate"
    },
    {
      "action": "Highlight unique features (databases, templates) in AI-optimized content",
      "priority": 2,
      "expected_outcome": "Differentiate from Evernote in AI responses"
    },
    {
      "action": "Improve SEO and AI-indexable documentation",
      "priority": 3,
      "expected_outcome": "Increase visibility score by 5-10 points"
    }
  ]
}
```

## Now Analyze

**Target Brand**: {{brand_name}}
{{brand_metrics}}
{{competitors_data}}
