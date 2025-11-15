"""AI-powered match summary generation using Anthropic API."""

import logging
import json
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class AISummaryGenerator:
    """Generates AI-powered summaries of football match results using Anthropic."""

    def __init__(self, api_key, model="claude-sonnet-4-20250514", timeout=30):
        """
        Initialize the AI summary generator.

        Args:
            api_key: Anthropic API key
            model: Model to use (default: claude-sonnet-4-20250514)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.client = Anthropic(api_key=api_key, timeout=timeout)
        logger.info(f"AISummaryGenerator initialized with model: {model}")

    def _build_prompt(self, matches_data):
        """
        Build system and user prompts for the AI.

        Args:
            matches_data: List of match dictionaries

        Returns:
            tuple: (system_prompt, user_prompt)
        """
        # System prompt - define the AI's role
        system_prompt = (
            "You are a sports journalist creating dramatic, headline-style summaries "
            "about recent football matches. Your headlines should be engaging, "
            "capture the most interesting storylines, and cover big wins, big losses, "
            "and notable performances across all competitions."
        )

        # Convert matches to JSON for the user prompt
        matches_json = json.dumps(matches_data, indent=2)

        # User prompt - instructions and data
        user_prompt = f"""Based on these recent matches from the last 7 days across the Premier League, La Liga, Bundesliga, Serie A, Ligue 1, and Champions League:

{matches_json}

Generate 3-7 dramatic, headline-style summaries that capture the most interesting storylines. Focus on:
- Big wins and shocking results
- Important matches (especially Champions League)
- Notable patterns or trends
- Surprising outcomes

Output only the headlines, one per line, with no numbering, bullets, or additional formatting. Keep each headline concise and impactful."""

        logger.debug(f"System prompt: {system_prompt}")
        logger.debug(f"User prompt length: {len(user_prompt)} characters")

        return system_prompt, user_prompt

    def generate_summary(self, matches_data):
        """
        Generate an AI summary of match results.

        Args:
            matches_data: List of match dictionaries with match information

        Returns:
            str: Generated summary text, or None on failure
        """
        logger.info(f"Summary generation requested for {len(matches_data)} matches")

        try:
            # Build prompts
            system_prompt, user_prompt = self._build_prompt(matches_data)
            logger.info("Prompts constructed successfully")

            # Log full prompt
            logger.info("=" * 80)
            logger.info("FULL PROMPT TO ANTHROPIC:")
            logger.info(f"System: {system_prompt}")
            logger.info(f"User: {user_prompt}")
            logger.info("=" * 80)

            # Call Anthropic API
            logger.info(f"Calling Anthropic API with model: {self.model}")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract text from response
            summary_text = response.content[0].text

            # Log full response
            logger.info("=" * 80)
            logger.info("FULL RESPONSE FROM ANTHROPIC:")
            logger.info(f"Model: {response.model}")
            logger.info(f"Stop reason: {response.stop_reason}")
            logger.info(f"Usage: {response.usage}")
            logger.info(f"Summary text:\n{summary_text}")
            logger.info("=" * 80)

            logger.info("Summary generated successfully")
            return summary_text

        except Exception as e:
            logger.error(f"Error generating summary: {e}", exc_info=True)
            return None
