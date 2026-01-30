import openai
import json
import os

class DurabilityAgent:
    def __init__(self):
        # Use Bytez API (OpenAI compatible)
        self.client = openai.OpenAI(
            api_key=os.getenv("BYTEZ_API_KEY"),
            base_url="https://api.bytez.com/models/v2/openai/v1/"
        )

    def run(self, materials: list, climate: str) -> dict:
        prompt = f"""
        You are a materials durability expert.

        Given these materials:
        {', '.join(materials)}

        In climate: {climate}

        Analyze expected lifespan and durability (in years).
        Consider maintenance requirements and resistance to local conditions.

        Return ONLY valid JSON with format:
        {{
            "material_name": {{"lifespan_years": 0, "maintenance": "low|medium|high", "notes": "brief note"}}
        }}
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
            start = result.index("{")
            end = result.rindex("}") + 1
            return json.loads(result[start:end])
        except Exception as e:
            return {"error": f"Error in DurabilityAgent: {e}"}

if __name__ == "__main__":
    agent = DurabilityAgent()
    result = agent.run(["concrete", "brick"], "tropical")
    print(result)
