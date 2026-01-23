"""
GitHub API Integration for Publishing Inventory
"""
import os
import json
import base64
import requests
from typing import Optional, Tuple


class GitHubPublisher:
    """Handles publishing inventory and assets to GitHub."""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.config = self._load_config(config_path)
        self.base_url = "https://api.github.com"
    
    def _load_config(self, config_path: str) -> dict:
        """Load GitHub configuration."""
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        return {}
    
    def _get_headers(self) -> dict:
        """Get request headers with auth."""
        return {
            "Authorization": f"Bearer {self.config.get('github_token', '')}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def _get_file_sha(self, file_path: str) -> Optional[str]:
        """Get the SHA of an existing file (required for updates)."""
        owner = self.config.get("github_owner", "")
        repo = self.config.get("github_repo", "")
        branch = self.config.get("github_branch", "main")
        
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
        params = {"ref": branch}
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        
        if response.status_code == 200:
            return response.json().get("sha")
        return None
    
    def publish_file(self, file_path: str, content: str, message: str = "Update inventory") -> Tuple[bool, str]:
        """
        Publish a file to GitHub.
        
        Args:
            file_path: Path in the repo (e.g., "docs/inventory.json")
            content: File content as string
            message: Commit message
        
        Returns:
            Tuple of (success, message)
        """
        owner = self.config.get("github_owner", "")
        repo = self.config.get("github_repo", "")
        branch = self.config.get("github_branch", "main")
        
        if not all([owner, repo, self.config.get("github_token")]):
            return False, "GitHub configuration incomplete. Check config.json"
        
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
        
        # Encode content to base64
        content_bytes = content.encode("utf-8")
        content_base64 = base64.b64encode(content_bytes).decode("utf-8")
        
        # Build request body
        body = {
            "message": message,
            "content": content_base64,
            "branch": branch
        }
        
        # Get existing file SHA if updating
        sha = self._get_file_sha(file_path)
        if sha:
            body["sha"] = sha
        
        try:
            response = requests.put(url, headers=self._get_headers(), json=body)
            
            if response.status_code in [200, 201]:
                return True, "Published successfully!"
            else:
                error_msg = response.json().get("message", "Unknown error")
                return False, f"GitHub API error: {error_msg}"
        except requests.RequestException as e:
            return False, f"Network error: {str(e)}"
    
    def publish_image(self, local_path: str, repo_path: str) -> Tuple[bool, str]:
        """
        Upload an image file to GitHub.
        
        Args:
            local_path: Local file path
            repo_path: Path in the repo (e.g., "docs/Assets/image.jpg")
        
        Returns:
            Tuple of (success, message)
        """
        if not os.path.exists(local_path):
            return False, f"File not found: {local_path}"
        
        with open(local_path, "rb") as f:
            content_bytes = f.read()
        
        content_base64 = base64.b64encode(content_bytes).decode("utf-8")
        
        owner = self.config.get("github_owner", "")
        repo = self.config.get("github_repo", "")
        branch = self.config.get("github_branch", "main")
        
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{repo_path}"
        
        body = {
            "message": f"Add image: {os.path.basename(repo_path)}",
            "content": content_base64,
            "branch": branch
        }
        
        # Check if file exists
        sha = self._get_file_sha(repo_path)
        if sha:
            body["sha"] = sha
        
        try:
            response = requests.put(url, headers=self._get_headers(), json=body)
            
            if response.status_code in [200, 201]:
                return True, "Image uploaded!"
            else:
                error_msg = response.json().get("message", "Unknown error")
                return False, f"Upload error: {error_msg}"
        except requests.RequestException as e:
            return False, f"Network error: {str(e)}"
    
    def is_configured(self) -> bool:
        """Check if GitHub is properly configured."""
        required = ["github_token", "github_owner", "github_repo"]
        return all(self.config.get(key) for key in required)
