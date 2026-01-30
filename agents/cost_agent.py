import openai
import json
import os

class CostAgent:
    def __init__(self):
        # Use Bytez API (OpenAI compatible)
        self.client = openai.OpenAI(
            api_key=os.getenv("BYTEZ_API_KEY"),
            base_url="https://api.bytez.com/models/v2/openai/v1/"
        )

    def run(self, materials: list, location: str) -> dict:
        prompt = f"""
        You are a construction cost analyst.

        Given these materials:
        {', '.join(materials)}

        In location: {location}

        Provide cost analysis for each material (relative cost: low/medium/high).
        Consider availability and transportation costs.

        Return ONLY valid JSON with format:
        {{
            "material_name": {{"relative_cost": "low|medium|high", "estimated_price_per_unit": "estimate", "notes": "brief note"}}
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
            return {"error": f"Error in CostAgent: {e}"}

if __name__ == "__main__":
    agent = CostAgent()
    result = agent.run(["concrete", "steel"], "Lahore")
    print(result)
