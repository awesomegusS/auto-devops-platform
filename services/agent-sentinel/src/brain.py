import os
import json
from openai import OpenAI
from loguru import logger

class Brain:
    def __init__(self):
        # We load the config from env
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1") # Default to OpenAI if not set
        self.model = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

        if not api_key or "placeholder" in api_key:
            logger.warning("⚠️ No valid API Key found! Agent will run in 'Mock Mode'.")
            self.client = None
        else:
            # The 'openai' library works with any provider using the same standard!
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            logger.info(f"🧠 Brain connected to {base_url} using model {self.model}")

    def analyze_logs(self, logs: str) -> dict:
        if not self.client:
            return self._mock_analysis()

        prompt = f"""
        You are a Site Reliability Engineer (SRE).
        Analyze the following server logs and identify the root cause of the failure.
        
        LOGS:
        {logs}
        
        Respond ONLY with a valid JSON object in this format:
        {{
            "root_cause": "brief explanation",
            "suggested_action": "restart" | "ignore",
            "confidence": 0.0 to 1.0
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful SRE assistant that speaks JSON."},
                    {"role": "user", "content": prompt}
                ],
                # Note: 'response_format' is specific to OpenAI/Groq recent models. 
                # If using an older model, you might need to remove this line.
                response_format={"type": "json_object"}, 
                temperature=0
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.error(f"Brain freeze! LLM failed: {e}")
            return {"suggested_action": "ignore", "root_cause": "LLM Error"}

    def _mock_analysis(self):
        
        return {
            "root_cause": "Simulated Process Crash",
            "suggested_action": "restart",
            "confidence": 0.99
        }