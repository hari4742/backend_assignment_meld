from openai import OpenAI
import json
import re
from app.core.config import settings

OPEN_AI_API_KEY = settings.OPENAI_API_KEY
OPEN_AI_MODEL = settings.OPENAI_MODEL


def analyze_sentiment_with_llm(review_text: str, stars: int):
    if not OPEN_AI_API_KEY:
        raise ValueError(
            "OpenAI API key is not set. Please configure it in the .env file.")

    sys_prompt = f'''
You are an expert in sentiment analysis. Given a product review and its corresponding star rating, analyze the review to determine its sentiment and emotional tone. 

## Examples:

### Example Input 1:
- Review: "This product exceeded my expectations! Totally worth it."
- Star Rating: 9

### Example Output 1:
```json
{{
  "sentiment": "Very Positive",
  "tone": "Joyful"
}}
```

### Instructions:
1. Classify the overall **sentiment** into one of the following categories: ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"].
2. Identify the primary **emotional tone**, choosing from: ["Joyful", "Angry", "Sad", "Fearful", "Surprised", "Trusting", "Disgusted", "Neutral"].
3. Return the analysis results strictly in the following JSON format:

```json
{{
  "sentiment": "<sentiment_category>",
  "tone": "<tone_category>"
}}
```
'''

    user_prompt = f'''Begin!

### Input:
- Review: "{review_text}"
- Star Rating: {stars} (out of 10)

### Output:'''

    try:
        client = OpenAI(api_key=OPEN_AI_API_KEY)

        response = client.chat.completions.create(
            model=OPEN_AI_MODEL,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])

        sentiment_analysis = response.choices[0].message.content.strip()

        result = parse_sentiment_output(sentiment_analysis)
        return result.get('sentiment'), result.get('tone')

    except Exception as e:
        print(f"Error while analyzing sentiment: {e}")

    return None, None


def parse_sentiment_output(json_output: str) -> dict:
    try:
        clean_json = re.sub(r'```json\s*|\s*```', '',
                            json_output.strip(), flags=re.IGNORECASE)
        result_dict = json.loads(clean_json)
        return result_dict or {}
    except json.JSONDecodeError:
        print("Invalid JSON string provided.")
        return {}
