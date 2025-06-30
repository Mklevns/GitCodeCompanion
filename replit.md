# Multi-LLM Code Quality Pipeline

## Overview

This repository implements a sophisticated multi-LLM code quality pipeline designed to integrate with GitHub for automated code analysis and improvement. The system orchestrates four different Large Language Models (LLMs) - Gemini, ChatGPT, Claude, and DeepSeek - in a sequential "gauntlet" approach to provide comprehensive code analysis, generation, integration, and verification.

The pipeline is triggered by GitHub pull requests and provides automated code quality assessment, bug detection, security analysis, and improvement suggestions through a four-stage process where each LLM specializes in a specific aspect of code quality.

## System Architecture

The system follows a modular, event-driven architecture with the following key characteristics:

### Architecture Pattern
- **Event-Driven Pipeline**: Triggered by GitHub webhook events (PR creation/updates)
- **Sequential Processing**: Four-stage pipeline where each stage depends on the previous one
- **Stateful Orchestration**: Main orchestrator maintains pipeline state throughout execution
- **Modular Design**: Separated concerns across different utility modules

### Core Components
- **Main Orchestrator** (`main.py`): Central pipeline coordinator and state manager
- **LLM Clients** (`llm_clients.py`): Unified interface for multiple LLM providers
- **GitHub Integration** (`github_utils.py`): GitHub API interaction and PR management
- **Pipeline Stages** (`pipeline_stages.py`): Implementation of the four-stage analysis process
- **Security Layer** (`security_utils.py`): Input sanitization and security measures
- **Report Generation** (`report_generator.py`): Comprehensive reporting system

## Key Components

### 1. LLM Integration Layer
**Problem**: Need to integrate multiple LLM providers with different APIs and capabilities
**Solution**: Unified client interface that abstracts provider-specific implementations
- Supports OpenAI (ChatGPT), Anthropic (Claude), Google (Gemini), and DeepSeek
- Handles authentication and rate limiting for each provider
- Provides consistent error handling across all LLM interactions

### 2. GitHub Integration
**Problem**: Seamless integration with GitHub workflows and pull request management
**Solution**: Dedicated GitHub manager using PyGithub library
- Retrieves changed files from pull requests
- Posts pipeline updates and results as PR comments
- Manages repository access and authentication via GitHub tokens

### 3. Security Framework
**Problem**: Preventing prompt injection and malicious code execution
**Solution**: Multi-layered security approach with input sanitization
- Pattern-based detection of dangerous code constructs
- Input sanitization for all user-provided code
- Secure handling of API keys and sensitive data

### 4. Four-Stage Pipeline Architecture
**Problem**: Need comprehensive code analysis covering multiple quality dimensions
**Solution**: Sequential pipeline where each LLM specializes in specific analysis types

**Stage 1 - Gemini Analysis**: Deep code analysis for bugs, performance, and security
**Stage 2 - ChatGPT Generation**: Code improvement and fix generation
**Stage 3 - Claude Integration**: Seamless integration of improvements with existing code
**Stage 4 - DeepSeek Verification**: Final verification and quality assurance

## Data Flow

1. **Trigger**: GitHub webhook fires on PR creation/update
2. **Initialization**: Pipeline validates environment and initializes all clients
3. **Code Extraction**: Retrieves changed files from the pull request
4. **Stage 1**: Gemini performs comprehensive code analysis
5. **Stage 2**: ChatGPT generates improvements based on Gemini's analysis
6. **Stage 3**: Claude integrates improvements with existing codebase
7. **Stage 4**: DeepSeek performs final verification
8. **Reporting**: Comprehensive report generated and posted to PR
9. **Cleanup**: Pipeline state saved and resources cleaned up

Each stage passes structured data to the next, maintaining context and building upon previous analyses.

## External Dependencies

### LLM Providers
- **OpenAI API**: For ChatGPT integration (requires OPENAI_API_KEY)
- **Anthropic API**: For Claude integration (requires ANTHROPIC_API_KEY)
- **Google Generative AI**: For Gemini integration (requires GEMINI_API_KEY)
- **DeepSeek API**: For final verification (requires DEEPSEEK_API_KEY)

### GitHub Integration
- **GitHub API**: Via PyGithub library (requires GITHUB_TOKEN)
- **Repository Access**: Requires REPOSITORY environment variable

### Python Dependencies
- `PyGithub`: GitHub API integration
- `openai`: OpenAI API client
- `anthropic`: Anthropic API client
- `google-generativeai`: Google's Gemini API client
- `requests`: HTTP client for custom API calls

## Deployment Strategy

### Environment Configuration
The application expects the following environment variables:
- `GITHUB_TOKEN`: GitHub API access token
- `REPOSITORY`: Target repository in format "owner/repo"
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GEMINI_API_KEY`: Google Generative AI API key
- `DEEPSEEK_API_KEY`: DeepSeek API key

### GitHub Actions Integration
**Problem**: Automated execution within GitHub's CI/CD pipeline
**Solution**: Designed as a GitHub Action that can be triggered by PR events
- Configurable trigger conditions (PR opened, updated, etc.)
- Supports both public and private repositories
- Secure secret management through GitHub's encrypted secrets

### Scalability Considerations
- Stateless design allows for horizontal scaling
- Rate limiting implementation for all LLM providers
- Error recovery and retry mechanisms for robust operation
- Modular architecture supports easy addition of new LLM providers

## Changelog

```
Changelog:
- June 30, 2025: Initial setup and architecture design
- June 30, 2025: Successfully implemented all 4 pipeline stages
- June 30, 2025: All LLM clients operational (OpenAI, Anthropic, Gemini, DeepSeek)
- June 30, 2025: Demo mode successfully processing sample code files
- June 30, 2025: GitHub integration ready for production deployment
- June 30, 2025: Comprehensive security layer and reporting system completed
- June 30, 2025: Added customizable prompt system with project-specific optimization
- June 30, 2025: Created CLI tool for prompt management and configuration
- June 30, 2025: Implemented predefined project types (AI/ML, Web, Security, General)
- June 30, 2025: Added custom project type creation and prompt import/export
- June 30, 2025: Implemented LangChain framework for advanced workflow management
- June 30, 2025: Added GitPython integration replacing conflicting GitHub library
- June 30, 2025: Created advanced pipeline with memory, conditional logic, and retry mechanisms
- June 30, 2025: Established comprehensive deployment guide and production configurations
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
Target repository: JanusAI_V2 (multimodal AI project)
GitHub repository: https://github.com/Mklevns/JanusAI_V2
Focus: AI/ML code analysis with emphasis on vision-language models
```