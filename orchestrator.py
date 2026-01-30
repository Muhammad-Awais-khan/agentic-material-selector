from agents.availability_agent import AvailabilityAgent
from agents.carbon_agent import CarbonAgent
from agents.cost_agent import CostAgent
from agents.durability_agent import DurabilityAgent
import json
import openai
import os

class MaterialSelectorOrchestrator:
    def __init__(self):
        self.availability_agent = AvailabilityAgent()
        self.carbon_agent = CarbonAgent()
        self.cost_agent = CostAgent()
        self.durability_agent = DurabilityAgent()
        self.client = openai.OpenAI(
            api_key=os.getenv("BYTEZ_API_KEY"),
            base_url="https://api.bytez.com/models/v2/openai/v1/"
        )

    def evaluate_materials(self, city: str, country: str):
        """
        Orchestrate all agents to provide comprehensive material evaluation
        """
        # Determine climate using LLM
        climate_prompt = f"What is the typical climate type for {city}, {country}? Respond with a single word like 'temperate', 'tropical', 'subtropical', 'arid', 'desert', 'continental', etc."
        try:
            climate_response = self.client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a geography expert. Provide concise climate classifications."},
                    {"role": "user", "content": climate_prompt}
                ]
            )
            climate = climate_response.choices[0].message.content.strip().lower()
        except Exception as e:
            climate = "temperate"  # Fallback
            print(f"Error determining climate: {e}, using default.")
        
        print(f"Evaluating materials for {city}, {country} (climate: {climate})...")
        
        # Step 1: Get availability
        availability = self.availability_agent.run(city, country)
        print(f"Availability analysis complete")
        
        # Step 2: Get all materials from availability
        all_materials = availability.get("easy_to_get", [])
        
        if not all_materials:
            all_materials = availability.get("limited", [])
            all_materials += availability.get("import_only", [])

        # Step 3: Analyze other factors
        carbon_analysis = self.carbon_agent.run(all_materials)
        print(f"Carbon impact analysis complete")
        
        cost_analysis = self.cost_agent.run(all_materials, city)
        print(f"Cost analysis complete")
        
        durability_analysis = self.durability_agent.run(all_materials, climate)
        print(f"Durability analysis complete")
        
        # Step 4: Compile comprehensive report
        report = {
            "location": {"city": city, "country": country},
            "availability": availability,
            "carbon_impact": carbon_analysis,
            "cost_analysis": cost_analysis,
            "durability": durability_analysis,
            "recommendation": self._generate_recommendation(
                all_materials, carbon_analysis, cost_analysis, durability_analysis
            )
        }
        
        return report

    def _generate_recommendation(self, all_materials, carbon, cost, durability):
        """Use LLM to select the best material based on all analyses"""
        
        prompt = f"""
        You are a construction material selection expert.

        Based on the following analyses for materials in {all_materials[0].get('location', 'the area')}:

        Available materials: {', '.join([m['name'] for m in all_materials])}

        Carbon Impact Analysis: {json.dumps(carbon, indent=2)}

        Cost Analysis: {json.dumps(cost, indent=2)}

        Durability Analysis: {json.dumps(durability, indent=2)}

        Select the single best material from the available ones, considering sustainability, cost-effectiveness, and durability. Provide a brief reasoning and the selected material.

        Respond in this format:
        Selected Material: [material name]
        Reasoning: [brief explanation]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that selects the best construction material based on provided analyses."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error in recommendation: {e}"

if __name__ == "__main__":
    orchestrator = MaterialSelectorOrchestrator()
    result = orchestrator.evaluate_materials("Lahore", "Pakistan")
    print("\n=== COMPREHENSIVE MATERIAL EVALUATION REPORT ===")
    print(json.dumps(result, indent=2))
