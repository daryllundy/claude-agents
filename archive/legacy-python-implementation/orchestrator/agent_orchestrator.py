"""
Agent Orchestrator - Master coordinator for all sub-agents in Claude Code

This orchestrator intelligently routes tasks to the appropriate specialized agents
and can coordinate multi-agent workflows for complex tasks.
"""

from anthropic import Anthropic
import os
from typing import Dict, List, Any, Optional

# Import all specialized agents
from docker_agent import DockerAgent
from test_suite_agent import TestSuiteAgent
from devops_agent import DevOpsAgent
from security_agent import SecurityAgent
from database_agent import DatabaseAgent
from api_design_agent import APIDesignAgent
from frontend_agent import FrontendAgent
from performance_agent import PerformanceAgent
from refactoring_agent import RefactoringAgent
from documentation_agent import DocumentationAgent
from code_review_agent import CodeReviewAgent
from data_science_agent import DataScienceAgent
from mobile_agent import MobileAgent
from game_dev_agent import GameDevelopmentAgent
from observability_agent import ObservabilityAgent
from migration_agent import MigrationAgent
from dependency_agent import DependencyAgent
from scaffolding_agent import ScaffoldingAgent
from git_agent import GitAgent
from debugging_agent import DebuggingAgent
from validation_agent import ValidationAgent
from architecture_agent import ArchitectureAgent
from localization_agent import LocalizationAgent
from compliance_agent import ComplianceAgent


class AgentOrchestrator:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        # Initialize all specialized agents
        self.agents = {
            "docker": DockerAgent(api_key),
            "testing": TestSuiteAgent(api_key),
            "devops": DevOpsAgent(api_key),
            "security": SecurityAgent(api_key),
            "database": DatabaseAgent(api_key),
            "api_design": APIDesignAgent(api_key),
            "frontend": FrontendAgent(api_key),
            "performance": PerformanceAgent(api_key),
            "refactoring": RefactoringAgent(api_key),
            "documentation": DocumentationAgent(api_key),
            "code_review": CodeReviewAgent(api_key),
            "data_science": DataScienceAgent(api_key),
            "mobile": MobileAgent(api_key),
            "game_dev": GameDevelopmentAgent(api_key),
            "observability": ObservabilityAgent(api_key),
            "migration": MigrationAgent(api_key),
            "dependency": DependencyAgent(api_key),
            "scaffolding": ScaffoldingAgent(api_key),
            "git": GitAgent(api_key),
            "debugging": DebuggingAgent(api_key),
            "validation": ValidationAgent(api_key),
            "architecture": ArchitectureAgent(api_key),
            "localization": LocalizationAgent(api_key),
            "compliance": ComplianceAgent(api_key),
        }
        
        self.routing_prompt = """You are an intelligent agent router. Analyze the task and determine which specialized agent(s) should handle it.

Available agents:
- docker: Container operations, Dockerfiles, Docker Compose
- testing: Unit tests, integration tests, test coverage
- devops: CI/CD, infrastructure, deployments
- security: Security analysis, vulnerability detection
- database: Schema design, queries, migrations
- api_design: REST/GraphQL API design, documentation
- frontend: React/Vue/Angular, UI components, state management
- performance: Optimization, profiling, bottleneck analysis
- refactoring: Code improvement, design patterns, cleanup
- documentation: Code docs, README, API documentation
- code_review: Code quality review, best practices
- data_science: ML pipelines, data preprocessing, modeling
- mobile: iOS/Android, React Native, Flutter
- game_dev: Game mechanics, physics, rendering
- observability: Monitoring, logging, metrics, tracing
- migration: System migrations, upgrades, data migration
- dependency: Dependency management, updates, audits
- scaffolding: Project setup, boilerplate generation
- git: Git operations, commit messages, branching
- debugging: Bug analysis, troubleshooting, fixes
- validation: Input validation, data validation, schemas
- architecture: System design, architectural patterns
- localization: i18n, translations, RTL support
- compliance: GDPR, HIPAA, accessibility, regulations

Respond with a JSON object:
{
  "primary_agent": "agent_name",
  "secondary_agents": ["agent_name1", "agent_name2"],
  "reasoning": "Why these agents were selected",
  "workflow": "Sequential or parallel execution plan"
}

If multiple agents are needed, explain the workflow."""

    def route_task(self, task: str, context: dict = None) -> dict:
        """Determine which agent(s) should handle the task"""
        
        prompt = f"Task: {task}\n\n"
        if context:
            prompt += f"Context: {context}\n\n"
        prompt += "Determine which agent(s) should handle this task."
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.routing_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        import re
        
        text = response.content[0].text
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            routing = json.loads(json_match.group())
            return routing
        
        # Fallback to simple routing based on keywords
        return self._simple_routing(task)
    
    def _simple_routing(self, task: str) -> dict:
        """Fallback routing based on keyword matching"""
        task_lower = task.lower()
        
        routing_map = {
            "docker": ["docker", "container", "dockerfile", "compose"],
            "testing": ["test", "unit test", "integration test", "coverage"],
            "devops": ["cicd", "ci/cd", "deploy", "pipeline", "kubernetes"],
            "security": ["security", "vulnerability", "exploit", "penetration"],
            "database": ["database", "sql", "schema", "query", "migration"],
            "api_design": ["api", "rest", "graphql", "endpoint"],
            "frontend": ["react", "vue", "angular", "component", "ui"],
            "performance": ["performance", "optimize", "slow", "bottleneck"],
            "refactoring": ["refactor", "clean", "improve", "smell"],
            "documentation": ["document", "readme", "docs", "comment"],
            "code_review": ["review", "quality", "best practice"],
            "debugging": ["debug", "bug", "error", "fix", "issue"],
            "git": ["git", "commit", "branch", "merge", "pull request"],
            "scaffolding": ["scaffold", "boilerplate", "setup", "initialize"],
        }
        
        for agent, keywords in routing_map.items():
            if any(keyword in task_lower for keyword in keywords):
                return {
                    "primary_agent": agent,
                    "secondary_agents": [],
                    "reasoning": f"Task contains keywords related to {agent}",
                    "workflow": "single"
                }
        
        # Default to code_review for general tasks
        return {
            "primary_agent": "code_review",
            "secondary_agents": [],
            "reasoning": "Default routing for general code tasks",
            "workflow": "single"
        }
    
    def execute(self, task: str, context: dict = None) -> dict:
        """
        Execute a task by routing to appropriate agent(s)
        
        Args:
            task: The task to execute
            context: Additional context for the task
        
        Returns:
            dict with results from all agents involved
        """
        # Route the task
        routing = self.route_task(task, context)
        
        results = {
            "routing": routing,
            "primary_result": None,
            "secondary_results": [],
            "summary": ""
        }
        
        # Execute primary agent
        primary_agent_name = routing["primary_agent"]
        if primary_agent_name in self.agents:
            primary_agent = self.agents[primary_agent_name]
            results["primary_result"] = primary_agent.execute(task, context)
        
        # Execute secondary agents if needed
        for agent_name in routing.get("secondary_agents", []):
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                secondary_result = agent.execute(task, context)
                results["secondary_results"].append({
                    "agent": agent_name,
                    "result": secondary_result
                })
        
        # Generate summary
        results["summary"] = self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: dict) -> str:
        """Generate a summary of the multi-agent execution"""
        summary = f"Task routed to: {results['routing']['primary_agent']}\n"
        summary += f"Reasoning: {results['routing']['reasoning']}\n\n"
        
        if results["primary_result"]:
            summary += "Primary agent completed successfully.\n"
        
        if results["secondary_results"]:
            summary += f"Additional agents involved: {len(results['secondary_results'])}\n"
        
        return summary
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())
    
    def get_agent(self, agent_name: str):
        """Get a specific agent by name"""
        return self.agents.get(agent_name)


# Example usage
if __name__ == "__main__":
    orchestrator = AgentOrchestrator()
    
    # Example 1: Simple task
    result = orchestrator.execute(
        "Create a Dockerfile for a Python FastAPI application"
    )
    print("Routed to:", result["routing"]["primary_agent"])
    print("\nSummary:", result["summary"])
    
    # Example 2: Complex multi-agent task
    result = orchestrator.execute(
        "Setup a new microservices project with Docker, CI/CD, and monitoring",
        context={"language": "Node.js", "platform": "AWS"}
    )
    print("\n" + "="*50)
    print("Complex Task Routing:")
    print("Primary:", result["routing"]["primary_agent"])
    print("Secondary:", result["routing"]["secondary_agents"])
    
    # Example 3: List all available agents
    print("\n" + "="*50)
    print("Available Agents:")
    for agent in orchestrator.list_agents():
        print(f"  - {agent}")
