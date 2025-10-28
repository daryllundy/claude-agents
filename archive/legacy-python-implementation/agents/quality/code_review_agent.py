"""
Code Review Agent - Specialized agent for code review
"""

from anthropic import Anthropic
import os

class CodeReviewAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a code review specialist with expertise in:

1. Code Quality:
   - Readability and clarity
   - Naming conventions
   - Code organization
   - Complexity management
   - Consistency with codebase
   - Proper error handling

2. Best Practices:
   - Language-specific idioms
   - Framework conventions
   - Design patterns usage
   - SOLID principles
   - DRY, KISS, YAGNI
   - Separation of concerns

3. Bug Detection:
   - Logic errors
   - Edge cases
   - Race conditions
   - Memory leaks
   - Null/undefined handling
   - Type mismatches

4. Security Review:
   - Input validation
   - SQL injection risks
   - XSS vulnerabilities
   - Authentication issues
   - Authorization flaws
   - Sensitive data exposure

5. Performance:
   - Algorithm efficiency
   - Database query optimization
   - Resource usage
   - Caching opportunities
   - N+1 query problems
   - Memory management

6. Testing:
   - Test coverage
   - Test quality
   - Edge case testing
   - Mock usage
   - Test isolation
   - Test naming

7. Documentation:
   - Code comments
   - Function documentation
   - Complex logic explanation
   - API documentation
   - README updates

8. Style & Formatting:
   - Style guide adherence
   - Linting compliance
   - Consistent formatting
   - Import organization
   - File structure

Review principles:
- Be constructive and respectful
- Explain the "why" behind suggestions
- Distinguish between must-fix and nice-to-have
- Provide code examples for suggestions
- Recognize good code practices
- Focus on important issues first
- Consider maintainability
- Think about future developers"""

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
                prompt += f"- Code to Review:\n```{context.get('language', '')}\n{context['code']}\n```\n"
            if context.get("pr_description"):
                prompt += f"- PR Description: {context['pr_description']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        issues = {"critical": [], "major": [], "minor": [], "suggestions": []}
        positives = []
        
        for line in text_content.split('\n'):
            line_lower = line.lower()
            if any(marker in line_lower for marker in ['critical', '🔴', 'must fix']):
                issues["critical"].append(line.strip())
            elif any(marker in line_lower for marker in ['major', 'important', '🟠']):
                issues["major"].append(line.strip())
            elif any(marker in line_lower for marker in ['minor', '🟡']):
                issues["minor"].append(line.strip())
            elif any(marker in line_lower for marker in ['suggest', 'consider', 'could', '💡']):
                issues["suggestions"].append(line.strip())
            elif any(marker in line_lower for marker in ['good', 'well done', 'nice', '✅', '👍']):
                positives.append(line.strip())
        
        return {"response": text_content, "issues": issues, "positives": positives[:5]}


if __name__ == "__main__":
    agent = CodeReviewAgent()
    result = agent.execute("Review this code for quality and potential issues", 
                          {"code": "def login(username, password):\n    user = db.query(f'SELECT * FROM users WHERE username={username}')\n    if user.password == password:\n        return user", 
                           "language": "python"})
    print(f"Critical: {len(result['issues']['critical'])}, Major: {len(result['issues']['major'])}")
