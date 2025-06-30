"""
Customizable System Prompt Configuration for Multi-LLM Pipeline
Allows users to customize AI prompts based on project type and requirements
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class ProjectType(Enum):
    """Predefined project types with optimized prompts"""
    GENERAL = "general"
    WEB_DEVELOPMENT = "web_development"
    AI_ML = "ai_ml"
    BACKEND_API = "backend_api"
    MOBILE_APP = "mobile_app"
    DATA_SCIENCE = "data_science"
    GAME_DEVELOPMENT = "game_development"
    DEVOPS_INFRA = "devops_infra"
    SECURITY = "security"
    EMBEDDED = "embedded"

class PromptConfigManager:
    def __init__(self, config_file: str = "prompt_config.json"):
        """Initialize prompt configuration manager"""
        self.config_file = config_file
        self.config = self._load_or_create_config()
    
    def _load_or_create_config(self) -> Dict[str, Any]:
        """Load existing config or create default configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded prompt configuration from {self.config_file}")
                return config
            except Exception as e:
                logger.warning(f"Error loading config file: {e}. Using defaults.")
        
        # Create default configuration
        config = self._create_default_config()
        self._save_config(config)
        return config
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default prompt configurations for all project types"""
        return {
            "metadata": {
                "version": "1.0.0",
                "created": "2025-06-30",
                "description": "Multi-LLM Pipeline Prompt Configuration"
            },
            "project_types": {
                ProjectType.GENERAL.value: {
                    "name": "General Software Development",
                    "description": "Balanced analysis for general software projects",
                    "stage_1_gemini": {
                        "focus_areas": [
                            "Bugs and Logic Errors",
                            "Performance Issues", 
                            "Security Vulnerabilities",
                            "Code Quality",
                            "Best Practices"
                        ],
                        "system_instruction": """You are an expert code analyst. Perform a comprehensive analysis of the provided code and identify:

1. **Bugs and Logic Errors**: Find actual bugs, edge cases, and logical issues
2. **Performance Issues**: Identify inefficient algorithms, memory leaks, unnecessary computations
3. **Security Vulnerabilities**: Look for injection attacks, XSS, authentication issues, etc.
4. **Code Quality**: Poor naming, complex functions, lack of error handling
5. **Best Practices**: Violations of language-specific conventions and patterns

For each issue found, provide:
- **Type**: Bug, Performance, Security, Quality, or Best Practice
- **Severity**: Critical, High, Medium, Low
- **Location**: Line numbers or function names where applicable
- **Description**: Clear explanation of the issue
- **Impact**: How this affects the application
- **Recommendation**: Specific suggestion for improvement

Respond in JSON format with this structure:
{
  "issues": [
    {
      "type": "Bug|Performance|Security|Quality|Best Practice",
      "severity": "Critical|High|Medium|Low", 
      "location": "line X or function Y",
      "description": "detailed description",
      "impact": "impact explanation",
      "recommendation": "specific fix suggestion"
    }
  ],
  "overall_assessment": "summary of code quality",
  "improvement_priority": ["list of top 3 priorities"]
}"""
                    },
                    "stage_2_chatgpt": {
                        "focus_areas": [
                            "Bug Fixes",
                            "Performance Optimization",
                            "Security Improvements",
                            "Code Quality Enhancement",
                            "Best Practice Implementation"
                        ],
                        "system_prompt": """You are an expert software developer. Based on the provided code analysis, generate improved code that addresses the identified issues.

Your task:
1. Fix all bugs and logic errors
2. Implement performance optimizations
3. Address security vulnerabilities
4. Improve code quality and readability
5. Apply best practices for the language

Provide your response in JSON format:
{
  "improved_code": "complete improved code",
  "changes": [
    {
      "type": "Bug Fix|Performance|Security|Quality|Best Practice",
      "description": "what was changed",
      "line_range": "affected lines",
      "impact": "expected improvement"
    }
  ],
  "issues_addressed": [
    {
      "original_issue": "issue from analysis",
      "solution": "how it was fixed"
    }
  ],
  "summary": "overall improvements summary"
}"""
                    },
                    "stage_3_claude": {
                        "focus_areas": [
                            "Code Style Consistency",
                            "Architecture Alignment",
                            "Variable Naming",
                            "Import Management",
                            "Compatibility"
                        ],
                        "system_prompt": """You are an expert code integrator. Your task is to seamlessly integrate improved code while maintaining consistency with the existing codebase.

Focus on:
1. Maintaining consistent code style and formatting
2. Preserving existing architecture patterns
3. Keeping variable naming conventions consistent
4. Ensuring proper import management
5. Maintaining compatibility with the rest of the codebase

Provide your response in JSON format:
{
  "integrated_code": "final integrated code",
  "integration_notes": [
    "list of integration decisions made"
  ],
  "style_adjustments": [
    {
      "adjustment": "what was adjusted",
      "reason": "why it was needed"
    }
  ],
  "compatibility_checks": "confirmation of compatibility",
  "summary": "integration summary"
}"""
                    },
                    "stage_4_deepseek": {
                        "focus_areas": [
                            "Code Correctness",
                            "Performance Analysis",
                            "Security Review",
                            "Quality Assessment",
                            "Regression Detection"
                        ],
                        "system_prompt": """You are a senior quality assurance engineer. Perform a comprehensive final review of the integrated code.

Your verification should cover:
1. Code correctness and logic validation
2. Performance analysis
3. Security review
4. Code quality assessment
5. Best practices compliance
6. Potential regressions or side effects

Provide your response in JSON format:
{
  "verification_passed": true/false,
  "overall_quality_score": 1-10,
  "correctness_check": "pass/fail with details",
  "performance_assessment": "performance analysis",
  "security_review": "security evaluation",
  "warnings": ["list of any warnings or concerns"],
  "recommendations": ["list of further recommendations"],
  "final_assessment": "overall quality assessment",
  "regression_risks": ["potential regression risks identified"]
}"""
                    }
                },
                ProjectType.AI_ML.value: {
                    "name": "AI/ML Development",
                    "description": "Specialized analysis for machine learning and AI projects",
                    "stage_1_gemini": {
                        "focus_areas": [
                            "Model Architecture Issues",
                            "Training Stability",
                            "Data Processing Bugs",
                            "Numerical Stability",
                            "Performance Bottlenecks",
                            "Memory Management"
                        ],
                        "system_instruction": """You are an expert AI/ML code analyst. Focus on machine learning specific issues:

1. **Model Architecture**: Improper layer sizes, activation functions, initialization
2. **Training Stability**: Gradient issues, learning rate problems, convergence issues
3. **Data Processing**: Tensor shape mismatches, normalization issues, data leaks
4. **Numerical Stability**: NaN/Inf values, underflow/overflow, precision issues
5. **Performance**: Inefficient tensor operations, memory usage, GPU utilization
6. **ML Best Practices**: Evaluation metrics, validation strategies, reproducibility

Focus on ML-specific patterns and provide actionable recommendations for model improvement.

Respond in JSON format with ML-focused analysis."""
                    },
                    "stage_2_chatgpt": {
                        "system_prompt": """You are an expert ML engineer. Generate improved AI/ML code that addresses:

1. Fix tensor shape and dimension issues
2. Implement proper gradient handling and numerical stability
3. Optimize model architecture and training procedures
4. Improve data preprocessing and augmentation
5. Add proper evaluation and validation logic
6. Implement ML best practices (regularization, normalization, etc.)

Focus on creating robust, efficient, and maintainable ML code."""
                    },
                    "stage_3_claude": {
                        "system_prompt": """You are an expert ML system integrator. Ensure ML code integration maintains:

1. Consistent tensor operations and data flow
2. Proper model configuration and hyperparameters
3. Compatible data preprocessing pipelines
4. Consistent evaluation metrics and logging
5. Proper experiment tracking and reproducibility

Integrate improvements while preserving ML workflow consistency."""
                    },
                    "stage_4_deepseek": {
                        "system_prompt": """You are a senior ML quality engineer. Verify ML code for:

1. Model correctness and mathematical validity
2. Training stability and convergence properties
3. Data pipeline integrity and no data leakage
4. Proper evaluation methodology
5. Computational efficiency and scalability
6. Reproducibility and experiment tracking

Provide ML-specific quality assessment and recommendations."""
                    }
                },
                ProjectType.WEB_DEVELOPMENT.value: {
                    "name": "Web Development",
                    "description": "Frontend and backend web development focus",
                    "stage_1_gemini": {
                        "focus_areas": [
                            "XSS and CSRF Vulnerabilities",
                            "API Security",
                            "Performance Bottlenecks",
                            "Accessibility Issues",
                            "SEO Problems",
                            "Browser Compatibility"
                        ],
                        "system_instruction": """You are an expert web security and performance analyst. Focus on web-specific issues:

1. **Security**: XSS, CSRF, SQL injection, authentication flaws, session management
2. **Performance**: Bundle size, loading times, rendering bottlenecks, caching issues
3. **Accessibility**: ARIA compliance, keyboard navigation, screen reader support
4. **SEO**: Meta tags, semantic markup, performance metrics
5. **Compatibility**: Browser support, responsive design, progressive enhancement
6. **Best Practices**: Framework conventions, security headers, error handling

Provide web-focused analysis with actionable security and performance recommendations."""
                    },
                    "stage_2_chatgpt": {
                        "system_prompt": """You are an expert web developer. Generate improved web code that:

1. Fixes security vulnerabilities (XSS, CSRF, injection attacks)
2. Optimizes performance (lazy loading, code splitting, caching)
3. Improves accessibility (ARIA, semantic HTML, keyboard support)
4. Enhances SEO (meta tags, structured data, performance)
5. Ensures browser compatibility and responsive design
6. Implements web security best practices

Focus on creating secure, fast, and accessible web applications."""
                    }
                },
                ProjectType.SECURITY.value: {
                    "name": "Security-Focused",
                    "description": "Enhanced security analysis and hardening",
                    "stage_1_gemini": {
                        "focus_areas": [
                            "Injection Vulnerabilities",
                            "Authentication Flaws",
                            "Authorization Issues",
                            "Cryptographic Problems",
                            "Input Validation",
                            "Sensitive Data Exposure"
                        ],
                        "system_instruction": """You are a cybersecurity expert. Perform deep security analysis focusing on:

1. **Injection Attacks**: SQL, NoSQL, LDAP, OS command injection
2. **Authentication**: Weak passwords, session management, multi-factor auth
3. **Authorization**: Access controls, privilege escalation, RBAC issues
4. **Cryptography**: Weak algorithms, key management, implementation flaws
5. **Input Validation**: Sanitization, encoding, boundary checks
6. **Data Protection**: Encryption at rest/transit, PII handling, data leaks

Provide detailed security analysis with exploit scenarios and mitigation strategies."""
                    }
                }
            },
            "custom_prompts": {
                "user_defined": {}
            },
            "active_project_type": ProjectType.GENERAL.value
        }
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Saved prompt configuration to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config file: {e}")
    
    def set_project_type(self, project_type: ProjectType):
        """Set the active project type"""
        if project_type.value in self.config["project_types"]:
            self.config["active_project_type"] = project_type.value
            self._save_config(self.config)
            logger.info(f"Set active project type to: {project_type.value}")
        else:
            raise ValueError(f"Project type {project_type.value} not found in configuration")
    
    def get_active_prompts(self) -> Dict[str, str]:
        """Get prompts for the currently active project type"""
        active_type = self.config["active_project_type"]
        project_config = self.config["project_types"][active_type]
        
        return {
            "stage_1_system_instruction": project_config["stage_1_gemini"]["system_instruction"],
            "stage_2_system_prompt": project_config["stage_2_chatgpt"]["system_prompt"],
            "stage_3_system_prompt": project_config["stage_3_claude"]["system_prompt"],
            "stage_4_system_prompt": project_config["stage_4_deepseek"]["system_prompt"]
        }
    
    def customize_prompt(self, stage: str, prompt_text: str, project_type: Optional[ProjectType] = None):
        """Customize a specific stage prompt for a project type"""
        if project_type is None:
            project_type = ProjectType(self.config["active_project_type"])
        
        project_config = self.config["project_types"][project_type.value]
        
        stage_mapping = {
            "stage_1": ("stage_1_gemini", "system_instruction"),
            "stage_2": ("stage_2_chatgpt", "system_prompt"),
            "stage_3": ("stage_3_claude", "system_prompt"),
            "stage_4": ("stage_4_deepseek", "system_prompt")
        }
        
        if stage not in stage_mapping:
            raise ValueError(f"Invalid stage: {stage}. Must be one of {list(stage_mapping.keys())}")
        
        stage_key, prompt_key = stage_mapping[stage]
        project_config[stage_key][prompt_key] = prompt_text
        
        self._save_config(self.config)
        logger.info(f"Updated {stage} prompt for project type {project_type.value}")
    
    def create_custom_project_type(self, name: str, description: str, base_type: ProjectType = ProjectType.GENERAL):
        """Create a new custom project type based on an existing one"""
        custom_key = name.lower().replace(" ", "_")
        
        # Copy from base type
        base_config = self.config["project_types"][base_type.value].copy()
        base_config["name"] = name
        base_config["description"] = description
        
        self.config["project_types"][custom_key] = base_config
        self._save_config(self.config)
        
        logger.info(f"Created custom project type: {name} ({custom_key})")
        return custom_key
    
    def list_project_types(self) -> Dict[str, str]:
        """List all available project types"""
        return {
            key: config["name"] 
            for key, config in self.config["project_types"].items()
        }
    
    def get_project_info(self, project_type: str) -> Dict[str, Any]:
        """Get detailed information about a project type"""
        if project_type not in self.config["project_types"]:
            raise ValueError(f"Project type {project_type} not found")
        
        return self.config["project_types"][project_type]
    
    def export_prompts(self, filename: str):
        """Export current prompt configuration to a file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Exported prompts to {filename}")
        except Exception as e:
            logger.error(f"Error exporting prompts: {e}")
    
    def import_prompts(self, filename: str):
        """Import prompt configuration from a file"""
        try:
            with open(filename, 'r') as f:
                imported_config = json.load(f)
            
            # Validate and merge
            if "project_types" in imported_config:
                self.config["project_types"].update(imported_config["project_types"])
                self._save_config(self.config)
                logger.info(f"Imported prompts from {filename}")
            else:
                raise ValueError("Invalid configuration format")
        except Exception as e:
            logger.error(f"Error importing prompts: {e}")