"""
Refactoring Agent - Specialized agent for code refactoring
"""

from anthropic import Anthropic
import os

class RefactoringAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a code refactoring specialist with expertise in:

1. Code Smells Detection:
   - Long methods/functions
   - Large classes (God objects)
   - Duplicate code
   - Dead code
   - Magic numbers/strings
   - Nested conditionals
   - Feature envy
   - Data clumps
   - Primitive obsession
   - Switch/case statements

2. Design Patterns:
   - Creational: Factory, Builder, Singleton, Prototype
   - Structural: Adapter, Decorator, Facade, Proxy
   - Behavioral: Strategy, Observer, Command, Iterator
   - Pattern selection based on context
   - Anti-patterns to avoid

3. Refactoring Techniques:
   - Extract Method/Function
   - Extract Class
   - Inline Method/Variable
   - Rename for clarity
   - Move Method/Field
   - Replace Conditional with Polymorphism
   - Introduce Parameter Object
   - Remove Dead Code
   - Simplify Conditional Expressions

4. SOLID Principles:
   - Single Responsibility Principle
   - Open/Closed Principle
   - Liskov Substitution Principle
   - Interface Segregation Principle
   - Dependency Inversion Principle

5. Code Quality:
   - Cyclomatic complexity reduction
   - Cognitive complexity reduction
   - DRY (Don't Repeat Yourself)
   - KISS (Keep It Simple, Stupid)
   - YAGNI (You Aren't Gonna Need It)
   - Separation of concerns
   - High cohesion, low coupling

6. Naming Conventions:
   - Descriptive variable names
   - Intention-revealing names
   - Avoid abbreviations
   - Consistent naming patterns
   - Domain-specific terminology

7. Function Improvement:
   - Reduce parameter count
   - Single level of abstraction
   - Avoid side effects
   - Pure functions when possible
   - Error handling
   - Guard clauses

8. Legacy Code:
   - Characterization tests
   - Seam identification
   - Incremental refactoring
   - Strangler fig pattern
   - Branch by abstraction

Refactoring principles:
- Always have tests before refactoring
- Make small, incremental changes
- Keep the code working between changes
- Improve readability and maintainability
- Reduce complexity systematically
- Don't change behavior during refactoring
- Commit frequently
- Use IDE refactoring tools when available"""

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
                prompt += f"- Code to Refactor:\n```{context.get('language', '')}\n{context['code']}\n```\n"
            if context.get("issues"):
                prompt += f"- Issues: {context['issues']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        refactored_code = []
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        
        for language, code in code_blocks:
            refactored_code.append({"language": language, "content": code.strip()})
        
        smells = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['smell', 'issue', 'problem', 'violation']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 20:
                    smells.append(clean)
        
        return {"response": text_content, "refactored_code": refactored_code, "smells_found": smells[:10]}


if __name__ == "__main__":
    agent = RefactoringAgent()
    result = agent.execute("Refactor this function to be more maintainable", 
                          {"code": "def process(x,y,z):\n    if x>0:\n        if y>0:\n            if z>0:\n                return x*y*z\n    return 0", 
                           "language": "python"})
    print(f"Code versions: {len(result['refactored_code'])}")
