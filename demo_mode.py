#!/usr/bin/env python3
"""
Demo Mode for Multi-LLM Pipeline
Demonstrates the pipeline functionality with sample code files
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

from pipeline_stages import PipelineStages
from report_generator import ReportGenerator
from security_utils import SecurityUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DemoPipeline:
    def __init__(self):
        """Initialize the Demo Pipeline"""
        self.pipeline_stages = PipelineStages()
        self.report_generator = ReportGenerator()
        self.security_utils = SecurityUtils()
        
        # Pipeline state
        self.pipeline_state = {
            'stage': 'initialization',
            'status': 'running',
            'results': {},
            'errors': [],
            'start_time': None,
            'end_time': None
        }
    
    def validate_environment(self) -> bool:
        """Validate that all required API keys are available"""
        required_vars = [
            'GEMINI_API_KEY', 
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY',
            'DEEPSEEK_API_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing required API keys: {missing_vars}")
            return False
        
        logger.info("Environment validation passed")
        return True
    
    def create_sample_files(self) -> List[Dict[str, Any]]:
        """Create sample code files for demonstration"""
        sample_files = [
            {
                'path': 'calculator.py',
                'content': '''def divide(a, b):
    return a / b

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, x, y):
        result = x + y
        self.history.append(f"{x} + {y} = {result}")
        return result
    
    def get_history(self):
        return self.history''',
                'status': 'modified',
                'additions': 20,
                'deletions': 0
            },
            {
                'path': 'user_auth.py',
                'content': '''import hashlib

def authenticate_user(username, password):
    # Simple authentication - not secure!
    if username == "admin" and password == "password":
        return True
    return False

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def validate_input(user_input):
    # No input validation
    return user_input

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_admin = False
    
    def login(self):
        if authenticate_user(self.username, self.password):
            self.is_admin = True
            return "Login successful"
        return "Login failed"''',
                'status': 'added',
                'additions': 25,
                'deletions': 0
            }
        ]
        
        logger.info(f"Created {len(sample_files)} sample files for demonstration")
        return sample_files
    
    def print_stage_update(self, stage_name: str, status: str, details: str = ""):
        """Print stage update information"""
        status_emoji = {
            'running': '🔄',
            'completed': '✅',
            'failed': '❌',
            'skipped': '⏭️'
        }
        
        print(f"\n{status_emoji.get(status, '🔄')} Multi-LLM Pipeline - Stage: {stage_name}")
        print(f"Status: {status.title()}")
        if details:
            print(f"Details: {details}")
        print("-" * 60)
    
    def run_demo(self):
        """Run the complete multi-LLM pipeline demonstration"""
        import time
        
        self.pipeline_state['start_time'] = time.time()
        
        try:
            print("="*80)
            print("🚀 Multi-LLM Code Quality Pipeline - DEMO MODE")
            print("="*80)
            print("Demonstrating 4-stage AI-powered code analysis:")
            print("1. 🔍 Gemini Analysis - Deep code analysis")
            print("2. 🛠️ ChatGPT Generation - Code improvements")  
            print("3. 🔗 Claude Integration - Seamless integration")
            print("4. ✅ DeepSeek Verification - Quality assurance")
            print("-" * 80)
            
            # Validate environment
            if not self.validate_environment():
                print("❌ Environment validation failed. Please check API keys.")
                return
            
            # Create sample files
            sample_files = self.create_sample_files()
            print(f"📁 Analyzing {len(sample_files)} sample code files...")
            
            # Stage 1: Gemini Analysis
            self.print_stage_update('1 - Gemini Analysis', 'running', 
                                  'Analyzing code for bugs, performance issues, and improvements...')
            
            analysis_results = self.pipeline_stages.stage_1_gemini_analysis(sample_files)
            self.pipeline_state['results']['stage_1'] = analysis_results
            
            total_issues = sum(len(result.get('analysis', {}).get('issues', [])) 
                             for result in analysis_results.values() 
                             if result.get('status') == 'completed')
            
            self.print_stage_update('1 - Gemini Analysis', 'completed', 
                                  f'Found {total_issues} issues across {len(analysis_results)} files')
            
            # Stage 2: ChatGPT Generation
            self.print_stage_update('2 - ChatGPT Generation', 'running',
                                  'Generating improved code based on analysis...')
            
            generation_results = self.pipeline_stages.stage_2_chatgpt_generation(
                analysis_results, sample_files)
            self.pipeline_state['results']['stage_2'] = generation_results
            
            files_improved = sum(1 for result in generation_results.values() 
                               if result.get('status') == 'completed')
            
            self.print_stage_update('2 - ChatGPT Generation', 'completed',
                                  f'Generated improvements for {files_improved} files')
            
            # Stage 3: Claude Integration
            self.print_stage_update('3 - Claude Integration', 'running',
                                  'Integrating improved code while maintaining consistency...')
            
            integration_results = self.pipeline_stages.stage_3_claude_integration(
                generation_results, sample_files)
            self.pipeline_state['results']['stage_3'] = integration_results
            
            files_integrated = sum(1 for result in integration_results.values() 
                                 if result.get('status') == 'completed')
            
            self.print_stage_update('3 - Claude Integration', 'completed',
                                  f'Successfully integrated {files_integrated} files')
            
            # Stage 4: DeepSeek Verification
            self.print_stage_update('4 - DeepSeek Verification', 'running',
                                  'Performing final quality assurance and verification...')
            
            verification_results = self.pipeline_stages.stage_4_deepseek_verification(
                integration_results)
            self.pipeline_state['results']['stage_4'] = verification_results
            
            verification_passed = sum(1 for result in verification_results.values()
                                    if result.get('verification_passed', False))
            
            self.print_stage_update('4 - DeepSeek Verification', 'completed',
                                  f'Verification passed for {verification_passed}/{len(verification_results)} files')
            
            # Generate final report
            print("\n📋 Generating comprehensive final report...")
            final_report = self.report_generator.generate_comprehensive_report(
                self.pipeline_state['results']
            )
            
            self.pipeline_state['status'] = 'completed'
            self.pipeline_state['end_time'] = time.time()
            
            # Display results
            print("\n" + "="*80)
            print("🎯 MULTI-LLM PIPELINE COMPLETE - FINAL REPORT")
            print("="*80)
            print(final_report)
            print("\n" + "="*80)
            print("✅ Demo completed successfully!")
            print(f"⏱️ Total processing time: {self.pipeline_state['end_time'] - self.pipeline_state['start_time']:.2f} seconds")
            print("="*80)
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            print(f"\n❌ Demo failed: {str(e)}")
            
            self.pipeline_state['status'] = 'failed'
            self.pipeline_state['end_time'] = time.time()
            
            return

def main():
    """Main entry point for demo"""
    try:
        demo = DemoPipeline()
        demo.run_demo()
    except Exception as e:
        logger.error(f"Critical error in demo: {e}")
        print(f"❌ Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()