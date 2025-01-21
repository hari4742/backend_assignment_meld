import openai
from app.core.config import settings

OPEN_AI_API_KEY = settings.OPENAI_API_KEY
OPEN_AI_MODEL = settings.OPENAI_MODEL


def analyze_sentiment_with_llm(review_text: str, stars: int):
    if not OPEN_AI_API_KEY:
        raise ValueError(
            "OpenAI API key is not set. Please configure it in the .env file.")

    # TODO: improve prompt
    prompt = f"""
    Given the following review text: "{review_text}" and the star rating: {stars},
    determine the tone (e.g. Positive, Negative, Neutral) and sentiment of the review.
    """

    try:
        response = openai.ChatCompletion.create(
            model=OPEN_AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            api_key=OPEN_AI_API_KEY
        )

        sentiment_analysis = response['choices'][0]['message']['content'].strip().split(
            "\n")

        # TODO: improve extraction of results from response
        if len(sentiment_analysis) == 2:
            tone, sentiment = sentiment_analysis
            return tone.strip(), sentiment.strip()

    except Exception as e:
        print(f"Error while analyzing sentiment: {e}")

    return None, None
