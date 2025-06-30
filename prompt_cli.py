#!/usr/bin/env python3
"""
Command Line Interface for Multi-LLM Pipeline Prompt Configuration
Allows users to easily customize system prompts for different project types
"""

import argparse
import sys
import json
from typing import Optional
from prompt_config import PromptConfigManager, ProjectType

def list_project_types(config_manager: PromptConfigManager):
    """List all available project types"""
    print("\nAvailable Project Types:")
    print("=" * 50)
    
    project_types = config_manager.list_project_types()
    active_type = config_manager.config["active_project_type"]
    
    for key, name in project_types.items():
        status = " (ACTIVE)" if key == active_type else ""
        print(f"  {key}: {name}{status}")
    
    print(f"\nCurrently Active: {active_type}")

def show_project_details(config_manager: PromptConfigManager, project_type: str):
    """Show detailed information about a project type"""
    try:
        info = config_manager.get_project_info(project_type)
        print(f"\nProject Type: {info['name']}")
        print(f"Description: {info['description']}")
        
        print(f"\nFocus Areas by Stage:")
        for stage_key, stage_info in info.items():
            if isinstance(stage_info, dict) and 'focus_areas' in stage_info:
                stage_name = stage_key.replace('_', ' ').title()
                print(f"\n{stage_name}:")
                for area in stage_info['focus_areas']:
                    print(f"  - {area}")
        
    except ValueError as e:
        print(f"Error: {e}")

def show_prompts(config_manager: PromptConfigManager, project_type: Optional[str] = None):
    """Show current prompts for a project type"""
    if project_type:
        if project_type not in config_manager.config["project_types"]:
            print(f"Error: Project type '{project_type}' not found")
            return
        
        original_active = config_manager.config["active_project_type"]
        config_manager.config["active_project_type"] = project_type
        prompts = config_manager.get_active_prompts()
        config_manager.config["active_project_type"] = original_active
    else:
        prompts = config_manager.get_active_prompts()
        project_type = config_manager.config["active_project_type"]
    
    print(f"\nSystem Prompts for: {project_type}")
    print("=" * 60)
    
    stage_names = {
        "stage_1_system_instruction": "Stage 1 - Gemini Analysis",
        "stage_2_system_prompt": "Stage 2 - ChatGPT Generation", 
        "stage_3_system_prompt": "Stage 3 - Claude Integration",
        "stage_4_system_prompt": "Stage 4 - DeepSeek Verification"
    }
    
    for key, prompt in prompts.items():
        stage_name = stage_names.get(key, key)
        print(f"\n{stage_name}:")
        print("-" * 40)
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)

def set_project_type(config_manager: PromptConfigManager, project_type: str):
    """Set the active project type"""
    try:
        # Check if it's a predefined type
        if hasattr(ProjectType, project_type.upper()):
            proj_type = ProjectType(project_type)
            config_manager.set_project_type(proj_type)
        elif project_type in config_manager.config["project_types"]:
            config_manager.config["active_project_type"] = project_type
            config_manager._save_config(config_manager.config)
        else:
            print(f"Error: Project type '{project_type}' not found")
            return
        
        print(f"Successfully set active project type to: {project_type}")
    except Exception as e:
        print(f"Error setting project type: {e}")

def customize_prompt_interactive(config_manager: PromptConfigManager):
    """Interactive prompt customization"""
    print("\nCustomize System Prompts")
    print("=" * 30)
    
    # Select project type
    project_types = config_manager.list_project_types()
    print("\nAvailable project types:")
    for i, (key, name) in enumerate(project_types.items(), 1):
        print(f"{i}. {key}: {name}")
    
    try:
        choice = int(input(f"\nSelect project type (1-{len(project_types)}): "))
        project_key = list(project_types.keys())[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection")
        return
    
    # Select stage
    stages = {
        "1": "stage_1",
        "2": "stage_2", 
        "3": "stage_3",
        "4": "stage_4"
    }
    
    print("\nSelect stage to customize:")
    print("1. Stage 1 - Gemini Analysis")
    print("2. Stage 2 - ChatGPT Generation")
    print("3. Stage 3 - Claude Integration")
    print("4. Stage 4 - DeepSeek Verification")
    
    stage_choice = input("Enter stage number (1-4): ")
    if stage_choice not in stages:
        print("Invalid stage selection")
        return
    
    stage = stages[stage_choice]
    
    # Show current prompt
    project_type_enum = None
    for pt in ProjectType:
        if pt.value == project_key:
            project_type_enum = pt
            break
    
    if not project_type_enum:
        print("Error: Invalid project type")
        return
    
    prompts = config_manager.get_active_prompts()
    current_prompt = ""
    
    # Get current prompt based on stage
    if stage == "stage_1":
        current_prompt = config_manager.config["project_types"][project_key]["stage_1_gemini"]["system_instruction"]
    elif stage == "stage_2":
        current_prompt = config_manager.config["project_types"][project_key]["stage_2_chatgpt"]["system_prompt"]
    elif stage == "stage_3":
        current_prompt = config_manager.config["project_types"][project_key]["stage_3_claude"]["system_prompt"]
    elif stage == "stage_4":
        current_prompt = config_manager.config["project_types"][project_key]["stage_4_deepseek"]["system_prompt"]
    
    print(f"\nCurrent prompt for {stage}:")
    print("-" * 40)
    print(current_prompt[:300] + "..." if len(current_prompt) > 300 else current_prompt)
    
    print(f"\nEnter new prompt (or press Enter to keep current):")
    print("(Type 'END' on a new line when finished)")
    
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    
    if lines:
        new_prompt = "\n".join(lines)
        config_manager.customize_prompt(stage, new_prompt, project_type_enum)
        print(f"Successfully updated {stage} prompt for {project_key}")

def create_custom_project(config_manager: PromptConfigManager):
    """Create a new custom project type"""
    print("\nCreate Custom Project Type")
    print("=" * 30)
    
    name = input("Enter project name: ").strip()
    if not name:
        print("Error: Project name cannot be empty")
        return
    
    description = input("Enter project description: ").strip()
    if not description:
        print("Error: Description cannot be empty")
        return
    
    # Select base type
    print("\nSelect base project type:")
    base_types = list(ProjectType)
    for i, pt in enumerate(base_types, 1):
        print(f"{i}. {pt.value}")
    
    try:
        choice = int(input(f"Select base type (1-{len(base_types)}): "))
        base_type = base_types[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection")
        return
    
    try:
        custom_key = config_manager.create_custom_project_type(name, description, base_type)
        print(f"Successfully created custom project type: {custom_key}")
    except Exception as e:
        print(f"Error creating custom project type: {e}")

def export_import_prompts(config_manager: PromptConfigManager, action: str, filename: str):
    """Export or import prompt configurations"""
    try:
        if action == "export":
            config_manager.export_prompts(filename)
            print(f"Successfully exported prompts to {filename}")
        elif action == "import":
            config_manager.import_prompts(filename)
            print(f"Successfully imported prompts from {filename}")
    except Exception as e:
        print(f"Error during {action}: {e}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Multi-LLM Pipeline Prompt Configuration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prompt_cli.py --list                    # List all project types
  python prompt_cli.py --set ai_ml               # Set active project type
  python prompt_cli.py --show                    # Show current prompts
  python prompt_cli.py --show --project ai_ml    # Show prompts for specific type
  python prompt_cli.py --details ai_ml           # Show project type details
  python prompt_cli.py --customize               # Interactive prompt customization
  python prompt_cli.py --create-custom           # Create custom project type
  python prompt_cli.py --export config.json     # Export configuration
  python prompt_cli.py --import config.json     # Import configuration
        """
    )
    
    parser.add_argument("--config", default="prompt_config.json",
                      help="Configuration file path")
    parser.add_argument("--list", action="store_true",
                      help="List all available project types")
    parser.add_argument("--set", metavar="TYPE",
                      help="Set active project type")
    parser.add_argument("--show", action="store_true",
                      help="Show current system prompts")
    parser.add_argument("--project", metavar="TYPE", 
                      help="Specify project type for --show")
    parser.add_argument("--details", metavar="TYPE",
                      help="Show detailed information about a project type")
    parser.add_argument("--customize", action="store_true",
                      help="Interactive prompt customization")
    parser.add_argument("--create-custom", action="store_true",
                      help="Create a new custom project type")
    parser.add_argument("--export", metavar="FILE",
                      help="Export prompt configuration to file")
    parser.add_argument("--import", metavar="FILE", dest="import_file",
                      help="Import prompt configuration from file")
    
    args = parser.parse_args()
    
    # Initialize configuration manager
    config_manager = PromptConfigManager(args.config)
    
    # Handle commands
    if args.list:
        list_project_types(config_manager)
    elif args.set:
        set_project_type(config_manager, args.set)
    elif args.show:
        show_prompts(config_manager, args.project)
    elif args.details:
        show_project_details(config_manager, args.details)
    elif args.customize:
        customize_prompt_interactive(config_manager)
    elif args.create_custom:
        create_custom_project(config_manager)
    elif args.export:
        export_import_prompts(config_manager, "export", args.export)
    elif args.import_file:
        export_import_prompts(config_manager, "import", args.import_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()