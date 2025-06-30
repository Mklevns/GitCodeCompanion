# GitHub Account Setup Guide

## Quick Setup Steps

### 1. Get Your GitHub Personal Access Token

1. Go to GitHub Settings: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "Multi-LLM Pipeline"
4. Select these permissions:
   - `repo` (Full control of private repositories)
   - `read:org` (Read org and team membership)
   - `workflow` (Update GitHub Action workflows)

5. Click "Generate token" and copy it immediately

### 2. Set Up Environment Variables

Add these to your environment (replace with your actual values):

```bash
export GITHUB_TOKEN="your_personal_access_token_here"
export REPOSITORY="your-username/your-repo-name"
```

### 3. Test Your Setup

Run this command to verify everything works:

```bash
python -c "
from git_github_utils import GitHubManager
try:
    github = GitHubManager()
    repo_info = github.get_repository_info()
    print(f'Connected to: {repo_info[\"name\"]}')
    print(f'Owner: {repo_info[\"owner\"]}')
    print('✅ GitHub setup successful!')
except Exception as e:
    print(f'❌ Setup failed: {e}')
"
```

## For GitHub Actions Integration

### 1. Add Secrets to Your Repository

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these repository secrets:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `GEMINI_API_KEY`: Your Google Gemini API key
- `DEEPSEEK_API_KEY`: Your DeepSeek API key

### 2. Create Workflow File

Create `.github/workflows/multi-llm-pipeline.yml` in your repository:

```yaml
name: Multi-LLM Code Quality Pipeline

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  code-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Pipeline
      run: |
        pip install openai anthropic google-genai requests gitpython
    
    - name: Run Multi-LLM Analysis
      run: |
        # Copy pipeline files to your repo
        curl -O https://raw.githubusercontent.com/your-pipeline-repo/main.py
        curl -O https://raw.githubusercontent.com/your-pipeline-repo/llm_clients.py
        # ... other files ...
        python main.py
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        REPOSITORY: ${{ github.repository }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        PR_NUMBER: ${{ github.event.pull_request.number }}
```

## Local Testing

### Test with a Specific Pull Request

```bash
export GITHUB_TOKEN="your_token"
export REPOSITORY="your-username/your-repo"
export PR_NUMBER="123"  # Replace with actual PR number

python main.py
```

### Test Repository Access

```bash
python -c "
from git_github_utils import GitHubManager
github = GitHubManager()

# Test basic access
print('Repository Info:')
repo = github.get_repository_info()
print(f'  Name: {repo[\"name\"]}')
print(f'  Owner: {repo[\"owner\"]}')

# Test PR access (if you have PRs)
try:
    prs = github._make_api_request('GET', f'/repos/{repo[\"full_name\"]}/pulls')
    print(f'  Open PRs: {len(prs)}')
except:
    print('  No PRs or access issue')
"
```

## Common Issues

### "REPOSITORY not found" Error
- Make sure you set the REPOSITORY environment variable
- Format should be "username/repo-name" (not the full URL)

### "Authentication failed" Error  
- Check your GitHub token has the right permissions
- Make sure the token isn't expired

### "API rate limit exceeded"
- GitHub has rate limits - wait a few minutes
- Consider using GitHub App instead of personal token for higher limits

## Repository Format Examples

Correct formats:
- `REPOSITORY="octocat/Hello-World"`
- `REPOSITORY="microsoft/vscode"`
- `REPOSITORY="your-username/your-project"`

Incorrect formats:
- `https://github.com/user/repo` (don't include URL)
- `user/repo.git` (don't include .git)
- `user` (missing repo name)