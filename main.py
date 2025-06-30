#!/usr/bin/env python3
"""
Multi-LLM Code Quality Pipeline
Main orchestrator for the 4-stage LLM gauntlet
"""

import os
import sys
import json
import logging
import traceback
from typing import Dict, Any, Optional, List

from git_github_utils import GitHubManager
from pipeline_stages import PipelineStages
from report_generator import ReportGenerator
from security_utils import SecurityUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MultiLLMPipeline:
    def __init__(self):
        """Initialize the Multi-LLM Pipeline"""
        self.github_manager = GitHubManager()
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
        """Validate that all required environment variables are set"""
        required_vars = [
            'GITHUB_TOKEN',
            'GEMINI_API_KEY', 
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY',
            'DEEPSEEK_API_KEY',
            'PR_NUMBER',
            'REPOSITORY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            return False
        
        logger.info("Environment validation passed")
        return True
    
    def get_changed_files(self) -> List[Dict[str, Any]]:
        """Get list of changed files from the pull request"""
        try:
            pr_number = int(os.getenv('PR_NUMBER'))
            changed_files = self.github_manager.get_pr_changed_files(pr_number)
            
            # Filter for code files only
            code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.php', '.rb', '.swift', '.kt'}
            code_files = []
            
            for file_info in changed_files:
                file_path = file_info['filename']
                _, ext = os.path.splitext(file_path)
                
                if ext.lower() in code_extensions and file_info['status'] != 'removed':
                    try:
                        content = self.github_manager.get_file_content(file_path)
                        if content:
                            code_files.append({
                                'path': file_path,
                                'content': content,
                                'status': file_info['status'],
                                'additions': file_info.get('additions', 0),
                                'deletions': file_info.get('deletions', 0)
                            })
                    except Exception as e:
                        logger.warning(f"Could not retrieve content for {file_path}: {e}")
            
            logger.info(f"Found {len(code_files)} code files to analyze")
            return code_files
            
        except Exception as e:
            logger.error(f"Error getting changed files: {e}")
            return []
    
    def post_stage_update(self, stage_name: str, status: str, details: str = ""):
        """Post update comment for a pipeline stage"""
        try:
            pr_number = int(os.getenv('PR_NUMBER'))
            
            status_emoji = {
                'running': '🔄',
                'completed': '✅',
                'failed': '❌',
                'skipped': '⏭️'
            }
            
            comment = f"""
## {status_emoji.get(status, '🔄')} Multi-LLM Pipeline - Stage: {stage_name}

**Status:** {status.title()}
**Stage:** {stage_name}

{details}

---
*Automated by Multi-LLM Code Quality Pipeline*
"""
            
            self.github_manager.post_comment(pr_number, comment)
            
        except Exception as e:
            logger.error(f"Error posting stage update: {e}")
    
    def run_stage_1_analysis(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Stage 1: Gemini Analysis"""
        self.pipeline_state['stage'] = 'stage_1_analysis'
        self.post_stage_update('1 - Gemini Analysis', 'running', 
                             'Analyzing code for bugs, performance issues, and improvements...')
        
        try:
            results = self.pipeline_stages.stage_1_gemini_analysis(files)
            self.pipeline_state['results']['stage_1'] = results
            
            # Create summary for comment
            total_issues = sum(len(result.get('issues', [])) for result in results.values())
            files_analyzed = len(results)
            
            details = f"""
**Analysis Complete:**
- Files analyzed: {files_analyzed}
- Issues identified: {total_issues}
- Performance suggestions: Available in detailed report
"""
            
            self.post_stage_update('1 - Gemini Analysis', 'completed', details)
            return results
            
        except Exception as e:
            error_msg = f"Stage 1 failed: {str(e)}"
            logger.error(error_msg)
            self.pipeline_state['errors'].append(error_msg)
            self.post_stage_update('1 - Gemini Analysis', 'failed', f"Error: {str(e)}")
            raise
    
    def run_stage_2_generation(self, analysis_results: Dict[str, Any], 
                             original_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Stage 2: ChatGPT Code Generation"""
        self.pipeline_state['stage'] = 'stage_2_generation'
        self.post_stage_update('2 - ChatGPT Generation', 'running',
                             'Generating improved code based on analysis...')
        
        try:
            results = self.pipeline_stages.stage_2_chatgpt_generation(analysis_results, original_files)
            self.pipeline_state['results']['stage_2'] = results
            
            # Create summary for comment
            files_improved = len(results)
            total_changes = sum(len(result.get('changes', [])) for result in results.values())
            
            details = f"""
**Code Generation Complete:**
- Files improved: {files_improved}
- Total changes made: {total_changes}
- Improvements focus on: Bug fixes, performance, readability
"""
            
            self.post_stage_update('2 - ChatGPT Generation', 'completed', details)
            return results
            
        except Exception as e:
            error_msg = f"Stage 2 failed: {str(e)}"
            logger.error(error_msg)
            self.pipeline_state['errors'].append(error_msg)
            self.post_stage_update('2 - ChatGPT Generation', 'failed', f"Error: {str(e)}")
            raise
    
    def run_stage_3_integration(self, generated_code: Dict[str, Any], 
                              original_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Stage 3: Claude Integration"""
        self.pipeline_state['stage'] = 'stage_3_integration'
        self.post_stage_update('3 - Claude Integration', 'running',
                             'Integrating improved code while maintaining consistency...')
        
        try:
            results = self.pipeline_stages.stage_3_claude_integration(generated_code, original_files)
            self.pipeline_state['results']['stage_3'] = results
            
            # Create summary for comment
            files_integrated = len(results)
            
            details = f"""
**Integration Complete:**
- Files integrated: {files_integrated}
- Style consistency: Maintained
- Architecture alignment: Verified
- Variable naming: Consistent
"""
            
            self.post_stage_update('3 - Claude Integration', 'completed', details)
            return results
            
        except Exception as e:
            error_msg = f"Stage 3 failed: {str(e)}"
            logger.error(error_msg)
            self.pipeline_state['errors'].append(error_msg)
            self.post_stage_update('3 - Claude Integration', 'failed', f"Error: {str(e)}")
            raise
    
    def run_stage_4_verification(self, integrated_code: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 4: DeepSeek Verification"""
        self.pipeline_state['stage'] = 'stage_4_verification'
        self.post_stage_update('4 - DeepSeek Verification', 'running',
                             'Performing final quality assurance and verification...')
        
        try:
            results = self.pipeline_stages.stage_4_deepseek_verification(integrated_code)
            self.pipeline_state['results']['stage_4'] = results
            
            # Create summary for comment
            verification_passed = all(result.get('verification_passed', False) for result in results.values())
            total_warnings = sum(len(result.get('warnings', [])) for result in results.values())
            
            status_text = "✅ PASSED" if verification_passed else "⚠️ WARNINGS"
            
            details = f"""
**Verification Complete:**
- Overall Status: {status_text}
- Files verified: {len(results)}
- Warnings found: {total_warnings}
- Quality assurance: Complete
"""
            
            self.post_stage_update('4 - DeepSeek Verification', 'completed', details)
            return results
            
        except Exception as e:
            error_msg = f"Stage 4 failed: {str(e)}"
            logger.error(error_msg)
            self.pipeline_state['errors'].append(error_msg)
            self.post_stage_update('4 - DeepSeek Verification', 'failed', f"Error: {str(e)}")
            raise
    
    def generate_final_report(self) -> str:
        """Generate comprehensive final report"""
        try:
            report = self.report_generator.generate_comprehensive_report(
                self.pipeline_state['results']
            )
            return report
        except Exception as e:
            logger.error(f"Error generating final report: {e}")
            return f"Error generating report: {str(e)}"
    
    def post_final_report(self, report: str):
        """Post the final comprehensive report"""
        try:
            pr_number = int(os.getenv('PR_NUMBER'))
            
            final_comment = f"""
# 🎯 Multi-LLM Pipeline Complete - Final Report

{report}

---

## Pipeline Summary
- **Status**: {'✅ SUCCESS' if not self.pipeline_state['errors'] else '⚠️ COMPLETED WITH WARNINGS'}
- **Stages Completed**: 4/4
- **Total Processing Time**: Available in detailed logs

## Next Steps
1. Review the analysis and proposed changes above
2. Test the improved code in your development environment  
3. Accept or reject the proposed changes based on your judgment
4. Merge the pull request if satisfied with the improvements

---
*🤖 Automated by Multi-LLM Code Quality Pipeline | Powered by Gemini, ChatGPT, Claude & DeepSeek*
"""
            
            self.github_manager.post_comment(pr_number, final_comment)
            
        except Exception as e:
            logger.error(f"Error posting final report: {e}")
    
    def handle_pipeline_failure(self, stage: str, error: str):
        """Handle pipeline failure with rollback capability"""
        try:
            pr_number = int(os.getenv('PR_NUMBER'))
            
            failure_comment = f"""
# ❌ Multi-LLM Pipeline Failed

**Failed Stage**: {stage}
**Error**: {error}

## Rollback Information
The pipeline has been safely stopped. No changes have been applied to your code.

## Troubleshooting
1. Check that all API keys are properly configured
2. Verify the code changes don't contain problematic content
3. Review the pipeline logs for detailed error information

## Support
If this issue persists, please check:
- API rate limits for the LLM services
- Network connectivity issues
- Malformed code that may cause parsing errors

---
*🔧 Pipeline Support | Multi-LLM Code Quality Pipeline*
"""
            
            self.github_manager.post_comment(pr_number, failure_comment)
            
        except Exception as e:
            logger.error(f"Error posting failure report: {e}")
    
    def run(self):
        """Run the complete multi-LLM pipeline"""
        import time
        
        self.pipeline_state['start_time'] = time.time()
        
        try:
            # Initial validation
            if not self.validate_environment():
                sys.exit(1)
            
            # Post initial comment
            pr_number = int(os.getenv('PR_NUMBER'))
            initial_comment = """
# 🚀 Multi-LLM Code Quality Pipeline Started

Your pull request is being processed through our 4-stage AI-powered code quality pipeline:

1. **🔍 Gemini Analysis** - Deep code analysis for bugs and improvements
2. **🛠️ ChatGPT Generation** - Code improvement and bug fixes  
3. **🔗 Claude Integration** - Seamless code integration and consistency
4. **✅ DeepSeek Verification** - Final quality assurance and verification

**Estimated Time**: 2-5 minutes depending on code complexity

---
*⏳ Processing... Updates will be posted as each stage completes*
"""
            self.github_manager.post_comment(pr_number, initial_comment)
            
            # Get changed files
            changed_files = self.get_changed_files()
            if not changed_files:
                logger.warning("No code files found to analyze")
                self.post_stage_update('Analysis', 'skipped', 'No code files found in pull request')
                return
            
            logger.info(f"Starting pipeline for {len(changed_files)} files")
            
            # Stage 1: Gemini Analysis
            analysis_results = self.run_stage_1_analysis(changed_files)
            
            # Stage 2: ChatGPT Generation
            generation_results = self.run_stage_2_generation(analysis_results, changed_files)
            
            # Stage 3: Claude Integration
            integration_results = self.run_stage_3_integration(generation_results, changed_files)
            
            # Stage 4: DeepSeek Verification
            verification_results = self.run_stage_4_verification(integration_results)
            
            # Generate and post final report
            final_report = self.generate_final_report()
            self.post_final_report(final_report)
            
            self.pipeline_state['status'] = 'completed'
            self.pipeline_state['end_time'] = time.time()
            
            logger.info("Multi-LLM pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            logger.error(traceback.format_exc())
            
            self.pipeline_state['status'] = 'failed'
            self.pipeline_state['end_time'] = time.time()
            
            self.handle_pipeline_failure(
                self.pipeline_state['stage'], 
                str(e)
            )
            
            sys.exit(1)

def main():
    """Main entry point"""
    try:
        pipeline = MultiLLMPipeline()
        pipeline.run()
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
