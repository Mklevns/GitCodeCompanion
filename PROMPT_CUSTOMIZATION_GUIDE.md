# Multi-LLM Pipeline: Customizable Prompt System

## Overview

The Multi-LLM Pipeline now features a powerful customizable prompt system that allows you to tailor AI analysis for different project types and requirements. Each of the four AI stages (Gemini, ChatGPT, Claude, DeepSeek) can be optimized with project-specific prompts.

## Key Features

- **Project-Specific Optimization**: Predefined prompts for AI/ML, Web Development, Security, and more
- **Custom Project Types**: Create your own project types with specialized prompts
- **Per-Stage Customization**: Customize prompts for each of the four pipeline stages
- **Persistent Configuration**: Settings are saved and persist across pipeline runs
- **Easy Management**: Command-line interface for prompt management
- **Import/Export**: Share prompt configurations across teams

## Predefined Project Types

### General Software Development
- Balanced analysis for general software projects
- Covers bugs, performance, security, quality, and best practices

### AI/ML Development
- **Focus Areas**: Model architecture, training stability, data processing, numerical stability
- **Specialized for**: TensorFlow, PyTorch, scikit-learn, data science workflows
- **Detects**: Gradient issues, tensor shape problems, overfitting, data leaks

### Web Development
- **Focus Areas**: XSS/CSRF vulnerabilities, API security, performance, accessibility, SEO
- **Specialized for**: React, Vue, Angular, Node.js, Express, Django, Flask
- **Detects**: Security vulnerabilities, performance bottlenecks, accessibility issues

### Security-Focused
- **Focus Areas**: Injection attacks, authentication flaws, cryptographic issues
- **Specialized for**: Security audits, penetration testing, secure coding
- **Detects**: OWASP Top 10 vulnerabilities, cryptographic weaknesses

## Quick Start

### 1. List Available Project Types
```bash
python prompt_cli.py --list
```

### 2. Set Project Type for Your Codebase
```bash
# For AI/ML projects
python prompt_cli.py --set ai_ml

# For web development
python prompt_cli.py --set web_development

# For security-focused analysis
python prompt_cli.py --set security
```

### 3. View Current Prompts
```bash
# Show prompts for active project type
python prompt_cli.py --show

# Show prompts for specific project type
python prompt_cli.py --show --project ai_ml
```

### 4. View Project Details
```bash
python prompt_cli.py --details ai_ml
```

## Creating Custom Project Types

### Interactive Creation
```bash
python prompt_cli.py --create-custom
```

### Programmatic Creation
```python
from prompt_config import PromptConfigManager, ProjectType

config_manager = PromptConfigManager()
config_manager.create_custom_project_type(
    "Blockchain DApp",
    "Smart contract and DeFi development",
    ProjectType.SECURITY
)
```

## Customizing Individual Prompts

### Interactive Customization
```bash
python prompt_cli.py --customize
```

### Programmatic Customization
```python
from prompt_config import PromptConfigManager

config_manager = PromptConfigManager()

# Customize Stage 1 (Gemini Analysis) for blockchain
blockchain_prompt = """You are an expert blockchain security analyst. Focus on:
1. Smart Contract Vulnerabilities (reentrancy, overflow, access control)
2. Gas Optimization (storage operations, loop efficiency)
3. DeFi-Specific Issues (flash loans, MEV, price manipulation)
4. Economic Security (tokenomics, governance attacks)
"""

config_manager.customize_prompt("stage_1", blockchain_prompt)
```

## Pipeline Integration

The pipeline automatically uses prompts for the active project type:

```python
# Pipeline automatically loads active project type prompts
from pipeline_stages import PipelineStages

# Initialize with custom config file (optional)
pipeline = PipelineStages("my_custom_prompts.json")

# Run analysis with project-specific prompts
results = pipeline.stage_1_gemini_analysis(files)
```

## Configuration Management

### Export Configuration
```bash
python prompt_cli.py --export team_prompts.json
```

### Import Configuration
```bash
python prompt_cli.py --import team_prompts.json
```

### Share Team Configurations
```python
# Export for team sharing
config_manager.export_prompts("team_ai_ml_config.json")

# Import team configuration
config_manager.import_prompts("team_ai_ml_config.json")
```

## Example: Setting Up for JanusAI_V2

For your JanusAI_V2 repository (AI/ML project):

```bash
# Set AI/ML project type
python prompt_cli.py --set ai_ml

# View AI/ML specific focus areas
python prompt_cli.py --details ai_ml

# Optionally customize for reinforcement learning
python prompt_cli.py --customize
# Then select ai_ml project and stage_1, add RL-specific prompts
```

The AI/ML project type will optimize analysis for:
- Model architecture issues
- Training stability problems
- Data processing bugs
- Numerical stability issues
- Performance bottlenecks
- Memory management

## Advanced Customization

### Creating Domain-Specific Prompts

For specialized domains like reinforcement learning:

```python
rl_prompt = """You are an expert in reinforcement learning systems. Focus on:

1. **Policy Networks**: Architecture issues, gradient flow, exploration/exploitation
2. **Value Functions**: Convergence issues, overestimation bias, target networks
3. **Training Stability**: Hyperparameter sensitivity, reward shaping, curriculum learning
4. **Environment Integration**: State/action space design, reward engineering
5. **Scalability**: Parallel training, distributed systems, memory efficiency

Analyze for RL-specific patterns and provide actionable recommendations."""

config_manager.customize_prompt("stage_1", rl_prompt)
```

### Multi-Environment Configurations

```python
# Development environment
config_manager.set_project_type(ProjectType.GENERAL)

# Production security review
config_manager.set_project_type(ProjectType.SECURITY)

# ML model deployment
config_manager.set_project_type(ProjectType.AI_ML)
```

## Best Practices

1. **Match Project Type to Codebase**: Use AI/ML type for machine learning projects, Web type for web applications
2. **Customize Gradually**: Start with predefined types, then customize as needed
3. **Team Consistency**: Export and share configurations across team members
4. **Version Control**: Include prompt config files in your repository
5. **Regular Updates**: Refine prompts based on pipeline feedback and results

## Integration with GitHub Actions

The pipeline automatically uses the active project type when triggered by GitHub Actions. Set your project type once, and all subsequent PR analyses will use the optimized prompts.

```yaml
# In your GitHub workflow
- name: Set AI/ML Project Type
  run: python prompt_cli.py --set ai_ml

- name: Run Multi-LLM Pipeline
  uses: ./
  # Pipeline uses AI/ML optimized prompts automatically
```

This customizable prompt system ensures that your Multi-LLM Pipeline provides the most relevant and actionable code analysis for your specific project type and requirements.