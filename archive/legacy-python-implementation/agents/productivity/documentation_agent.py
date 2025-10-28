"""
Documentation Agent - Specialized agent for code documentation
"""

from anthropic import Anthropic
import os

class DocumentationAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a documentation specialist with expertise in:

1. Code Documentation:
   - Function/method docstrings
   - Class documentation
   - Module-level documentation
   - Inline comments (when needed)
   - Type hints and annotations
   - Documentation standards (JSDoc, Sphinx, Javadoc)

2. API Documentation:
   - Endpoint descriptions
   - Request/response examples
   - Authentication documentation
   - Error codes and handling
   - Rate limiting information
   - OpenAPI/Swagger specs

3. README Files:
   - Project overview and purpose
   - Installation instructions
   - Quick start guide
   - Usage examples
   - Configuration options
   - Contributing guidelines
   - License information
   - Badges and status indicators

4. Architecture Documentation:
   - System architecture diagrams
   - Component relationships
   - Data flow diagrams
   - Deployment architecture
   - Technology stack overview
   - Design decisions (ADRs)

5. User Guides:
   - Feature documentation
   - Step-by-step tutorials
   - Use case examples
   - Troubleshooting guides
   - FAQ sections
   - Screenshots and visuals

6. Developer Guides:
   - Development setup
   - Code organization
   - Coding standards
   - Testing guidelines
   - Deployment procedures
   - CI/CD pipeline documentation

7. Changelog:
   - Version history
   - Breaking changes
   - New features
   - Bug fixes
   - Deprecations
   - Migration guides

8. Comment Best Practices:
   - Explain "why" not "what"
   - Avoid obvious comments
   - Keep comments up-to-date
   - Use TODO/FIXME/HACK markers
   - Document complex algorithms
   - Note performance considerations

Documentation principles:
- Write for your audience (users vs developers)
- Keep documentation close to code
- Use clear, concise language
- Provide practical examples
- Keep documentation updated
- Use consistent formatting
- Include diagrams when helpful
- Make documentation searchable
- Version documentation with code
- Test documentation examples"""

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
            if context.get("code"):
                prompt += f"- Code:\n```{context.get('language', '')}\n{context['code']}\n```\n"
            if context.get("doc_type"):
                prompt += f"- Documentation Type: {context['doc_type']}\n"
            if context.get("audience"):
                prompt += f"- Audience: {context['audience']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        documentation = []
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        
        for language, code in code_blocks:
            documentation.append({"language": language, "content": code.strip()})
        
        return {"response": text_content, "documentation": documentation}


if __name__ == "__main__":
    agent = DocumentationAgent()
    result = agent.execute("Generate comprehensive documentation for this function", 
                          {"code": "def calculate_total(items, tax_rate=0.08):\n    return sum(item['price'] for item in items) * (1 + tax_rate)", 
                           "language": "python", "doc_type": "docstring"})
