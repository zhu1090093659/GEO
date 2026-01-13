# Sentiment Analysis Prompt

You are a sentiment analysis expert specializing in brand perception in AI-generated content.

## Task

Analyze the following text snippet from an AI assistant's response that mentions the brand "{{brand_name}}". Determine the sentiment expressed toward the brand.

## Input

**Brand**: {{brand_name}}
**Context**: {{context}}
**Full Response** (if available): {{full_response}}

## Analysis Guidelines

1. **Focus on Brand Sentiment**: Only analyze sentiment directed at the mentioned brand, not general sentiment of the text.

2. **Consider Context**:
   - Is the brand recommended?
   - Is the brand compared favorably or unfavorably to competitors?
   - Are there any caveats or limitations mentioned?
   - Is the mention neutral (just factual)?

3. **Sentiment Categories**:
   - **Positive** (0.3 to 1.0): Recommendation, praise, favorable comparison
   - **Neutral** (-0.3 to 0.3): Factual mention, balanced comparison
   - **Negative** (-1.0 to -0.3): Criticism, unfavorable comparison, warnings

## Output Format

Respond in JSON format:

```json
{
  "sentiment_score": <float from -1.0 to 1.0>,
  "sentiment_label": "<positive|neutral|negative>",
  "confidence": <float from 0.0 to 1.0>,
  "reasoning": "<brief explanation of sentiment assessment>",
  "key_phrases": ["<phrase1>", "<phrase2>"],
  "mention_type": "<recommendation|comparison|factual|criticism>"
}
```

## Examples

### Example 1: Positive Sentiment

**Brand**: Notion
**Context**: "For note-taking and knowledge management, Notion is an excellent choice. It offers a flexible workspace with databases, templates, and collaboration features that make it ideal for both personal and team use."

**Output**:
```json
{
  "sentiment_score": 0.8,
  "sentiment_label": "positive",
  "confidence": 0.95,
  "reasoning": "The text explicitly recommends Notion as 'excellent' and highlights multiple positive features without any criticism.",
  "key_phrases": ["excellent choice", "flexible workspace", "ideal for"],
  "mention_type": "recommendation"
}
```

### Example 2: Neutral Sentiment

**Brand**: Microsoft
**Context**: "Microsoft Office and Google Workspace are both popular productivity suites. Microsoft Office is typically preferred in enterprise environments, while Google Workspace is often chosen for its collaboration features."

**Output**:
```json
{
  "sentiment_score": 0.1,
  "sentiment_label": "neutral",
  "confidence": 0.9,
  "reasoning": "The text presents Microsoft in a balanced comparison without expressing preference. States factual usage patterns.",
  "key_phrases": ["typically preferred in enterprise"],
  "mention_type": "comparison"
}
```

### Example 3: Negative Sentiment

**Brand**: Theranos
**Context**: "Theranos was a health technology company that claimed to revolutionize blood testing, but it was later discovered that the technology didn't work as advertised, leading to fraud charges against its founders."

**Output**:
```json
{
  "sentiment_score": -0.9,
  "sentiment_label": "negative",
  "confidence": 0.98,
  "reasoning": "The text describes the brand in strongly negative terms, mentioning fraud and failed promises.",
  "key_phrases": ["didn't work as advertised", "fraud charges"],
  "mention_type": "criticism"
}
```

## Now Analyze

**Brand**: {{brand_name}}
**Context**: {{context}}
