import os
import json
from groq import Groq

class AiAnalyzer:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key) if api_key else None

    def analyze(self, code):
        if not self.client:
            return {
                'time_complexity': 'Unknown',
                'space_complexity': 'Unknown',
                'confidence': '0%',
                'explanation': 'Groq API Key missing. Please set GROQ_API_KEY in .env file.',
                'suggestions': 'No suggestions available.'
            }

        prompt = f"""
        Analyze the following Python code for algorithmic complexity and potential improvements.
        
        Code:
        ```python
        {code}
        ```
        
        Return a strictly valid JSON response (no markdown formatting) with the following keys:
        - "time_complexity": (e.g., "O(n)")
        - "space_complexity": (e.g., "O(1)")
        - "explanation": (Brief explanation of how complexity was derived)
        - "confidence": (Percentage string, e.g., "95%")
        - "suggestions": (A concise paragraph suggesting code improvements, safe practices, or pythonic refactors. Use natural language.)
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert algorithm analyst. You provide strict JSON output."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile", # Updated to supported model
                temperature=0.1,
            )
            
            response_content = chat_completion.choices[0].message.content.strip()
            # Attempt to clean potential markdown code blocks if the model hallucinates them
            if response_content.startswith("```json"):
                response_content = response_content[7:]
            if response_content.endswith("```"):
                response_content = response_content[:-3]
                
            return json.loads(response_content)

        except Exception as e:
            return {
                'time_complexity': 'Error',
                'space_complexity': 'Error',
                'confidence': '0%',
                'explanation': f'AI Analysis Failed: {str(e)}',
                'suggestions': 'Check API connection.'
            }
