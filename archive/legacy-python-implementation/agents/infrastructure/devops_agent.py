"""
DevOps Agent - Specialized agent for DevOps and CI/CD in Claude Code

This agent handles:
- CI/CD pipeline configuration
- Infrastructure as Code (IaC)
- Deployment strategies
- Monitoring and observability
- Cloud platform configurations
"""

from anthropic import Anthropic
import json
import os
from typing import List, Dict, Optional

class DevOpsAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a DevOps specialist agent with expertise in:

1. CI/CD Pipelines:
   - GitHub Actions, GitLab CI, Jenkins, CircleCI
   - Build automation and testing
   - Deployment automation
   - Pipeline optimization
   - Artifact management

2. Infrastructure as Code:
   - Terraform for multi-cloud provisioning
   - AWS CloudFormation
   - Kubernetes manifests and Helm charts
   - Ansible for configuration management
   - Pulumi for modern IaC

3. Cloud Platforms:
   - AWS (EC2, ECS, Lambda, RDS, S3, CloudWatch)
   - Google Cloud Platform
   - Azure
   - DigitalOcean, Linode

4. Container Orchestration:
   - Kubernetes deployments, services, ingress
   - Helm chart creation
   - Service mesh (Istio, Linkerd)
   - Auto-scaling configurations

5. Monitoring & Observability:
   - Prometheus and Grafana
   - ELK stack (Elasticsearch, Logstash, Kibana)
   - Application Performance Monitoring (APM)
   - Log aggregation and analysis
   - Alerting strategies

6. Deployment Strategies:
   - Blue-green deployments
   - Canary releases
   - Rolling updates
   - Feature flags

7. Security & Compliance:
   - Secret management (Vault, AWS Secrets Manager)
   - IAM and RBAC
   - Network security groups
   - Compliance scanning

When creating DevOps configurations:
- Follow infrastructure as code best practices
- Use version control for all configurations
- Implement proper secret management
- Add health checks and monitoring
- Use descriptive naming conventions
- Include documentation and comments
- Plan for rollback scenarios
- Consider cost optimization
- Implement security by default"""

    def execute(self, task: str, context: dict = None) -> dict:
        """
        Execute a DevOps-related task
        
        Args:
            task: The DevOps task to perform
            context: Platform, tools, project requirements, etc.
        
        Returns:
            dict with 'response', 'configs', and 'commands'
        """
        messages = [
            {
                "role": "user",
                "content": self._build_prompt(task, context)
            }
        ]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=6000,
            system=self.system_prompt,
            messages=messages
        )
        
        return self._parse_response(response)
    
    def _build_prompt(self, task: str, context: dict = None) -> str:
        prompt = f"Task: {task}\n\n"
        
        if context:
            prompt += "Context:\n"
            
            if context.get("platform"):
                prompt += f"- Cloud Platform: {context['platform']}\n"
            
            if context.get("ci_cd_tool"):
                prompt += f"- CI/CD Tool: {context['ci_cd_tool']}\n"
            
            if context.get("orchestration"):
                prompt += f"- Orchestration: {context['orchestration']}\n"
            
            if context.get("language"):
                prompt += f"- Application Language: {context['language']}\n"
            
            if context.get("environment"):
                prompt += f"- Environment: {context['environment']}\n"
            
            if context.get("requirements"):
                prompt += f"- Requirements: {context['requirements']}\n"
            
            if context.get("existing_infrastructure"):
                prompt += f"- Existing Infrastructure:\n{context['existing_infrastructure']}\n"
            
            prompt += "\n"
        
        prompt += "Provide complete, production-ready configurations."
        return prompt
    
    def _parse_response(self, response) -> dict:
        """Parse the Claude response and extract configurations"""
        text_content = ""
        configs = []
        commands = []
        
        for block in response.content:
            if block.type == "text":
                text_content += block.text
        
        # Extract code blocks
        import re
        code_pattern = r"```(\w+)\n(.*?)```"
        code_blocks = re.findall(code_pattern, text_content, re.DOTALL)
        
        config_types = {
            'yaml': 'yaml_config',
            'yml': 'yaml_config',
            'hcl': 'terraform',
            'tf': 'terraform',
            'json': 'json_config',
            'dockerfile': 'dockerfile',
            'bash': 'script',
            'sh': 'script'
        }
        
        for language, code in code_blocks:
            config_type = config_types.get(language.lower(), 'config')
            configs.append({
                "type": config_type,
                "language": language,
                "content": code.strip()
            })
        
        # Extract command blocks (lines starting with $, >, or common command prefixes)
        command_pattern = r'(?:^|\n)[$>]\s*(.+?)(?=\n|$)'
        found_commands = re.findall(command_pattern, text_content, re.MULTILINE)
        commands.extend(found_commands)
        
        return {
            "response": text_content,
            "configs": configs,
            "commands": commands
        }
    
    def create_pipeline(self, language: str, ci_tool: str, 
                       test_command: str = None, build_command: str = None) -> dict:
        """Create a CI/CD pipeline configuration"""
        task = f"Create a complete CI/CD pipeline for a {language} application"
        
        requirements = []
        if test_command:
            requirements.append(f"Run tests with: {test_command}")
        if build_command:
            requirements.append(f"Build with: {build_command}")
        requirements.extend([
            "Include linting and code quality checks",
            "Add security scanning",
            "Deploy to staging on merge to main",
            "Deploy to production on tag creation"
        ])
        
        context = {
            "language": language,
            "ci_cd_tool": ci_tool,
            "requirements": "\n".join(f"  - {req}" for req in requirements)
        }
        
        return self.execute(task, context)
    
    def create_infrastructure(self, platform: str, components: List[str]) -> dict:
        """Create infrastructure as code"""
        task = f"Create infrastructure configuration for: {', '.join(components)}"
        context = {
            "platform": platform,
            "requirements": f"Components needed: {', '.join(components)}"
        }
        return self.execute(task, context)
    
    def setup_monitoring(self, stack: str = "prometheus") -> dict:
        """Setup monitoring and observability"""
        task = f"Create a monitoring setup using {stack}"
        context = {
            "requirements": """
  - Application metrics collection
  - System resource monitoring
  - Log aggregation
  - Alerting rules for critical issues
  - Dashboards for visualization
"""
        }
        return self.execute(task, context)


# Example usage
if __name__ == "__main__":
    agent = DevOpsAgent()
    
    # Example 1: Create GitHub Actions pipeline
    result = agent.create_pipeline(
        language="python",
        ci_tool="GitHub Actions",
        test_command="pytest",
        build_command="python -m build"
    )
    
    print("Pipeline Configuration Created")
    print(f"Number of config files: {len(result['configs'])}")
    print(f"Number of commands: {len(result['commands'])}")
    
    # Example 2: Create Kubernetes deployment
    k8s_result = agent.execute(
        task="Create Kubernetes manifests for a web application with database",
        context={
            "orchestration": "Kubernetes",
            "requirements": """
  - Web application with 3 replicas
  - PostgreSQL database
  - Redis cache
  - Ingress with TLS
  - Auto-scaling based on CPU
  - Resource limits and requests
"""
        }
    )
    
    print("\n" + "="*50)
    print("Kubernetes Configs Created")
    for config in k8s_result['configs']:
        print(f"  - {config['type']}")
    
    # Example 3: Setup monitoring
    monitoring_result = agent.setup_monitoring(stack="prometheus")
    print("\n" + "="*50)
    print("Monitoring Setup:")
    print(monitoring_result["response"][:500] + "...")
