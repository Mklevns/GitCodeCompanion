#!/usr/bin/env python3
"""
Demo: Customizable Prompt System for Multi-LLM Pipeline
Shows how to customize prompts for different project types
"""

import os
import sys
import logging
from prompt_config import PromptConfigManager, ProjectType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def demo_prompt_customization():
    """Demonstrate the prompt customization system"""
    print("=" * 80)
    print("Multi-LLM Pipeline: Customizable Prompt System Demo")
    print("=" * 80)
    
    # Initialize prompt configuration manager
    config_manager = PromptConfigManager("demo_prompt_config.json")
    
    print("\n1. Available Project Types:")
    print("-" * 40)
    project_types = config_manager.list_project_types()
    for key, name in project_types.items():
        active = " (ACTIVE)" if key == config_manager.config["active_project_type"] else ""
        print(f"   {key}: {name}{active}")
    
    print("\n2. Setting Project Type to AI/ML:")
    print("-" * 40)
    config_manager.set_project_type(ProjectType.AI_ML)
    print("Successfully set project type to AI/ML")
    
    print("\n3. AI/ML Project Focus Areas:")
    print("-" * 40)
    ai_ml_config = config_manager.get_project_info("ai_ml")
    for stage_key, stage_info in ai_ml_config.items():
        if isinstance(stage_info, dict) and 'focus_areas' in stage_info:
            stage_name = stage_key.replace('_', ' ').title()
            print(f"\n{stage_name}:")
            for area in stage_info['focus_areas']:
                print(f"   - {area}")
    
    print("\n4. Current AI/ML Prompts (Preview):")
    print("-" * 40)
    ai_ml_prompts = config_manager.get_active_prompts()
    
    stage_names = {
        "stage_1_system_instruction": "Stage 1 - Gemini Analysis",
        "stage_2_system_prompt": "Stage 2 - ChatGPT Generation", 
        "stage_3_system_prompt": "Stage 3 - Claude Integration",
        "stage_4_system_prompt": "Stage 4 - DeepSeek Verification"
    }
    
    for key, prompt in ai_ml_prompts.items():
        stage_name = stage_names.get(key, key)
        print(f"\n{stage_name}:")
        preview = prompt[:150] + "..." if len(prompt) > 150 else prompt
        print(f"   {preview}")
    
    print("\n5. Creating Custom Project Type:")
    print("-" * 40)
    custom_key = config_manager.create_custom_project_type(
        "Blockchain DApp", 
        "Smart contract and decentralized application development",
        ProjectType.SECURITY
    )
    print(f"Created custom project type: {custom_key}")
    
    print("\n6. Customizing Stage 1 Prompt for Blockchain:")
    print("-" * 40)
    blockchain_prompt = """You are an expert blockchain and smart contract security analyst. Focus on:

1. **Smart Contract Vulnerabilities**: Reentrancy, integer overflow/underflow, access control issues
2. **Gas Optimization**: Inefficient operations, unnecessary storage reads/writes
3. **DeFi-Specific Issues**: Flash loan attacks, price manipulation, liquidity issues
4. **Consensus Vulnerabilities**: MEV attacks, front-running, sandwich attacks
5. **Code Quality**: Proper use of modifiers, events, error handling

Provide blockchain-focused analysis with emphasis on economic security and gas efficiency."""
    
    config_manager.customize_prompt("stage_1", blockchain_prompt, None)
    config_manager.config["active_project_type"] = custom_key
    config_manager._save_config(config_manager.config)
    
    print("Successfully customized Stage 1 prompt for blockchain projects")
    
    print("\n7. Web Development Project Type:")
    print("-" * 40)
    config_manager.set_project_type(ProjectType.WEB_DEVELOPMENT)
    web_config = config_manager.get_project_info("web_development")
    
    print(f"Name: {web_config['name']}")
    print(f"Description: {web_config['description']}")
    print("\nFocus Areas:")
    for area in web_config['stage_1_gemini']['focus_areas']:
        print(f"   - {area}")
    
    print("\n8. Security-Focused Project Type:")
    print("-" * 40)
    config_manager.set_project_type(ProjectType.SECURITY)
    security_config = config_manager.get_project_info("security")
    
    print(f"Name: {security_config['name']}")
    print(f"Description: {security_config['description']}")
    print("\nSecurity Focus Areas:")
    for area in security_config['stage_1_gemini']['focus_areas']:
        print(f"   - {area}")
    
    print("\n9. Exporting Configuration:")
    print("-" * 40)
    config_manager.export_prompts("exported_prompts.json")
    print("Configuration exported to exported_prompts.json")
    
    print("\n" + "=" * 80)
    print("Prompt Customization Demo Complete!")
    print("=" * 80)
    print("\nKey Features Demonstrated:")
    print("✓ Multiple predefined project types (General, AI/ML, Web, Security, etc.)")
    print("✓ Project-specific focus areas and optimized prompts")
    print("✓ Custom project type creation")
    print("✓ Individual prompt customization per stage")
    print("✓ Configuration export/import capability")
    print("✓ Easy switching between project types")
    
    print("\nUsage in Pipeline:")
    print("- Pipeline automatically uses prompts for active project type")
    print("- Prompts optimize AI analysis for specific domains")
    print("- Custom prompts can be created for unique project needs")
    print("- Configuration persists across pipeline runs")

def demo_cli_usage():
    """Show CLI usage examples"""
    print("\n" + "=" * 80)
    print("Command Line Interface Usage Examples")
    print("=" * 80)
    
    cli_examples = [
        ("List all project types", "python prompt_cli.py --list"),
        ("Set AI/ML project type", "python prompt_cli.py --set ai_ml"),
        ("Show current prompts", "python prompt_cli.py --show"),
        ("Show AI/ML prompts", "python prompt_cli.py --show --project ai_ml"),
        ("Show project details", "python prompt_cli.py --details security"),
        ("Interactive customization", "python prompt_cli.py --customize"),
        ("Create custom type", "python prompt_cli.py --create-custom"),
        ("Export configuration", "python prompt_cli.py --export my_config.json"),
        ("Import configuration", "python prompt_cli.py --import my_config.json")
    ]
    
    for description, command in cli_examples:
        print(f"\n{description}:")
        print(f"   {command}")

if __name__ == "__main__":
    try:
        demo_prompt_customization()
        demo_cli_usage()
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)