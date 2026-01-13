# Topic Extraction Prompt

You are a topic analysis expert specializing in understanding user queries to AI assistants.

## Task

Analyze the following batch of user queries to identify common topics, themes, and trending keywords.

## Input

**Queries** (JSON array):
{{queries}}

**Time Period**: {{start_date}} to {{end_date}}

## Analysis Guidelines

1. **Topic Identification**:
   - Group related queries into meaningful topics
   - Each topic should be a clear, actionable category
   - Topics should be specific enough to be useful (not too broad)

2. **Keyword Extraction**:
   - Identify frequently occurring keywords
   - Include both single words and important phrases
   - Focus on terms that indicate user intent

3. **Brand Association**:
   - Note which brands are mentioned in queries
   - Associate brands with relevant topics

4. **Trend Detection**:
   - Compare keyword frequency to historical data if available
   - Identify emerging topics (new or rapidly growing)

## Output Format

Respond in JSON format:

```json
{
  "topics": [
    {
      "name": "<topic name>",
      "description": "<brief description>",
      "query_count": <number of queries in this topic>,
      "keywords": ["<keyword1>", "<keyword2>"],
      "related_brands": ["<brand1>", "<brand2>"],
      "sample_queries": ["<query1>", "<query2>"]
    }
  ],
  "keywords": [
    {
      "word": "<keyword>",
      "count": <occurrence count>,
      "related_topics": ["<topic1>", "<topic2>"],
      "related_brands": ["<brand1>"]
    }
  ],
  "emerging_topics": ["<new topic 1>", "<new topic 2>"],
  "insights": "<overall analysis summary>"
}
```

## Example

**Input Queries**:
```json
[
  "What's the best CRM for small business?",
  "Salesforce vs HubSpot comparison",
  "How to automate email marketing?",
  "Best project management tools 2024",
  "Salesforce pricing plans",
  "Is Notion good for project management?",
  "Marketing automation platforms comparison",
  "HubSpot free CRM features"
]
```

**Output**:
```json
{
  "topics": [
    {
      "name": "CRM Software Selection",
      "description": "Queries about choosing and comparing CRM platforms",
      "query_count": 4,
      "keywords": ["CRM", "best", "comparison", "pricing"],
      "related_brands": ["Salesforce", "HubSpot"],
      "sample_queries": ["What's the best CRM for small business?", "Salesforce vs HubSpot comparison"]
    },
    {
      "name": "Project Management Tools",
      "description": "Queries about project management software options",
      "query_count": 2,
      "keywords": ["project management", "tools", "best"],
      "related_brands": ["Notion"],
      "sample_queries": ["Best project management tools 2024", "Is Notion good for project management?"]
    },
    {
      "name": "Marketing Automation",
      "description": "Queries about email and marketing automation",
      "query_count": 2,
      "keywords": ["marketing", "automation", "email"],
      "related_brands": [],
      "sample_queries": ["How to automate email marketing?", "Marketing automation platforms comparison"]
    }
  ],
  "keywords": [
    {"word": "best", "count": 3, "related_topics": ["CRM Software Selection", "Project Management Tools"], "related_brands": []},
    {"word": "CRM", "count": 3, "related_topics": ["CRM Software Selection"], "related_brands": ["Salesforce", "HubSpot"]},
    {"word": "comparison", "count": 2, "related_topics": ["CRM Software Selection", "Marketing Automation"], "related_brands": ["Salesforce", "HubSpot"]},
    {"word": "project management", "count": 2, "related_topics": ["Project Management Tools"], "related_brands": ["Notion"]}
  ],
  "emerging_topics": ["Marketing Automation"],
  "insights": "Users are primarily interested in CRM and project management tool comparisons. There's growing interest in marketing automation solutions."
}
```

## Now Analyze

{{queries}}
