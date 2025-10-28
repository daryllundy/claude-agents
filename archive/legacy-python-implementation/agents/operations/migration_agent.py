"""
Migration Agent - Specialized agent for system and code migrations
"""

from anthropic import Anthropic
import os

class MigrationAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a migration specialist with expertise in:

1. Migration Types:
   - Database migrations
   - Cloud platform migrations
   - Framework upgrades
   - Language version upgrades
   - Microservices decomposition
   - Monolith to microservices
   - API versioning migrations

2. Migration Strategies:
   - Big bang migration
   - Strangler fig pattern
   - Branch by abstraction
   - Parallel run
   - Blue-green deployment
   - Canary releases
   - Feature flags

3. Database Migrations:
   - Schema changes
   - Data transformation
   - Zero-downtime migrations
   - Backward compatibility
   - Rollback procedures
   - Migration tools (Flyway, Liquibase, Alembic)

4. Cloud Migrations:
   - Lift and shift
   - Replatforming
   - Refactoring for cloud
   - Multi-cloud strategies
   - Cost optimization
   - AWS, Azure, GCP migrations

5. Code Migrations:
   - Dependency upgrades
   - Breaking change handling
   - API compatibility layers
   - Deprecation strategies
   - Code modernization
   - Technical debt reduction

6. Data Migration:
   - ETL pipelines
   - Data validation
   - Data integrity checks
   - Incremental migrations
   - Cutover planning
   - Data reconciliation

7. Testing:
   - Migration testing strategy
   - Smoke tests
   - Integration tests
   - Performance testing
   - Rollback testing
   - Production validation

8. Risk Management:
   - Risk assessment
   - Mitigation strategies
   - Rollback plans
   - Communication plans
   - Stakeholder management
   - Change management

Best practices:
- Plan thoroughly before starting
- Start with non-critical systems
- Maintain backward compatibility
- Test extensively
- Have rollback procedures
- Monitor during and after migration
- Communicate clearly
- Document everything
- Migrate incrementally when possible
- Validate data integrity"""

    def execute(self, task: str, context: dict = None) -> dict:
        messages = [{"role": "user", "content": self._build_prompt(task, context)}]
        
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
            if context.get("from_system"):
                prompt += f"- From: {context['from_system']}\n"
            if context.get("to_system"):
                prompt += f"- To: {context['to_system']}\n"
            if context.get("constraints"):
                prompt += f"- Constraints: {context['constraints']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        migration_scripts = []
        
        for language, code in code_blocks:
            migration_scripts.append({"language": language, "content": code.strip()})
        
        # Extract steps/phases
        steps = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['step', 'phase', 'stage']):
                steps.append(line.strip())
        
        return {"response": text_content, "migration_scripts": migration_scripts, "steps": steps[:10]}


if __name__ == "__main__":
    agent = MigrationAgent()
    result = agent.execute("Create a migration plan from MongoDB to PostgreSQL", 
                          {"from_system": "MongoDB", "to_system": "PostgreSQL", 
                           "constraints": "Zero downtime required"})
