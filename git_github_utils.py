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
        """Initialize GitHub client with GitPython and REST API"""
        try:
            self.github_token = os.getenv('GITHUB_TOKEN')
            if not self.github_token:
                raise ValueError("GITHUB_TOKEN not found")
            
            self.repository = os.getenv('REPOSITORY')
            if not self.repository:
                raise ValueError("REPOSITORY not found")
            
            # Extract owner and repo name
            self.owner, self.repo_name = self.repository.split('/')
            
            # Initialize GitPython repo if in a git directory
            try:
                self.git_repo = Repo('.')
                logger.info(f"Git repository initialized: {self.git_repo.working_dir}")
            except:
                self.git_repo = None
                logger.warning("Not in a git repository, some features may be limited")
            
            # GitHub API base URL
            self.api_base = "https://api.github.com"
            self.headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            
            logger.info(f"GitHub client initialized for repository: {self.repository}")
            
        except Exception as e:
            logger.error(f"Failed to initialize GitHub client: {e}")
            raise

    def _make_api_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make authenticated GitHub API request"""
        url = f"{self.api_base}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            raise

    def get_pr_changed_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """Get list of changed files in a pull request"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}/pulls/{pr_number}/files"
            files_data = self._make_api_request('GET', endpoint)
            
            changed_files = []
            for file_data in files_data:
                file_info = {
                    'filename': file_data['filename'],
                    'status': file_data['status'],  # added, modified, removed
                    'additions': file_data['additions'],
                    'deletions': file_data['deletions'],
                    'changes': file_data['changes'],
                    'patch': file_data.get('patch', ''),
                    'sha': file_data['sha'],
                    'blob_url': file_data['blob_url']
                }
                
                # Get file content if it's not deleted
                if file_data['status'] != 'removed':
                    try:
                        content = self.get_file_content(file_data['filename'])
                        file_info['content'] = content
                    except Exception as e:
                        logger.warning(f"Could not get content for {file_data['filename']}: {e}")
                        file_info['content'] = None
                
                changed_files.append(file_info)
            
            logger.info(f"Retrieved {len(changed_files)} changed files from PR #{pr_number}")
            return changed_files
            
        except Exception as e:
            logger.error(f"Failed to get PR changed files: {e}")
            return []

    def get_file_content(self, file_path: str, ref: str = None) -> Optional[str]:
        """Get content of a file from the repository"""
        try:
            # Use GitPython if available and no specific ref requested
            if self.git_repo and ref is None:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except FileNotFoundError:
                    logger.warning(f"File not found locally: {file_path}")
                except UnicodeDecodeError:
                    logger.warning(f"Binary file detected: {file_path}")
                    return None
            
            # Fallback to GitHub API
            endpoint = f"/repos/{self.owner}/{self.repo_name}/contents/{file_path}"
            if ref:
                endpoint += f"?ref={ref}"
            
            file_data = self._make_api_request('GET', endpoint)
            
            if file_data.get('type') == 'file':
                content = base64.b64decode(file_data['content']).decode('utf-8')
                return content
            else:
                logger.warning(f"Path is not a file: {file_path}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get file content for {file_path}: {e}")
            return None

    def post_comment(self, pr_number: int, comment: str) -> bool:
        """Post a comment on a pull request"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}/issues/{pr_number}/comments"
            data = {"body": comment}
            
            self._make_api_request('POST', endpoint, data)
            logger.info(f"Posted comment on PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to post comment on PR #{pr_number}: {e}")
            return False

    def update_pr_status(self, pr_number: int, state: str, description: str, 
                        context: str = "multi-llm-pipeline") -> bool:
        """Update PR status check"""
        try:
            # Get the PR to find the head SHA
            pr_endpoint = f"/repos/{self.owner}/{self.repo_name}/pulls/{pr_number}"
            pr_data = self._make_api_request('GET', pr_endpoint)
            sha = pr_data['head']['sha']
            
            # Create status check
            endpoint = f"/repos/{self.owner}/{self.repo_name}/statuses/{sha}"
            data = {
                "state": state,  # pending, success, error, failure
                "description": description,
                "context": context
            }
            
            self._make_api_request('POST', endpoint, data)
            logger.info(f"Updated PR #{pr_number} status: {state}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update PR status: {e}")
            return False

    def get_pr_info(self, pr_number: int) -> Dict[str, Any]:
        """Get pull request information"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}/pulls/{pr_number}"
            pr_data = self._make_api_request('GET', endpoint)
            
            return {
                'number': pr_data['number'],
                'title': pr_data['title'],
                'body': pr_data['body'],
                'state': pr_data['state'],
                'base_branch': pr_data['base']['ref'],
                'head_branch': pr_data['head']['ref'],
                'head_sha': pr_data['head']['sha'],
                'author': pr_data['user']['login'],
                'created_at': pr_data['created_at'],
                'updated_at': pr_data['updated_at']
            }
            
        except Exception as e:
            logger.error(f"Failed to get PR info: {e}")
            return {}

    def add_pr_label(self, pr_number: int, label: str) -> bool:
        """Add a label to a pull request"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}/issues/{pr_number}/labels"
            data = {"labels": [label]}
            
            self._make_api_request('POST', endpoint, data)
            logger.info(f"Added label '{label}' to PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add label to PR: {e}")
            return False

    def remove_pr_label(self, pr_number: int, label: str) -> bool:
        """Remove a label from a pull request"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}/issues/{pr_number}/labels/{label}"
            response = requests.delete(
                f"{self.api_base}{endpoint}",
                headers=self.headers
            )
            response.raise_for_status()
            
            logger.info(f"Removed label '{label}' from PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove label from PR: {e}")
            return False

    def create_pr_review(self, pr_number: int, body: str, event: str = "COMMENT") -> bool:
        """Create a review on a pull request"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}/pulls/{pr_number}/reviews"
            data = {
                "body": body,
                "event": event  # APPROVE, REQUEST_CHANGES, COMMENT
            }
            
            self._make_api_request('POST', endpoint, data)
            logger.info(f"Created review on PR #{pr_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create review: {e}")
            return False

    def get_repository_info(self) -> Dict[str, Any]:
        """Get repository information"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}"
            repo_data = self._make_api_request('GET', endpoint)
            
            return {
                'name': repo_data['name'],
                'full_name': repo_data['full_name'],
                'description': repo_data['description'],
                'language': repo_data['language'],
                'default_branch': repo_data['default_branch'],
                'private': repo_data['private'],
                'created_at': repo_data['created_at'],
                'updated_at': repo_data['updated_at']
            }
            
        except Exception as e:
            logger.error(f"Failed to get repository info: {e}")
            return {}

    def get_commit_info(self, sha: str = None) -> Dict[str, Any]:
        """Get commit information using GitPython or GitHub API"""
        try:
            if self.git_repo and sha is None:
                # Get latest commit from GitPython
                commit = self.git_repo.head.commit
                return {
                    'sha': commit.hexsha,
                    'message': commit.message.strip(),
                    'author': str(commit.author),
                    'date': commit.committed_datetime.isoformat(),
                    'files_changed': len(commit.stats.files)
                }
            else:
                # Use GitHub API
                sha = sha or "HEAD"
                endpoint = f"/repos/{self.owner}/{self.repo_name}/commits/{sha}"
                commit_data = self._make_api_request('GET', endpoint)
                
                return {
                    'sha': commit_data['sha'],
                    'message': commit_data['commit']['message'],
                    'author': commit_data['commit']['author']['name'],
                    'date': commit_data['commit']['author']['date'],
                    'files_changed': len(commit_data.get('files', []))
                }
                
        except Exception as e:
            logger.error(f"Failed to get commit info: {e}")
            return {}

    def get_branch_info(self, branch_name: str = None) -> Dict[str, Any]:
        """Get branch information"""
        try:
            if self.git_repo and branch_name is None:
                # Get current branch from GitPython
                branch_name = self.git_repo.active_branch.name
            
            branch_name = branch_name or "main"
            endpoint = f"/repos/{self.owner}/{self.repo_name}/branches/{branch_name}"
            branch_data = self._make_api_request('GET', endpoint)
            
            return {
                'name': branch_data['name'],
                'sha': branch_data['commit']['sha'],
                'protected': branch_data['protected'],
                'commit_message': branch_data['commit']['commit']['message']
            }
            
        except Exception as e:
            logger.error(f"Failed to get branch info: {e}")
            return {}

    def list_recent_commits(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent commits"""
        try:
            endpoint = f"/repos/{self.owner}/{self.repo_name}/commits"
            params = f"?per_page={limit}"
            
            response = requests.get(
                f"{self.api_base}{endpoint}{params}",
                headers=self.headers
            )
            response.raise_for_status()
            commits_data = response.json()
            
            commits = []
            for commit_data in commits_data:
                commits.append({
                    'sha': commit_data['sha'][:8],  # Short SHA
                    'message': commit_data['commit']['message'].split('\n')[0],  # First line
                    'author': commit_data['commit']['author']['name'],
                    'date': commit_data['commit']['author']['date']
                })
            
            return commits
            
        except Exception as e:
            logger.error(f"Failed to list recent commits: {e}")
            return []