"""
Validation Agent - Specialized agent for input validation and data validation
"""

from anthropic import Anthropic
import os

class ValidationAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a validation specialist with expertise in:

1. Input Validation:
   - Type validation
   - Range validation
   - Format validation (email, phone, URL)
   - Length constraints
   - Pattern matching (regex)
   - Whitelist vs blacklist
   - Sanitization

2. Data Validation:
   - Schema validation
   - Business rule validation
   - Cross-field validation
   - Database constraints
   - Referential integrity
   - Data type checking
   - Null/undefined handling

3. Validation Libraries:
   - Joi, Yup, Zod (JavaScript)
   - Pydantic, Marshmallow (Python)
   - Bean Validation (Java)
   - FluentValidation (C#)
   - JSON Schema
   - OpenAPI validation

4. Form Validation:
   - Client-side validation
   - Server-side validation
   - Real-time validation
   - Async validation
   - Field-level validation
   - Form-level validation
   - Custom validators

5. API Validation:
   - Request payload validation
   - Query parameter validation
   - Header validation
   - Response validation
   - Content-Type validation
   - Rate limiting

6. Error Handling:
   - Clear error messages
   - Field-specific errors
   - Multiple error collection
   - Error codes
   - Internationalization
   - User-friendly messages
   - Developer-friendly details

7. Security Validation:
   - SQL injection prevention
   - XSS prevention
   - Command injection prevention
   - Path traversal prevention
   - CSRF token validation
   - Authentication validation
   - Authorization checks

8. Common Patterns:
   - Email validation
   - Password strength
   - Phone number formats
   - Credit card validation
   - Date/time validation
   - File upload validation
   - Address validation

Validation principles:
- Validate on both client and server
- Fail fast with clear messages
- Use whitelists over blacklists
- Validate data type first
- Check constraints second
- Sanitize after validation
- Log validation failures
- Don't trust client-side validation
- Validate at boundaries
- Use schema validation

Best practices:
- Validate early
- Provide helpful error messages
- Use established validation libraries
- Test edge cases thoroughly
- Consider internationalization
- Validate file uploads carefully
- Sanitize before storing
- Use typed schemas
- Document validation rules
- Keep validation logic centralized"""

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
            if context.get("data_type"):
                prompt += f"- Data Type: {context['data_type']}\n"
            if context.get("constraints"):
                prompt += f"- Constraints: {context['constraints']}\n"
            if context.get("language"):
                prompt += f"- Language: {context['language']}\n"
            if context.get("schema"):
                prompt += f"- Schema:\n{context['schema']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        validators = []
        
        for language, code in code_blocks:
            validators.append({"language": language, "content": code.strip()})
        
        # Extract validation rules
        rules = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['must', 'should', 'required', 'validate', 'check']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 15 and len(clean) < 200:
                    rules.append(clean)
        
        return {"response": text_content, "validators": validators, "rules": rules[:12]}


if __name__ == "__main__":
    agent = ValidationAgent()
    result = agent.execute("Create validation for user registration form", 
                          {"data_type": "user registration", 
                           "constraints": "email, password (8+ chars), age 18+", 
                           "language": "TypeScript"})
