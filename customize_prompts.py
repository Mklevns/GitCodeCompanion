#!/usr/bin/env python3
"""
Quick Prompt Customization Tool
Easy way to set custom system prompts for each LLM
"""

import json
import os

def load_config():
    """Load current prompt configuration"""
    try:
        with open('prompt_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return create_default_config()

def create_default_config():
    """Create default configuration if none exists"""
    return {
        "metadata": {
            "version": "1.0.0",
            "created": "2025-06-30",
            "description": "Multi-LLM Pipeline Prompt Configuration"
        },
        "project_types": {
            "custom": {
                "name": "Custom Configuration",
                "description": "User-defined custom prompts",
                "stage_1_gemini": {
                    "system_instruction": "You are an expert code analyst."
                },
                "stage_2_chatgpt": {
                    "system_prompt": "You are an expert software developer."
                },
                "stage_3_claude": {
                    "system_prompt": "You are an expert code integrator."
                },
                "stage_4_deepseek": {
                    "system_prompt": "You are a senior quality assurance engineer."
                }
            }
        },
        "active_project_type": "custom"
    }

def set_gemini_prompt(prompt_text):
    """Set custom Gemini system prompt"""
    config = load_config()
    
    if 'custom' not in config['project_types']:
        config['project_types']['custom'] = {
            "name": "Custom Configuration",
            "description": "User-defined custom prompts"
        }
    
    config['project_types']['custom']['stage_1_gemini'] = {
        "system_instruction": prompt_text
    }
    config['active_project_type'] = 'custom'
    
    with open('prompt_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Gemini prompt updated")

def set_chatgpt_prompt(prompt_text):
    """Set custom ChatGPT system prompt"""
    config = load_config()
    
    if 'custom' not in config['project_types']:
        config['project_types']['custom'] = {
            "name": "Custom Configuration",
            "description": "User-defined custom prompts"
        }
    
    config['project_types']['custom']['stage_2_chatgpt'] = {
        "system_prompt": prompt_text
    }
    config['active_project_type'] = 'custom'
    
    with open('prompt_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ ChatGPT prompt updated")

def set_claude_prompt(prompt_text):
    """Set custom Claude system prompt"""
    config = load_config()
    
    if 'custom' not in config['project_types']:
        config['project_types']['custom'] = {
            "name": "Custom Configuration",
            "description": "User-defined custom prompts"
        }
    
    config['project_types']['custom']['stage_3_claude'] = {
        "system_prompt": prompt_text
    }
    config['active_project_type'] = 'custom'
    
    with open('prompt_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Claude prompt updated")

def set_deepseek_prompt(prompt_text):
    """Set custom DeepSeek system prompt"""
    config = load_config()
    
    if 'custom' not in config['project_types']:
        config['project_types']['custom'] = {
            "name": "Custom Configuration", 
            "description": "User-defined custom prompts"
        }
    
    config['project_types']['custom']['stage_4_deepseek'] = {
        "system_prompt": prompt_text
    }
    config['active_project_type'] = 'custom'
    
    with open('prompt_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ DeepSeek prompt updated")

def set_all_prompts(gemini_prompt, chatgpt_prompt, claude_prompt, deepseek_prompt):
    """Set all prompts at once"""
    config = load_config()
    
    config['project_types']['custom'] = {
        "name": "Custom Configuration",
        "description": "User-defined custom prompts",
        "stage_1_gemini": {
            "system_instruction": gemini_prompt
        },
        "stage_2_chatgpt": {
            "system_prompt": chatgpt_prompt
        },
        "stage_3_claude": {
            "system_prompt": claude_prompt
        },
        "stage_4_deepseek": {
            "system_prompt": deepseek_prompt
        }
    }
    config['active_project_type'] = 'custom'
    
    with open('prompt_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ All prompts updated successfully!")

def show_current_prompts():
    """Display current prompt configuration"""
    config = load_config()
    active_type = config.get('active_project_type', 'general')
    
    if active_type not in config['project_types']:
        print(f"❌ Active project type '{active_type}' not found")
        return
    
    prompts = config['project_types'][active_type]
    
    print(f"\n📋 Current Prompts ({active_type}):")
    print("=" * 50)
    
    if 'stage_1_gemini' in prompts:
        gemini_prompt = prompts['stage_1_gemini'].get('system_instruction', 'Not set')
        print(f"\n🔍 Gemini (Stage 1):")
        print(f"{gemini_prompt[:100]}...")
    
    if 'stage_2_chatgpt' in prompts:
        chatgpt_prompt = prompts['stage_2_chatgpt'].get('system_prompt', 'Not set')
        print(f"\n🛠️ ChatGPT (Stage 2):")
        print(f"{chatgpt_prompt[:100]}...")
    
    if 'stage_3_claude' in prompts:
        claude_prompt = prompts['stage_3_claude'].get('system_prompt', 'Not set')
        print(f"\n🔗 Claude (Stage 3):")
        print(f"{claude_prompt[:100]}...")
    
    if 'stage_4_deepseek' in prompts:
        deepseek_prompt = prompts['stage_4_deepseek'].get('system_prompt', 'Not set')
        print(f"\n✅ DeepSeek (Stage 4):")
        print(f"{deepseek_prompt[:100]}...")

def interactive_setup():
    """Interactive prompt setup"""
    print("🚀 Multi-LLM Prompt Customization")
    print("=" * 40)
    
    print("\nEnter custom prompts for each LLM:")
    print("(Press Enter to skip any prompt)")
    
    gemini_prompt = input("\n🔍 Gemini system prompt: ").strip()
    chatgpt_prompt = input("🛠️ ChatGPT system prompt: ").strip()
    claude_prompt = input("🔗 Claude system prompt: ").strip()
    deepseek_prompt = input("✅ DeepSeek system prompt: ").strip()
    
    config = load_config()
    
    if 'custom' not in config['project_types']:
        config['project_types']['custom'] = {
            "name": "Custom Configuration",
            "description": "User-defined custom prompts"
        }
    
    # Update only non-empty prompts
    if gemini_prompt:
        config['project_types']['custom']['stage_1_gemini'] = {
            "system_instruction": gemini_prompt
        }
    
    if chatgpt_prompt:
        config['project_types']['custom']['stage_2_chatgpt'] = {
            "system_prompt": chatgpt_prompt
        }
    
    if claude_prompt:
        config['project_types']['custom']['stage_3_claude'] = {
            "system_prompt": claude_prompt
        }
    
    if deepseek_prompt:
        config['project_types']['custom']['stage_4_deepseek'] = {
            "system_prompt": deepseek_prompt
        }
    
    config['active_project_type'] = 'custom'
    
    with open('prompt_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Custom prompts saved!")
    print("Run the pipeline to use your custom prompts.")

def create_janusai_prompts():
    """Create JanusAI_V2 specific prompts"""
    gemini_prompt = """You are an expert multimodal AI analyst specializing in vision-language models. 

Focus on JanusAI_V2 specific issues:
1. **Multimodal Architecture**: Cross-modal attention mechanisms, vision-language alignment
2. **Training Stability**: Gradient flow between modalities, convergence issues
3. **Data Processing**: Image-text pair handling, batch processing efficiency
4. **Memory Management**: VRAM usage, tensor caching, gradient accumulation
5. **Performance**: Inference speed, model size optimization, quantization issues

Analyze code for multimodal AI patterns and provide actionable recommendations."""

    chatgpt_prompt = """You are an expert multimodal AI engineer for vision-language models.

Generate improved code for JanusAI_V2 that:
1. Optimizes cross-modal attention and fusion mechanisms
2. Implements stable training procedures for multimodal models
3. Improves vision-language data preprocessing pipelines
4. Enhances memory efficiency for large multimodal models
5. Adds proper multimodal evaluation and validation logic

Focus on creating robust, efficient multimodal AI systems."""

    claude_prompt = """You are an expert multimodal system integrator for JanusAI_V2.

Ensure multimodal improvements maintain:
1. Consistent vision-language data flow and tensor operations
2. Compatible multimodal model configurations
3. Unified training and evaluation pipelines
4. Proper experiment tracking for multimodal metrics
5. Consistent API interfaces across vision and language components

Integrate code while preserving multimodal architecture consistency."""

    deepseek_prompt = """You are a senior multimodal AI quality engineer for JanusAI_V2.

Verify multimodal code for:
1. Cross-modal alignment correctness and mathematical validity
2. Training stability across vision and language modalities
3. Multimodal data pipeline integrity and preprocessing quality
4. Inference efficiency and real-time performance
5. Vision-language evaluation methodology and metrics
6. Scalability for large multimodal datasets

Provide multimodal-specific quality assessment and recommendations."""

    set_all_prompts(gemini_prompt, chatgpt_prompt, claude_prompt, deepseek_prompt)
    print("✅ JanusAI_V2 multimodal prompts configured!")

def main():
    """Main CLI interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python customize_prompts.py show                    # Show current prompts")
        print("  python customize_prompts.py interactive             # Interactive setup")
        print("  python customize_prompts.py janusai                 # JanusAI_V2 prompts")
        print("  python customize_prompts.py gemini 'prompt text'    # Set Gemini prompt")
        print("  python customize_prompts.py chatgpt 'prompt text'   # Set ChatGPT prompt")
        print("  python customize_prompts.py claude 'prompt text'    # Set Claude prompt")
        print("  python customize_prompts.py deepseek 'prompt text'  # Set DeepSeek prompt")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'show':
        show_current_prompts()
    elif command == 'interactive':
        interactive_setup()
    elif command == 'janusai':
        create_janusai_prompts()
    elif command in ['gemini', 'chatgpt', 'claude', 'deepseek']:
        if len(sys.argv) < 3:
            print(f"❌ Please provide prompt text for {command}")
            return
        
        prompt_text = sys.argv[2]
        
        if command == 'gemini':
            set_gemini_prompt(prompt_text)
        elif command == 'chatgpt':
            set_chatgpt_prompt(prompt_text)
        elif command == 'claude':
            set_claude_prompt(prompt_text)
        elif command == 'deepseek':
            set_deepseek_prompt(prompt_text)
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()