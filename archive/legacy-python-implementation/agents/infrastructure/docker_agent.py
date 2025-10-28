"""
Docker Agent - Specialized agent for Docker operations in Claude Code

This agent handles Docker-related tasks including:
- Container management
- Image building and optimization
- Docker Compose orchestration
- Dockerfile creation and best practices
"""

from anthropic import Anthropic
import json
import os

class DockerAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a Docker specialist agent. Your expertise includes:

1. Container Management:
   - Creating, starting, stopping, and removing containers
   - Container networking and volumes
   - Resource management and limits
   
2. Image Operations:
   - Building optimized Docker images
   - Multi-stage builds
   - Layer caching strategies
   - Security scanning and vulnerability assessment
   
3. Dockerfile Best Practices:
   - Minimal base images
   - Proper layer ordering
   - Security hardening
   - Build optimization
   
4. Docker Compose:
   - Multi-container applications
   - Service orchestration
   - Network and volume configuration
   
5. Troubleshooting:
   - Container debugging
   - Log analysis
   - Performance issues

When asked to create or modify Docker configurations:
- Always use official base images when possible
- Implement multi-stage builds for compiled languages
- Follow principle of least privilege
- Add health checks
- Use .dockerignore files
- Minimize layer count
- Pin versions for reproducibility

Provide specific, actionable Docker commands and configurations."""

    def execute(self, task: str, context: dict = None) -> dict:
        """
        Execute a Docker-related task
        
        Args:
            task: The Docker task to perform
            context: Additional context (current directory, project info, etc.)
        
        Returns:
            dict with 'response' and 'artifacts' (Dockerfiles, compose files, etc.)
        """
        messages = [
            {
                "role": "user",
                "content": self._build_prompt(task, context)
            }
        ]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=self.system_prompt,
            messages=messages
        )
        
        return self._parse_response(response)
    
    def _build_prompt(self, task: str, context: dict = None) -> str:
        prompt = f"Task: {task}\n\n"
        
        if context:
            prompt += "Context:\n"
            if context.get("project_type"):
                prompt += f"- Project Type: {context['project_type']}\n"
            if context.get("language"):
                prompt += f"- Language: {context['language']}\n"
            if context.get("dependencies"):
                prompt += f"- Dependencies: {context['dependencies']}\n"
            if context.get("files"):
                prompt += f"- Relevant Files: {', '.join(context['files'])}\n"
            prompt += "\n"
        
        prompt += "Provide Docker configurations and commands as needed."
        return prompt
    
    def _parse_response(self, response) -> dict:
        """Parse the Claude response and extract artifacts"""
        text_content = ""
        artifacts = []
        
        for block in response.content:
            if block.type == "text":
                text_content += block.text
        
        # Extract code blocks that look like Docker artifacts
        import re
        
        # Find Dockerfiles
        dockerfile_pattern = r"```dockerfile\n(.*?)```"
        dockerfiles = re.findall(dockerfile_pattern, text_content, re.DOTALL)
        for df in dockerfiles:
            artifacts.append({
                "type": "dockerfile",
                "content": df.strip()
            })
        
        # Find docker-compose files
        compose_pattern = r"```ya?ml\n(.*?)```"
        compose_files = re.findall(compose_pattern, text_content, re.DOTALL)
        for cf in compose_files:
            if "version:" in cf or "services:" in cf:
                artifacts.append({
                    "type": "docker-compose",
                    "content": cf.strip()
                })
        
        return {
            "response": text_content,
            "artifacts": artifacts
        }


# Example usage
if __name__ == "__main__":
    agent = DockerAgent()
    
    # Example 1: Create a Dockerfile for a Python app
    result = agent.execute(
        task="Create a production-ready Dockerfile for a FastAPI application",
        context={
            "project_type": "web_api",
            "language": "python",
            "dependencies": "fastapi, uvicorn, pydantic"
        }
    )
    
    print("Response:", result["response"])
    print("\nArtifacts found:", len(result["artifacts"]))
    
    # Example 2: Docker Compose for microservices
    result = agent.execute(
        task="Create a docker-compose.yml for a microservices architecture with API, database, and Redis cache"
    )
    
    print("\n" + "="*50)
    print("Response:", result["response"])
