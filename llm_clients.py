"""
LLM Clients for Multi-LLM Pipeline
Handles communication with Gemini, ChatGPT, Claude, and DeepSeek
"""

import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
import requests

# Import LLM SDKs
from openai import OpenAI
from anthropic import Anthropic
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class LLMClients:
    def __init__(self):
        """Initialize all LLM clients"""
        self.setup_openai()
        self.setup_anthropic()
        self.setup_gemini()
        self.setup_deepseek()
    
    def setup_openai(self):
        """Setup OpenAI client"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found")
            
            self.openai_client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def setup_anthropic(self):
        """Setup Anthropic client"""
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found")
            
            self.anthropic_client = Anthropic(api_key=api_key)
            # The newest Anthropic model is "claude-sonnet-4-20250514", not "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022" nor "claude-3-sonnet-20240229"
            self.claude_model = "claude-sonnet-4-20250514"
            logger.info("Anthropic client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise
    
    def setup_gemini(self):
        """Setup Gemini client"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found")
            
            self.gemini_client = genai.Client(api_key=api_key)
            # The newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
            self.gemini_model = "gemini-2.5-pro"
            logger.info("Gemini client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def setup_deepseek(self):
        """Setup DeepSeek client"""
        try:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY not found")
            
            self.deepseek_api_key = api_key
            self.deepseek_base_url = "https://api.deepseek.com/v1"
            logger.info("DeepSeek client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize DeepSeek client: {e}")
            raise
    
    def call_gemini(self, prompt: str, system_instruction: str = "") -> str:
        """Call Gemini API with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                config = types.GenerateContentConfig()
                if system_instruction:
                    config.system_instruction = system_instruction
                
                response = self.gemini_client.models.generate_content(
                    model=self.gemini_model,
                    contents=prompt,
                    config=config
                )
                
                if response.text:
                    return response.text
                else:
                    raise ValueError("Empty response from Gemini")
                    
            except Exception as e:
                logger.warning(f"Gemini API attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
    
    def call_chatgpt(self, prompt: str, system_prompt: str = "", response_format: str = "text") -> str:
        """Call ChatGPT API with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                kwargs = {
                    # The newest OpenAI model is "gpt-4o" which was released May 13, 2024
                    "model": "gpt-4o",
                    "messages": messages,
                    "max_tokens": 4000
                }
                
                if response_format == "json":
                    kwargs["response_format"] = {"type": "json_object"}
                
                response = self.openai_client.chat.completions.create(**kwargs)
                
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content
                else:
                    raise ValueError("Empty response from ChatGPT")
                    
            except Exception as e:
                logger.warning(f"ChatGPT API attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
    
    def call_claude(self, prompt: str, system_prompt: str = "") -> str:
        """Call Claude API with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                kwargs = {
                    "model": self.claude_model,
                    "max_tokens": 4000,
                    "messages": [{"role": "user", "content": prompt}]
                }
                
                if system_prompt:
                    kwargs["system"] = system_prompt
                
                response = self.anthropic_client.messages.create(**kwargs)
                
                if response.content and len(response.content) > 0:
                    return response.content[0].text
                else:
                    raise ValueError("Empty response from Claude")
                    
            except Exception as e:
                logger.warning(f"Claude API attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
    
    def call_deepseek(self, prompt: str, system_prompt: str = "") -> str:
        """Call DeepSeek API with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json"
                }
                
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                payload = {
                    "model": "deepseek-chat",
                    "messages": messages,
                    "max_tokens": 4000,
                    "temperature": 0.1
                }
                
                response = requests.post(
                    f"{self.deepseek_base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                response.raise_for_status()
                result = response.json()
                
                if result.get("choices") and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    raise ValueError("Empty response from DeepSeek")
                    
            except Exception as e:
                logger.warning(f"DeepSeek API attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise
