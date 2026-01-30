import openai
import json
import os

class CarbonAgent:
    def __init__(self):
        # Use Bytez API (OpenAI compatible)
        self.client = openai.OpenAI(
            api_key=os.getenv("BYTEZ_API_KEY"),
            base_url="https://api.bytez.com/models/v2/openai/v1/"
        )

    def run(self, materials: list) -> dict:
        prompt = f"""
        You are an environmental impact expert.

        Given these construction materials:
        {', '.join(materials)}

        Analyze their carbon footprint and environmental impact.
        Rate each material from 1-10 (10 = most sustainable).

        Return ONLY valid JSON with format:
        {{
            "material_name": {{"carbon_footprint": "value", "rating": 1-10, "notes": "brief note"}}
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
            return {"error": f"Error in CarbonAgent: {e}"}
           

if __name__ == "__main__":
    agent = CarbonAgent()
    result = agent.run(["concrete", "steel", "wood"])
    print(result)
