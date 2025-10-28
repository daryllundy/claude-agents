"""
Test Suite Agent - Specialized agent for testing in Claude Code

This agent handles all testing-related tasks including:
- Unit test generation
- Integration test design
- Test coverage analysis
- Test data generation
- Testing framework setup
"""

from anthropic import Anthropic
import json
import os
from typing import List, Dict, Optional

class TestSuiteAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a testing specialist agent focused on creating comprehensive test suites. Your expertise includes:

1. Test Design:
   - Unit tests with high coverage
   - Integration tests for component interaction
   - End-to-end tests for user workflows
   - Performance and load tests
   - Security tests

2. Testing Best Practices:
   - Arrange-Act-Assert (AAA) pattern
   - Test isolation and independence
   - Meaningful test names
   - Edge case coverage
   - Mock and stub usage
   - Test data builders/factories

3. Framework Expertise:
   - Python: pytest, unittest, hypothesis
   - JavaScript/TypeScript: Jest, Vitest, Mocha, Cypress
   - Java: JUnit, TestNG, Mockito
   - Go: testing package, testify
   - Ruby: RSpec, Minitest

4. Coverage Analysis:
   - Identifying untested code paths
   - Recommending critical tests
   - Branch and edge case coverage

5. Test Organization:
   - Proper file structure
   - Test categorization (unit/integration/e2e)
   - Fixtures and test utilities
   - Parameterized tests

When generating tests:
- Write clear, maintainable test code
- Include both positive and negative test cases
- Test edge cases and error conditions
- Use descriptive test names that explain what is being tested
- Keep tests focused and atomic
- Avoid test interdependencies
- Include setup and teardown when needed
- Add comments for complex test scenarios"""

    def execute(self, task: str, context: dict = None) -> dict:
        """
        Execute a testing-related task
        
        Args:
            task: The testing task to perform
            context: Code to test, language, framework, etc.
        
        Returns:
            dict with 'response', 'tests', and 'recommendations'
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
            
            if context.get("code"):
                prompt += f"Code to Test:\n```{context.get('language', '')}\n{context['code']}\n```\n\n"
            
            if context.get("language"):
                prompt += f"- Language: {context['language']}\n"
            
            if context.get("framework"):
                prompt += f"- Testing Framework: {context['framework']}\n"
            else:
                prompt += "- Use the most popular testing framework for this language\n"
            
            if context.get("test_type"):
                prompt += f"- Test Type: {context['test_type']}\n"
            
            if context.get("coverage_gaps"):
                prompt += f"- Coverage Gaps: {context['coverage_gaps']}\n"
            
            if context.get("existing_tests"):
                prompt += f"- Existing Tests: {context['existing_tests']}\n"
            
            prompt += "\n"
        
        prompt += "Generate comprehensive tests with clear assertions and good coverage."
        return prompt
    
    def _parse_response(self, response) -> dict:
        """Parse the Claude response and extract test code and recommendations"""
        text_content = ""
        test_files = []
        recommendations = []
        
        for block in response.content:
            if block.type == "text":
                text_content += block.text
        
        # Extract code blocks
        import re
        code_pattern = r"```(\w+)\n(.*?)```"
        code_blocks = re.findall(code_pattern, text_content, re.DOTALL)
        
        for language, code in code_blocks:
            # Identify test files by common patterns
            if any(keyword in code.lower() for keyword in ['test_', 'test(', 'it(', 'describe(', 'assert', '@test']):
                test_files.append({
                    "language": language,
                    "content": code.strip()
                })
        
        # Extract recommendations (lines starting with common recommendation markers)
        lines = text_content.split('\n')
        for line in lines:
            if any(marker in line.lower() for marker in ['recommend', 'should', 'consider', 'important', 'note:']):
                if len(line.strip()) > 10:
                    recommendations.append(line.strip())
        
        return {
            "response": text_content,
            "tests": test_files,
            "recommendations": recommendations[:10]  # Top 10 recommendations
        }
    
    def analyze_coverage(self, code: str, existing_tests: str, language: str) -> dict:
        """Analyze test coverage and suggest missing tests"""
        task = "Analyze the existing tests and identify coverage gaps. Suggest additional test cases needed."
        context = {
            "code": code,
            "existing_tests": existing_tests,
            "language": language
        }
        return self.execute(task, context)
    
    def generate_test_data(self, schema: dict, count: int = 10) -> dict:
        """Generate realistic test data based on schema"""
        task = f"Generate {count} realistic test data samples based on the provided schema."
        context = {
            "code": json.dumps(schema, indent=2),
            "language": "json"
        }
        return self.execute(task, context)


# Example usage
if __name__ == "__main__":
    agent = TestSuiteAgent()
    
    # Example 1: Generate unit tests for a function
    sample_code = """
def calculate_discount(price, discount_percent, user_tier):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    
    if user_tier == "premium":
        discount_percent += 5
    elif user_tier == "vip":
        discount_percent += 10
    
    discount_percent = min(discount_percent, 100)
    return price * (1 - discount_percent / 100)
"""
    
    result = agent.execute(
        task="Generate comprehensive unit tests for this discount calculation function",
        context={
            "code": sample_code,
            "language": "python",
            "framework": "pytest",
            "test_type": "unit"
        }
    )
    
    print("Generated Tests:", len(result["tests"]))
    print("\nRecommendations:")
    for rec in result["recommendations"]:
        print(f"  - {rec}")
    
    # Example 2: Analyze coverage
    existing_tests = """
def test_basic_discount():
    assert calculate_discount(100, 10, "standard") == 90
"""
    
    coverage_result = agent.analyze_coverage(
        code=sample_code,
        existing_tests=existing_tests,
        language="python"
    )
    
    print("\n" + "="*50)
    print("Coverage Analysis:")
    print(coverage_result["response"][:500] + "...")
