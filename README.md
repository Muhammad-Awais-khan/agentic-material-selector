# Agentic Material Selector

An intelligent, AI-powered system for selecting optimal construction materials based on location, sustainability, cost, and durability factors. This project uses multiple specialized agents orchestrated by an LLM to provide comprehensive material recommendations.

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for availability, carbon footprint, cost analysis, and durability assessment
- **LLM-Powered Decisions**: Uses advanced language models for climate determination and final material selection
- **Location-Aware**: Considers local availability, transportation costs, and regional climate conditions
- **Sustainability Focus**: Prioritizes eco-friendly materials with low carbon impact
- **Comprehensive Analysis**: Combines multiple factors for balanced recommendations

## 🏗️ Architecture

The system consists of:

- **Availability Agent**: Determines locally available construction materials
- **Carbon Agent**: Analyzes environmental impact and sustainability ratings
- **Cost Agent**: Evaluates relative costs and transportation factors
- **Durability Agent**: Assesses lifespan and maintenance requirements
- **Orchestrator**: Coordinates all agents and makes final LLM-based selections

## 👥 Team & Roles

**Project Lead & Architect**  
- **[Hammad Ul Haq](https://github.com/Hammad81314)**

**Core Contributor / Co-Developer**  
- **Muhammad Awais** – Development, Testing, Documentation

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agentic-material-selector.git
cd agentic-material-selector
```

2. Create a virtual environment:
```bash
python -m venv venv311
source venv311/Scripts/activate  # On Windows
# or
# source venv311/bin/activate   # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export BYTEZ_API_KEY="your_bytez_api_key_here"
```

## 📖 Usage

### Basic Usage

```python
from orchestrator import MaterialSelectorOrchestrator

orchestrator = MaterialSelectorOrchestrator()
result = orchestrator.evaluate_materials("Lahore", "Pakistan")

print(result["recommendation"])
```

### Command Line

```bash
python main.py
```

This will run the evaluation for Lahore, Pakistan and display a comprehensive report.

## 🔧 Configuration

- **API Key**: Set `BYTEZ_API_KEY` environment variable with your Bytez API key
- **Models**: Uses `openai/gpt-4o-mini` for cost-effective AI responses
- **Climate**: Automatically determined based on location

## 📊 Sample Output

```
Evaluating materials for Lahore, Pakistan (climate: subtropical)...
Availability analysis complete
Carbon impact analysis complete
Cost analysis complete
Durability analysis complete

=== COMPREHENSIVE MATERIAL EVALUATION REPORT ===
{
  "location": {
    "city": "Lahore",
    "country": "Pakistan"
  },
  "availability": {
    "easy_to_get": ["brick", "concrete", "steel"],
    "limited": ["wood"],
    "import_only": ["glass", "aluminum"]
  },
  "carbon_impact": {...},
  "cost_analysis": {...},
  "durability": {...},
  "recommendation": "Selected Material: brick\nReasoning: Brick is locally abundant, has moderate carbon impact, and excellent durability in subtropical climates with low maintenance costs."
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Bytez API](https://bytez.com) for AI capabilities
- Inspired by sustainable construction practices
- Thanks to the open-source community

## 📞 Contact

For questions or suggestions, please open an issue on GitHub.

---

*Made with ❤️ for sustainable construction*
