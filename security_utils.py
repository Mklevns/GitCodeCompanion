"""
Security Utilities for Multi-LLM Pipeline
Handles input sanitization and security measures
"""

import re
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SecurityUtils:
    def __init__(self):
        """Initialize security utilities"""
        # Define potentially dangerous patterns
        self.dangerous_patterns = [
            # Command injection patterns
            r'(?:^|\s)(?:rm|del|format|shutdown|reboot|kill|killall)\s',
            r'(?:^|\s)(?:sudo|su|chmod|chown)\s',
            r'(?:^|\s)(?:wget|curl|nc|netcat|telnet|ssh)\s',
            
            # Code execution patterns
            r'eval\s*\(',
            r'exec\s*\(',
            r'system\s*\(',
            r'shell_exec\s*\(',
            r'passthru\s*\(',
            
            # File system access patterns
            r'(?:^|\s)(?:\.\.\/|\.\.\\)',
            r'\/etc\/passwd',
            r'\/etc\/shadow',
            
            # SQL injection patterns
            r'(?:union|select|insert|update|delete|drop|create|alter)\s+(?:all\s+)?(?:select|from|where|order|group|having|union|insert|update|delete|drop|create|alter)',
            
            # JavaScript execution patterns
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.dangerous_patterns]
    
    def sanitize_code_input(self, code: str) -> str:
        """
        Sanitize code input to prevent prompt injection and other security issues
        """
        try:
            if not code or not isinstance(code, str):
                return ""
            
            # Remove or escape potentially dangerous content
            sanitized = code
            
            # Limit code length to prevent DoS
            max_length = 50000  # 50KB limit
            if len(sanitized) > max_length:
                logger.warning(f"Code input truncated from {len(sanitized)} to {max_length} characters")
                sanitized = sanitized[:max_length] + "\n# ... (truncated for security)"
            
            # Remove or flag suspicious patterns
            for pattern in self.compiled_patterns:
                matches = pattern.findall(sanitized)
                if matches:
                    logger.warning(f"Potentially dangerous pattern detected: {matches}")
                    # Replace with comment instead of removing to maintain context
                    sanitized = pattern.sub(lambda m: f"# SANITIZED: {m.group(0)}", sanitized)
            
            # Escape special characters that could be used for prompt injection
            sanitized = self._escape_prompt_injection(sanitized)
            
            return sanitized
            
        except Exception as e:
            logger.error(f"Error sanitizing code input: {e}")
            return "# Error: Could not sanitize input safely"
    
    def _escape_prompt_injection(self, text: str) -> str:
        """
        Escape potential prompt injection attempts
        """
        try:
            # Patterns that could be used for prompt injection
            injection_patterns = [
                # Direct prompt manipulation
                (r'(?i)ignore\s+(?:previous|all|above)\s+(?:instructions?|prompts?|commands?)', 
                 '# SANITIZED: ignore instruction attempt'),
                (r'(?i)forget\s+(?:everything|all|previous)', 
                 '# SANITIZED: forget instruction attempt'),
                (r'(?i)now\s+(?:act|behave|pretend)\s+(?:as|like)', 
                 '# SANITIZED: role change attempt'),
                (r'(?i)you\s+are\s+now\s+', 
                 '# SANITIZED: identity change attempt'),
                
                # System message manipulation
                (r'(?i)system\s*:', 
                 '# SANITIZED: system message attempt'),
                (r'(?i)assistant\s*:', 
                 '# SANITIZED: assistant message attempt'),
                (r'(?i)human\s*:', 
                 '# SANITIZED: human message attempt'),
                
                # Escape sequence attempts
                (r'```\s*(?:end|stop|exit|quit)', 
                 '# SANITIZED: escape sequence attempt'),
            ]
            
            sanitized = text
            for pattern, replacement in injection_patterns:
                sanitized = re.sub(pattern, replacement, sanitized)
            
            return sanitized
            
        except Exception as e:
            logger.error(f"Error escaping prompt injection: {e}")
            return text
    
    def validate_file_path(self, file_path: str) -> bool:
        """
        Validate that file path is safe and within allowed boundaries
        """
        try:
            if not file_path or not isinstance(file_path, str):
                return False
            
            # Check for path traversal attempts
            if '..' in file_path or '~' in file_path:
                logger.warning(f"Path traversal attempt detected: {file_path}")
                return False
            
            # Check for absolute paths (should be relative)
            if file_path.startswith('/') or (len(file_path) > 1 and file_path[1] == ':'):
                logger.warning(f"Absolute path detected: {file_path}")
                return False
            
            # Check for special characters that shouldn't be in file paths
            dangerous_chars = ['<', '>', '|', '*', '?', '"']
            if any(char in file_path for char in dangerous_chars):
                logger.warning(f"Dangerous characters in path: {file_path}")
                return False
            
            # Ensure it's a code file (basic check)
            allowed_extensions = {
                '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', 
                '.rs', '.php', '.rb', '.swift', '.kt', '.scala', '.sh', 
                '.ps1', '.r', '.m', '.pl', '.lua', '.dart', '.elm'
            }
            
            if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
                logger.warning(f"Non-code file detected: {file_path}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating file path: {e}")
            return False
    
    def sanitize_api_response(self, response: str) -> str:
        """
        Sanitize API responses to prevent issues
        """
        try:
            if not response or not isinstance(response, str):
                return ""
            
            # Remove potential harmful content from responses
            sanitized = response
            
            # Remove any potential script tags or executable content
            sanitized = re.sub(r'<script[^>]*>.*?</script>', '# SANITIZED: script content', sanitized, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove potential data URIs that could be harmful
            sanitized = re.sub(r'data:(?:text|application)/[^;]+;base64,[A-Za-z0-9+/=]+', '# SANITIZED: data URI', sanitized)
            
            # Limit response length
            max_length = 100000  # 100KB limit
            if len(sanitized) > max_length:
                logger.warning(f"API response truncated from {len(sanitized)} to {max_length} characters")
                sanitized = sanitized[:max_length] + "\n# ... (truncated for security)"
            
            return sanitized
            
        except Exception as e:
            logger.error(f"Error sanitizing API response: {e}")
            return "# Error: Could not sanitize response safely"
    
    def check_rate_limits(self, api_name: str) -> bool:
        """
        Basic rate limiting check (can be enhanced with actual rate limiting logic)
        """
        try:
            # This is a placeholder for actual rate limiting implementation
            # In a real implementation, you would track API calls and enforce limits
            
            rate_limits = {
                'gemini': 60,  # calls per minute
                'openai': 50,
                'anthropic': 40,
                'deepseek': 30
            }
            
            # For now, just return True
            # In production, implement actual rate limiting with Redis or similar
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limits for {api_name}: {e}")
            return False
    
    def mask_sensitive_data(self, text: str) -> str:
        """
        Mask potentially sensitive data in text
        """
        try:
            if not text or not isinstance(text, str):
                return ""
            
            masked = text
            
            # API keys and tokens
            masked = re.sub(r'(?i)(?:api[_-]?key|token|secret)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?', 
                          r'api_key="***MASKED***"', masked)
            
            # Email addresses
            masked = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                          '***EMAIL_MASKED***', masked)
            
            # Potential passwords
            masked = re.sub(r'(?i)(?:password|passwd|pwd)["\']?\s*[:=]\s*["\']?([^\s"\']{8,})["\']?', 
                          r'password="***MASKED***"', masked)
            
            # IP addresses (basic masking)
            masked = re.sub(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', 
                          '***IP_MASKED***', masked)
            
            return masked
            
        except Exception as e:
            logger.error(f"Error masking sensitive data: {e}")
            return text
    
    def validate_llm_response(self, response: str, expected_format: str = "text") -> bool:
        """
        Validate LLM response format and content
        """
        try:
            if not response or not isinstance(response, str):
                return False
            
            # Check for minimum length
            if len(response.strip()) < 10:
                logger.warning("LLM response too short")
                return False
            
            # Check for format-specific validation
            if expected_format == "json":
                try:
                    json.loads(response)
                except json.JSONDecodeError:
                    logger.warning("Invalid JSON in LLM response")
                    return False
            
            # Check for obvious error indicators
            error_indicators = [
                "I'm sorry, I can't",
                "I cannot",
                "I'm not able to",
                "Error:",
                "Exception:",
                "Failed to"
            ]
            
            response_lower = response.lower()
            if any(indicator.lower() in response_lower for indicator in error_indicators):
                logger.warning("Error indicator found in LLM response")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating LLM response: {e}")
            return False
