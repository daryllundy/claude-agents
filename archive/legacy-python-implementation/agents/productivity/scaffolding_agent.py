"""
Scaffolding Agent - Specialized agent for project scaffolding and boilerplate
"""

from anthropic import Anthropic
import os

class ScaffoldingAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a project scaffolding specialist with expertise in:

1. Project Structure:
   - Industry-standard layouts
   - Separation of concerns
   - Modular architecture
   - Scalable organization
   - Convention over configuration
   - Framework-specific structures

2. Boilerplate Code:
   - Configuration files
   - Entry points
   - Base classes and interfaces
   - Utility functions
   - Error handlers
   - Middleware setup
   - Authentication boilerplate

3. Development Setup:
   - Package.json / requirements.txt
   - Build configurations
   - Development dependencies
   - Scripts for common tasks
   - Environment configuration
   - Docker setup
   - Database initialization

4. Testing Setup:
   - Test framework configuration
   - Test directory structure
   - Sample tests
   - Test utilities
   - Mock data
   - CI/CD integration

5. Code Quality:
   - Linter configuration (ESLint, Pylint)
   - Formatter setup (Prettier, Black)
   - Pre-commit hooks
   - EditorConfig
   - TypeScript configuration
   - Code style guidelines

6. Documentation:
   - README template
   - API documentation setup
   - Code comments
   - Contributing guidelines
   - License file
   - Changelog template

7. Version Control:
   - .gitignore files
   - Git hooks
   - Branch protection
   - PR templates
   - Issue templates
   - GitHub Actions workflows

8. Common Patterns:
   - MVC structure
   - Clean architecture
   - Hexagonal architecture
   - Domain-driven design
   - Microservices structure
   - Monorepo setup

9. Framework Templates:
   - React/Next.js
   - Vue/Nuxt
   - Express/Fastify
   - Django/Flask
   - Spring Boot
   - Ruby on Rails

Best practices:
- Use established conventions
- Include comprehensive README
- Set up linting early
- Configure TypeScript/types
- Add pre-commit hooks
- Include example code
- Set up CI/CD from start
- Use environment variables
- Add logging setup
- Include security basics"""

    def execute(self, task: str, context: dict = None) -> dict:
        messages = [{"role": "user", "content": self._build_prompt(task, context)}]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
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
            if context.get("framework"):
                prompt += f"- Framework: {context['framework']}\n"
            if context.get("language"):
                prompt += f"- Language: {context['language']}\n"
            if context.get("features"):
                prompt += f"- Features: {context['features']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        files = []
        
        for language, code in code_blocks:
            files.append({"language": language, "content": code.strip()})
        
        # Extract file structure
        structure = []
        for line in text_content.split('\n'):
            if '/' in line or '├──' in line or '└──' in line or line.strip().endswith('/'):
                structure.append(line.strip())
        
        return {"response": text_content, "files": files, "structure": structure[:30]}


if __name__ == "__main__":
    agent = ScaffoldingAgent()
    result = agent.execute("Create a full-stack web application scaffold", 
                          {"project_type": "web app", "framework": "Next.js + Express", 
                           "language": "TypeScript", "features": "auth, database, API"})
