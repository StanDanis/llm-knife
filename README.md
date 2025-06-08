# LLM Knife

A Python library for working with various LLM models, including AWS Bedrock (Anthropic) and Azure OpenAI.

## Installation

This project uses Poetry for dependency management. To get started:

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-knife.git
cd llm-knife
```

3. Install dependencies:
```bash
poetry install
```

## Development Setup

1. Create a new virtual environment and install dependencies:
```bash
poetry shell
```

2. Install development dependencies:
```bash
poetry install --with dev
```

## Configuration

The library can be configured through:
- Environment variables
- Configuration files
- Runtime configuration

### Environment Variables

```bash
# AWS Configuration
LLM_KNIFE_AWS_REGION=us-west-2
LLM_KNIFE_ANTHROPIC_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
LLM_KNIFE_MAX_TOKENS=2048
LLM_KNIFE_TEMPERATURE=0.8
```

### Configuration Files

Create a configuration file at `~/.llm_knife/config.yaml`:
```yaml
aws:
  region: us-west-2
  bedrock:
    anthropic:
      model_id: anthropic.claude-3-sonnet-20240229-v1:0
      max_tokens: 2048
      temperature: 0.8
environment: production
```

## Usage

```python
from llm_knife.models.aws.anthropic_model import AnthropicModel

# Initialize the model
model = AnthropicModel()

# Generate text
response = model.generate(
    prompt="What is the capital of France?",
    context="You are a helpful geography assistant.",
    temperature=0.8,
    max_tokens=100
)
```

## Testing

Run tests with:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov
```

## Development Tools

The project includes several development tools:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:
```bash
poetry run black .
poetry run isort .
poetry run flake8
poetry run mypy .
```

## License

MIT License
