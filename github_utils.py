"""
GitHub Utilities for Multi-LLM Pipeline
Handles GitHub API interactions using GitPython and GitHub REST API
"""

import os
import logging
import requests
from typing import List, Dict, Any, Optional
from git import Repo, GitCommandError
import json
import base64
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubManager:
    def __init__(self):
        """Initialize GitHub client"""
        try:
            github_token = os.getenv('GITHUB_TOKEN')
            if not github_token:
                raise ValueError("GITHUB_TOKEN not found")
            
            self.github = Github(github_token)
            self.repository_name = os.getenv('REPOSITORY')
            if not self.repository_name:
                raise ValueError("REPOSITORY not found")
            
            self.repo = self.github.get_repo(self.repository_name)
            logger.info(f"GitHub client initialized for {self.repository_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize GitHub client: {e}")
            raise
    
    def get_pr_changed_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """Get list of changed files in a pull request"""
        try:
            pr = self.repo.get_pull(pr_number)
            files = []
            
            for file in pr.get_files():
                files.append({
                    'filename': file.filename,
                    'status': file.status,  # added, modified, removed
                    'additions': file.additions,
                    'deletions': file.deletions,
                    'changes': file.changes,
                    'patch': file.patch if hasattr(file, 'patch') else None
                })
            
            logger.info(f"Found {len(files)} changed files in PR #{pr_number}")
            return files
            
        except Exception as e:
            logger.error(f"Error getting changed files for PR #{pr_number}: {e}")
            raise
    
    def get_file_content(self, file_path: str, ref: str = None) -> Optional[str]:
        """Get content of a file from the repository"""
        try:
            if ref is None:
                # Get the content from the current branch
                content = self.repo.get_contents(file_path)
            else:
                content = self.repo.get_contents(file_path, ref=ref)
            
            if content.encoding == 'base64':
                decoded_content = base64.b64decode(content.content).decode('utf-8')
                return decoded_content
            else:
                return content.decoded_content.decode('utf-8')
                
        except Exception as e:
            logger.warning(f"Could not get content for {file_path}: {e}")
            return None
    
    def post_comment(self, pr_number: int, comment: str) -> bool:
        """Post a comment on a pull request"""
        try:
            pr = self.repo.get_pull(pr_number)
            pr.create_issue_comment(comment)
            logger.info(f"Posted comment on PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error posting comment on PR #{pr_number}: {e}")
            return False
    
    def update_pr_status(self, pr_number: int, state: str, description: str, 
                        context: str = "multi-llm-pipeline") -> bool:
        """Update PR status check"""
        try:
            pr = self.repo.get_pull(pr_number)
            commit = pr.head.sha
            
            # Map states to GitHub status states
            state_map = {
                'pending': 'pending',
                'running': 'pending', 
                'success': 'success',
                'completed': 'success',
                'failed': 'failure',
                'error': 'error'
            }
            
            github_state = state_map.get(state, 'pending')
            
            self.repo.get_commit(commit).create_status(
                state=github_state,
                description=description,
                context=context
            )
            
            logger.info(f"Updated PR #{pr_number} status to {github_state}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating PR #{pr_number} status: {e}")
            return False
    
    def get_pr_info(self, pr_number: int) -> Dict[str, Any]:
        """Get pull request information"""
        try:
            pr = self.repo.get_pull(pr_number)
            
            return {
                'number': pr.number,
                'title': pr.title,
                'body': pr.body,
                'state': pr.state,
                'base_branch': pr.base.ref,
                'head_branch': pr.head.ref,
                'author': pr.user.login,
                'created_at': pr.created_at.isoformat(),
                'updated_at': pr.updated_at.isoformat(),
                'commits': pr.commits,
                'additions': pr.additions,
                'deletions': pr.deletions,
                'changed_files': pr.changed_files
            }
            
        except Exception as e:
            logger.error(f"Error getting PR #{pr_number} info: {e}")
            return {}
    
    def add_pr_label(self, pr_number: int, label: str) -> bool:
        """Add a label to a pull request"""
        try:
            pr = self.repo.get_pull(pr_number)
            issue = self.repo.get_issue(pr_number)  # PRs are issues in GitHub API
            issue.add_to_labels(label)
            logger.info(f"Added label '{label}' to PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding label to PR #{pr_number}: {e}")
            return False
    
    def remove_pr_label(self, pr_number: int, label: str) -> bool:
        """Remove a label from a pull request"""
        try:
            issue = self.repo.get_issue(pr_number)
            issue.remove_from_labels(label)
            logger.info(f"Removed label '{label}' from PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing label from PR #{pr_number}: {e}")
            return False
    
    def create_pr_review(self, pr_number: int, body: str, event: str = "COMMENT") -> bool:
        """Create a review on a pull request"""
        try:
            pr = self.repo.get_pull(pr_number)
            
            # event can be: APPROVE, REQUEST_CHANGES, COMMENT
            pr.create_review(body=body, event=event)
            logger.info(f"Created review on PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating review on PR #{pr_number}: {e}")
            return False
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get repository information"""
        try:
            return {
                'name': self.repo.name,
                'full_name': self.repo.full_name,
                'description': self.repo.description,
                'language': self.repo.language,
                'default_branch': self.repo.default_branch,
                'private': self.repo.private,
                'created_at': self.repo.created_at.isoformat(),
                'updated_at': self.repo.updated_at.isoformat(),
                'size': self.repo.size,
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'open_issues': self.repo.open_issues_count
            }
            
        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            return {}
