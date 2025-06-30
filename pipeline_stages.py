"""
Pipeline Stages Implementation
Handles the 4-stage LLM gauntlet process
"""

import json
import time
import os
import logging
from typing import Dict, Any, List
from llm_clients import LLMClients
from security_utils import SecurityUtils
from prompt_config import PromptConfigManager

logger = logging.getLogger(__name__)

class PipelineStages:
    def __init__(self, prompt_config_file: str = "prompt_config.json"):
        """Initialize pipeline stages"""
        self.llm_clients = LLMClients()
        self.security_utils = SecurityUtils()
        self.prompt_config = PromptConfigManager(prompt_config_file)
        
        # Get current prompts for active project type
        self.prompts = self.prompt_config.get_active_prompts()
    
    def stage_1_gemini_analysis(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Stage 1: Gemini Deep Code Analysis
        Analyzes code for bugs, performance issues, and improvements
        """
        logger.info("Starting Stage 1: Gemini Analysis")
        results = {}
        
        system_instruction = self.prompts["stage_1_system_instruction"]
        
        for file_info in files:
            file_path = file_info.get('path', 'unknown_file')
            try:
                file_content = file_info['content']
                
                # Sanitize input
                sanitized_content = self.security_utils.sanitize_code_input(file_content)
                
                prompt = f"""Analyze this code file for issues and improvements:

**File**: {file_path}
**Language**: {self._detect_language(file_path)}

**Code**:
```
{sanitized_content}
```

Please provide your analysis in the specified JSON format."""
                
                # Call Gemini API
                response = self.llm_clients.call_gemini(prompt, system_instruction)
                
                # Sanitize and validate response
                sanitized_response = self.security_utils.sanitize_api_response(response)
                
                if not self.security_utils.validate_llm_response(sanitized_response, "json"):
                    logger.warning(f"Invalid response from Gemini for {file_path}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': 'Invalid response format'
                    }
                    continue
                
                try:
                    # Parse JSON response
                    analysis = json.loads(sanitized_response)
                    results[file_path] = {
                        'status': 'completed',
                        'analysis': analysis,
                        'timestamp': time.time()
                    }
                    logger.info(f"Completed Gemini analysis for {file_path}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error for {file_path}: {e}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': f'JSON parsing error: {str(e)}'
                    }
                
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
                results[file_path] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        logger.info(f"Stage 1 completed: {len(results)} files processed")
        return results
    
    def stage_2_chatgpt_generation(self, analysis_results: Dict[str, Any], 
                                 original_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Stage 2: ChatGPT Code Generation
        Generates improved code based on Gemini's analysis
        """
        logger.info("Starting Stage 2: ChatGPT Generation")
        results = {}
        
        # Create file mapping for easy lookup
        file_map = {f['path']: f for f in original_files}
        
        system_prompt = self.prompts["stage_2_system_prompt"]
        
        for file_path, analysis_result in analysis_results.items():
            try:
                if analysis_result.get('status') != 'completed':
                    logger.warning(f"Skipping {file_path} - analysis not completed")
                    continue
                
                original_file = file_map.get(file_path)
                if not original_file:
                    logger.warning(f"Original file not found for {file_path}")
                    continue
                
                analysis = analysis_result['analysis']
                original_code = original_file['content']
                
                prompt = f"""Generate improved code based on this analysis:

**File**: {file_path}
**Language**: {self._detect_language(file_path)}

**Original Code**:
```
{original_code}
```

**Analysis Results**:
{json.dumps(analysis, indent=2)}

**Instructions**:
- Address all issues identified in the analysis
- Maintain the original functionality
- Keep the same file structure and main functions
- Add comments where improvements are made
- Ensure code follows best practices

Please generate the improved code in the specified JSON format."""
                
                # Call ChatGPT API
                response = self.llm_clients.call_chatgpt(prompt, system_prompt, "json")
                
                # Sanitize and validate response
                sanitized_response = self.security_utils.sanitize_api_response(response)
                
                if not self.security_utils.validate_llm_response(sanitized_response, "json"):
                    logger.warning(f"Invalid response from ChatGPT for {file_path}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': 'Invalid response format'
                    }
                    continue
                
                try:
                    # Parse JSON response
                    generation = json.loads(sanitized_response)
                    results[file_path] = {
                        'status': 'completed',
                        'generated_code': generation.get('improved_code', ''),
                        'changes': generation.get('changes', []),
                        'issues_addressed': generation.get('issues_addressed', []),
                        'summary': generation.get('summary', ''),
                        'timestamp': time.time()
                    }
                    logger.info(f"Completed ChatGPT generation for {file_path}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error for {file_path}: {e}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': f'JSON parsing error: {str(e)}'
                    }
                
            except Exception as e:
                logger.error(f"Error generating code for {file_path}: {e}")
                results[file_path] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        logger.info(f"Stage 2 completed: {len(results)} files processed")
        return results
    
    def stage_3_claude_integration(self, generated_code: Dict[str, Any], 
                                 original_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Stage 3: Claude Integration
        Integrates generated code while maintaining consistency
        """
        logger.info("Starting Stage 3: Claude Integration")
        results = {}
        
        # Create file mapping for easy lookup
        file_map = {f['path']: f for f in original_files}
        
        system_prompt = self.prompts["stage_3_system_prompt"]
        
        for file_path, generation_result in generated_code.items():
            try:
                if generation_result.get('status') != 'completed':
                    logger.warning(f"Skipping {file_path} - generation not completed")
                    continue
                
                original_file = file_map.get(file_path)
                if not original_file:
                    logger.warning(f"Original file not found for {file_path}")
                    continue
                
                generated_code_content = generation_result['generated_code']
                original_code = original_file['content']
                changes = generation_result.get('changes', [])
                
                prompt = f"""Integrate this improved code while maintaining consistency:

**File**: {file_path}
**Language**: {self._detect_language(file_path)}

**Original Code**:
```
{original_code}
```

**Generated Improved Code**:
```
{generated_code_content}
```

**Changes Made**:
{json.dumps(changes, indent=2)}

**Integration Requirements**:
- Maintain the original code style and formatting patterns
- Keep consistent variable naming conventions
- Preserve import structure and organization
- Ensure compatibility with other files in the project
- Maintain the same function signatures for public methods
- Keep existing comments that are still relevant

Please provide the final integrated code in the specified JSON format."""
                
                # Call Claude API
                response = self.llm_clients.call_claude(prompt, system_prompt)
                
                # Sanitize and validate response
                sanitized_response = self.security_utils.sanitize_api_response(response)
                
                if not self.security_utils.validate_llm_response(sanitized_response, "json"):
                    logger.warning(f"Invalid response from Claude for {file_path}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': 'Invalid response format'
                    }
                    continue
                
                try:
                    # Parse JSON response
                    integration = json.loads(sanitized_response)
                    results[file_path] = {
                        'status': 'completed',
                        'integrated_code': integration.get('integrated_code', ''),
                        'integration_notes': integration.get('integration_notes', []),
                        'style_adjustments': integration.get('style_adjustments', []),
                        'compatibility_checks': integration.get('compatibility_checks', ''),
                        'summary': integration.get('summary', ''),
                        'timestamp': time.time()
                    }
                    logger.info(f"Completed Claude integration for {file_path}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error for {file_path}: {e}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': f'JSON parsing error: {str(e)}'
                    }
                
            except Exception as e:
                logger.error(f"Error integrating code for {file_path}: {e}")
                results[file_path] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        logger.info(f"Stage 3 completed: {len(results)} files processed")
        return results
    
    def stage_4_deepseek_verification(self, integrated_code: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stage 4: DeepSeek Verification
        Final verification and quality assurance
        """
        logger.info("Starting Stage 4: DeepSeek Verification")
        results = {}
        
        system_prompt = self.prompts["stage_4_system_prompt"]
        
        for file_path, integration_result in integrated_code.items():
            try:
                if integration_result.get('status') != 'completed':
                    logger.warning(f"Skipping {file_path} - integration not completed")
                    continue
                
                integrated_code_content = integration_result['integrated_code']
                integration_notes = integration_result.get('integration_notes', [])
                
                prompt = f"""Perform final verification of this integrated code:

**File**: {file_path}
**Language**: {self._detect_language(file_path)}

**Integrated Code**:
```
{integrated_code_content}
```

**Integration Notes**:
{json.dumps(integration_notes, indent=2)}

**Verification Requirements**:
- Verify code correctness and logic
- Check for performance issues
- Review security implications
- Assess code quality and maintainability
- Identify potential regressions
- Confirm best practices compliance

Rate the overall quality from 1-10 and provide detailed verification results in the specified JSON format."""
                
                # Call DeepSeek API
                response = self.llm_clients.call_deepseek(prompt, system_prompt)
                
                # Sanitize and validate response
                sanitized_response = self.security_utils.sanitize_api_response(response)
                
                if not self.security_utils.validate_llm_response(sanitized_response, "json"):
                    logger.warning(f"Invalid response from DeepSeek for {file_path}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': 'Invalid response format'
                    }
                    continue
                
                try:
                    # Parse JSON response
                    verification = json.loads(sanitized_response)
                    results[file_path] = {
                        'status': 'completed',
                        'verification_passed': verification.get('verification_passed', False),
                        'overall_quality_score': verification.get('overall_quality_score', 0),
                        'correctness_check': verification.get('correctness_check', ''),
                        'performance_assessment': verification.get('performance_assessment', ''),
                        'security_review': verification.get('security_review', ''),
                        'warnings': verification.get('warnings', []),
                        'recommendations': verification.get('recommendations', []),
                        'final_assessment': verification.get('final_assessment', ''),
                        'regression_risks': verification.get('regression_risks', []),
                        'timestamp': time.time()
                    }
                    logger.info(f"Completed DeepSeek verification for {file_path}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error for {file_path}: {e}")
                    results[file_path] = {
                        'status': 'failed',
                        'error': f'JSON parsing error: {str(e)}'
                    }
                
            except Exception as e:
                logger.error(f"Error verifying code for {file_path}: {e}")
                results[file_path] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        logger.info(f"Stage 4 completed: {len(results)} files processed")
        return results
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        extension_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.sh': 'Shell',
            '.ps1': 'PowerShell',
            '.r': 'R',
            '.m': 'MATLAB',
            '.pl': 'Perl',
            '.lua': 'Lua',
            '.dart': 'Dart',
            '.elm': 'Elm'
        }
        
        _, ext = os.path.splitext(file_path.lower())
        return extension_map.get(ext, 'Unknown')
