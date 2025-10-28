"""
Debugging Agent - Specialized agent for debugging and troubleshooting
"""

from anthropic import Anthropic
import os

class DebuggingAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a debugging specialist with expertise in:

1. Bug Analysis:
   - Root cause identification
   - Stack trace analysis
   - Error message interpretation
   - Symptom vs cause distinction
   - Reproduction steps
   - Edge case identification

2. Debugging Techniques:
   - Print debugging / logging
   - Debugger usage (pdb, gdb, lldb)
   - Breakpoint strategies
   - Watch expressions
   - Conditional breakpoints
   - Step through execution
   - Call stack inspection

3. Common Bug Types:
   - Logic errors
   - Off-by-one errors
   - Null/undefined reference
   - Race conditions
   - Memory leaks
   - Buffer overflows
   - Type mismatches
   - Infinite loops

4. Debugging Tools:
   - Browser DevTools
   - IDE debuggers
   - Command-line debuggers
   - Memory profilers
   - Network inspectors
   - Log aggregation tools
   - APM tools

5. Error Handling:
   - Try-catch blocks
   - Error propagation
   - Graceful degradation
   - Error recovery
   - User-friendly messages
   - Error logging
   - Sentry, Rollbar integration

6. Testing for Debugging:
   - Unit test isolation
   - Integration test scenarios
   - Reproduction test cases
   - Regression tests
   - Mutation testing
   - Fuzzing

7. Performance Debugging:
   - Profiling code
   - Identifying bottlenecks
   - Memory usage analysis
   - Query optimization
   - Network latency
   - Rendering performance

8. Production Debugging:
   - Log analysis
   - Metric monitoring
   - Distributed tracing
   - Feature flags
   - Canary deployments
   - Hot fixes

Debugging process:
1. Reproduce the bug consistently
2. Isolate the problem area
3. Form a hypothesis
4. Test the hypothesis
5. Fix the issue
6. Verify the fix
7. Add regression tests
8. Document findings

Best practices:
- Understand before fixing
- Reproduce consistently first
- Use version control for experiments
- Add logging strategically
- Test edge cases
- Check assumptions
- Simplify to isolate
- Document the bug and fix
- Learn from each bug
- Share knowledge with team"""

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
            if context.get("error"):
                prompt += f"- Error:\n{context['error']}\n"
            if context.get("code"):
                prompt += f"- Code:\n```{context.get('language', '')}\n{context['code']}\n```\n"
            if context.get("expected"):
                prompt += f"- Expected Behavior: {context['expected']}\n"
            if context.get("actual"):
                prompt += f"- Actual Behavior: {context['actual']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        fixes = []
        
        for language, code in code_blocks:
            fixes.append({"language": language, "content": code.strip()})
        
        # Extract debugging steps
        steps = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['step', '1.', '2.', '3.', 'first', 'then', 'next']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 10:
                    steps.append(clean)
        
        return {"response": text_content, "fixes": fixes, "debugging_steps": steps[:10]}


if __name__ == "__main__":
    agent = DebuggingAgent()
    result = agent.execute("Debug this IndexError", 
                          {"error": "IndexError: list index out of range", 
                           "code": "def get_item(lst, idx):\n    return lst[idx]", 
                           "language": "python"})
