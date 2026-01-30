import openai
import json
import os

class AvailabilityAgent:
    def __init__(self):
        # Use Bytez API (OpenAI compatible)
        self.client = openai.OpenAI(
            api_key=os.getenv("BYTEZ_API_KEY"),
            base_url="https://api.bytez.com/models/v2/openai/v1/"
        )

    def run(self, city: str, country: str) -> dict:
        prompt = f"""
        You are a construction materials expert.

        Given the location:
        City: {city}
        Country: {country}

        List construction materials in three categories:
        1. Easy to source locally
        2. Limited availability
        3. Mostly imported

        Return ONLY valid JSON with keys:
        easy_to_get, limited, import_only
        """
        
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o-mini",  # Using a cost-effective model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that always returns valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = response.choices[0].message.content
            
            # Extract JSON from response
            start = result.index("{")
            end = result.rindex("}") + 1
            return json.loads(result[start:end])
        except Exception as e:
            return {"error": f"Error in AvailabilityAgent: {e}"}

if __name__ == "__main__":
    agent = AvailabilityAgent()
    result = agent.run("Lahore", "Pakistan")
    print(result)
