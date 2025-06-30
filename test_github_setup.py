#!/usr/bin/env python3
"""
Quick test script to verify GitHub setup
"""
import os
from git_github_utils import GitHubManager

def test_github_setup():
    """Test GitHub connection and permissions"""
    print("Testing GitHub Setup...")
    print("-" * 40)
    
    # Check environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    repository = os.getenv('REPOSITORY')
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found")
        print("   Set it with: export GITHUB_TOKEN='your_token_here'")
        return False
        
    if not repository:
        print("❌ REPOSITORY not found")
        print("   Set it with: export REPOSITORY='username/repo-name'")
        return False
    
    print(f"✅ GITHUB_TOKEN: {'*' * 20}{github_token[-4:]}")
    print(f"✅ REPOSITORY: {repository}")
    
    # Test GitHub connection
    try:
        github = GitHubManager()
        repo_info = github.get_repository_info()
        
        print("\n📋 Repository Information:")
        print(f"   Name: {repo_info['name']}")
        print(f"   Owner: {repo_info['owner']}")
        print(f"   Full Name: {repo_info.get('full_name', 'N/A')}")
        print(f"   Private: {repo_info.get('private', 'N/A')}")
        
        # Test API access
        commits = github.list_recent_commits(limit=3)
        print(f"\n📝 Recent Commits: {len(commits)} found")
        for i, commit in enumerate(commits[:2], 1):
            print(f"   {i}. {commit.get('message', 'No message')[:50]}...")
        
        print("\n🎉 GitHub setup successful!")
        print("Your pipeline is ready to analyze pull requests.")
        return True
        
    except Exception as e:
        print(f"\n❌ GitHub setup failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your token has 'repo' permissions")
        print("2. Verify the repository name format: 'username/repo-name'")
        print("3. Make sure the repository exists and you have access")
        return False

if __name__ == "__main__":
    test_github_setup()