# Custom System Prompts Guide

## Method 1: Edit Configuration File (Easiest)

Edit `prompt_config.json` to customize prompts for each LLM:

```json
{
  "project_types": {
    "your_custom_type": {
      "name": "Your Custom Project",
      "description": "Custom analysis for your specific needs",
      "stage_1_gemini": {
        "system_instruction": "Your custom Gemini prompt here..."
      },
      "stage_2_chatgpt": {
        "system_prompt": "Your custom ChatGPT prompt here..."
      },
      "stage_3_claude": {
        "system_prompt": "Your custom Claude prompt here..."
      },
      "stage_4_deepseek": {
        "system_prompt": "Your custom DeepSeek prompt here..."
      }
    }
  }
}
```

## Method 2: Use CLI Tool (Interactive)

```bash
# Create custom project type
python prompt_cli.py --create-custom

# Set specific prompts
python prompt_cli.py --set-prompt gemini "Your Gemini system prompt"
python prompt_cli.py --set-prompt chatgpt "Your ChatGPT system prompt"
python prompt_cli.py --set-prompt claude "Your Claude system prompt"
python prompt_cli.py --set-prompt deepseek "Your DeepSeek system prompt"
```

## Method 3: Environment Variables (Quick Override)

Set environment variables to override specific prompts:

```bash
export GEMINI_SYSTEM_PROMPT="Custom Gemini analysis prompt"
export CHATGPT_SYSTEM_PROMPT="Custom ChatGPT generation prompt"
export CLAUDE_SYSTEM_PROMPT="Custom Claude integration prompt"
export DEEPSEEK_SYSTEM_PROMPT="Custom DeepSeek verification prompt"
```

## Method 4: Programmatic Customization

Create a custom configuration script:

```python
import json

def create_custom_prompts():
    config = {
        "stage_1_gemini": {
            "system_instruction": """
            You are a specialized code analyst for [YOUR DOMAIN].
            Focus on:
            1. Domain-specific issues
            2. Performance patterns
            3. Security concerns
            
            Provide detailed analysis in JSON format.
            """
        },
        "stage_2_chatgpt": {
            "system_prompt": """
            You are an expert developer for [YOUR DOMAIN].
            Generate improved code that:
            1. Fixes identified issues
            2. Optimizes for [YOUR REQUIREMENTS]
            3. Follows [YOUR STANDARDS]
            """
        },
        "stage_3_claude": {
            "system_prompt": """
            You are a code integration specialist.
            Ensure the improved code:
            1. Maintains [YOUR STYLE]
            2. Preserves [YOUR ARCHITECTURE]
            3. Follows [YOUR CONVENTIONS]
            """
        },
        "stage_4_deepseek": {
            "system_prompt": """
            You are a quality assurance expert.
            Verify the code meets:
            1. [YOUR QUALITY STANDARDS]
            2. [YOUR PERFORMANCE REQUIREMENTS]
            3. [YOUR SECURITY REQUIREMENTS]
            """
        }
    }
    
    with open('custom_prompts.json', 'w') as f:
        json.dump(config, f, indent=2)

create_custom_prompts()
```

## Examples for Different Use Cases

### For JanusAI_V2 (Multimodal AI)

```json
{
  "stage_1_gemini": {
    "system_instruction": "You are an expert multimodal AI analyst. Focus on vision-language model architecture, training stability, and multimodal data processing. Analyze for tensor shape consistency, gradient flow issues, and cross-modal alignment problems."
  },
  "stage_2_chatgpt": {
    "system_prompt": "You are a multimodal AI engineer. Generate improved code for vision-language models, focusing on efficient cross-modal attention, stable training procedures, and optimized multimodal data processing pipelines."
  },
  "stage_3_claude": {
    "system_prompt": "You are a multimodal system integrator. Ensure vision-language model improvements maintain consistent tensor operations, proper model configuration, and compatible multimodal data flows."
  },
  "stage_4_deepseek": {
    "system_prompt": "You are a multimodal AI quality expert. Verify vision-language model correctness, training stability, cross-modal alignment quality, and computational efficiency for multimodal processing."
  }
}
```

### For Security-Focused Analysis

```json
{
  "stage_1_gemini": {
    "system_instruction": "You are a cybersecurity expert. Perform deep security analysis focusing on OWASP Top 10, injection vulnerabilities, authentication flaws, and data protection issues. Provide exploit scenarios and risk assessments."
  },
  "stage_2_chatgpt": {
    "system_prompt": "You are a security engineer. Generate hardened code that implements secure coding practices, proper input validation, secure authentication, and defense-in-depth strategies."
  }
}
```

### For Performance-Critical Applications

```json
{
  "stage_1_gemini": {
    "system_instruction": "You are a performance optimization expert. Analyze for algorithmic complexity, memory usage patterns, CPU/GPU utilization, and scalability bottlenecks. Focus on micro-optimizations and system-level performance."
  },
  "stage_2_chatgpt": {
    "system_prompt": "You are a performance engineer. Generate optimized code with efficient algorithms, minimal memory allocations, vectorized operations, and parallel processing where appropriate."
  }
}
```

## Advanced Customization Features

### Dynamic Prompt Templates

```python
def generate_dynamic_prompt(project_name, focus_areas, tech_stack):
    return f"""
    You are an expert analyst for {project_name}.
    Technology Stack: {', '.join(tech_stack)}
    
    Focus specifically on:
    {chr(10).join(f'- {area}' for area in focus_areas)}
    
    Provide analysis tailored to this specific project context.
    """
```

### Conditional Prompts

```python
def get_conditional_prompt(file_type, project_type):
    if file_type == '.py' and project_type == 'ai_ml':
        return "Focus on ML-specific Python patterns..."
    elif file_type == '.js' and project_type == 'web':
        return "Focus on web security and performance..."
    # ... more conditions
```

## Best Practices

1. **Be Specific**: Include exact requirements and standards
2. **Use Examples**: Provide concrete examples of desired output
3. **Set Context**: Include domain-specific terminology and concepts
4. **Define Quality**: Specify what constitutes good vs. bad in your domain
5. **Include Constraints**: Mention any limitations or requirements

## Testing Your Custom Prompts

```bash
# Test with demo mode
python demo_mode.py

# Test specific configuration
python prompt_cli.py --show
python prompt_cli.py --test your_custom_type
```