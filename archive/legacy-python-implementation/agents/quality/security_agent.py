"""
Security Agent - Specialized agent for security analysis in Claude Code

This agent handles:
- Security vulnerability detection
- Code security review
- Dependency scanning
- Security best practices
- Threat modeling
- Secure coding recommendations
"""

from anthropic import Anthropic
import json
import os
from typing import List, Dict, Optional

class SecurityAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a security specialist agent focused on application security. Your expertise includes:

1. Common Vulnerabilities:
   - OWASP Top 10 (Injection, XSS, CSRF, etc.)
   - SQL Injection and NoSQL Injection
   - Command Injection
   - Path Traversal
   - Insecure Deserialization
   - Authentication and Authorization flaws
   - Sensitive Data Exposure
   - Security Misconfiguration

2. Secure Coding Practices:
   - Input validation and sanitization
   - Output encoding
   - Parameterized queries
   - Secure session management
   - Cryptographic best practices
   - Secrets management
   - Error handling (avoid information leakage)

3. Security Analysis:
   - Static code analysis
   - Dependency vulnerability scanning
   - Authentication flow review
   - Authorization logic verification
   - Data flow analysis
   - Attack surface assessment

4. Language-Specific Security:
   - Python: pickle risks, eval dangers, SQL injection
   - JavaScript: XSS, prototype pollution, npm vulnerabilities
   - Java: deserialization, XXE, SSRF
   - Go: race conditions, unsafe pointer operations
   - PHP: file inclusion, command injection

5. Infrastructure Security:
   - Container security
   - Cloud security posture
   - Network security
   - Secrets management (never hardcode)
   - Least privilege access
   - Security headers

6. Compliance & Standards:
   - OWASP guidelines
   - CWE (Common Weakness Enumeration)
   - CVE awareness
   - Security frameworks (NIST, ISO 27001)

When reviewing code for security:
- Identify specific vulnerabilities with CWE/CVE references
- Explain the security impact and exploit scenarios
- Provide secure code alternatives
- Prioritize findings by severity (Critical, High, Medium, Low)
- Consider both direct vulnerabilities and design flaws
- Check for security anti-patterns
- Verify proper error handling
- Review authentication and authorization
- Check for sensitive data exposure
- Validate input handling

Always provide:
1. Clear vulnerability description
2. Severity level and CVSS score if applicable
3. Proof of concept or exploit scenario
4. Remediation steps with code examples
5. Prevention strategies"""

    def execute(self, task: str, context: dict = None) -> dict:
        """
        Execute a security-related task
        
        Args:
            task: The security task to perform
            context: Code to analyze, dependencies, configuration, etc.
        
        Returns:
            dict with 'response', 'vulnerabilities', and 'recommendations'
        """
        messages = [
            {
                "role": "user",
                "content": self._build_prompt(task, context)
            }
        ]
        
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
            
            if context.get("code"):
                prompt += f"Code to Analyze:\n```{context.get('language', '')}\n{context['code']}\n```\n\n"
            
            if context.get("language"):
                prompt += f"- Language: {context['language']}\n"
            
            if context.get("framework"):
                prompt += f"- Framework: {context['framework']}\n"
            
            if context.get("dependencies"):
                prompt += f"- Dependencies:\n{context['dependencies']}\n"
            
            if context.get("config"):
                prompt += f"- Configuration:\n{context['config']}\n"
            
            if context.get("environment"):
                prompt += f"- Environment: {context['environment']}\n"
            
            if context.get("focus_areas"):
                prompt += f"- Focus Areas: {', '.join(context['focus_areas'])}\n"
            
            prompt += "\n"
        
        prompt += "Provide a thorough security analysis with specific, actionable recommendations."
        return prompt
    
    def _parse_response(self, response) -> dict:
        """Parse the Claude response and extract vulnerabilities and recommendations"""
        text_content = ""
        
        for block in response.content:
            if block.type == "text":
                text_content += block.text
        
        # Extract vulnerabilities (sections with severity indicators)
        vulnerabilities = self._extract_vulnerabilities(text_content)
        
        # Extract recommendations
        recommendations = self._extract_recommendations(text_content)
        
        # Extract secure code examples
        import re
        code_pattern = r"```(\w+)\n(.*?)```"
        secure_examples = []
        code_blocks = re.findall(code_pattern, text_content, re.DOTALL)
        
        for language, code in code_blocks:
            if any(term in code.lower() for term in ['secure', 'fixed', 'safe', 'correct']):
                secure_examples.append({
                    "language": language,
                    "code": code.strip()
                })
        
        return {
            "response": text_content,
            "vulnerabilities": vulnerabilities,
            "recommendations": recommendations,
            "secure_examples": secure_examples
        }
    
    def _extract_vulnerabilities(self, text: str) -> List[Dict]:
        """Extract vulnerability information from text"""
        vulnerabilities = []
        
        # Common severity indicators
        severity_patterns = [
            (r"(?:^|\n).*?(?:CRITICAL|Critical|🔴).*?(?:\n|$)", "CRITICAL"),
            (r"(?:^|\n).*?(?:HIGH|High|🟠).*?(?:\n|$)", "HIGH"),
            (r"(?:^|\n).*?(?:MEDIUM|Medium|🟡).*?(?:\n|$)", "MEDIUM"),
            (r"(?:^|\n).*?(?:LOW|Low|🟢).*?(?:\n|$)", "LOW"),
        ]
        
        lines = text.split('\n')
        current_vuln = None
        
        for i, line in enumerate(lines):
            # Check for vulnerability markers
            for pattern, severity in severity_patterns:
                import re
                if re.search(pattern, line, re.IGNORECASE):
                    if current_vuln:
                        vulnerabilities.append(current_vuln)
                    
                    current_vuln = {
                        "severity": severity,
                        "title": line.strip(),
                        "description": "",
                        "line_number": i + 1
                    }
                    break
            
            # Collect description for current vulnerability
            if current_vuln and i > current_vuln["line_number"]:
                if line.strip() and not any(s in line.upper() for s in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]):
                    current_vuln["description"] += line + "\n"
        
        if current_vuln:
            vulnerabilities.append(current_vuln)
        
        # Extract CWE/CVE references
        cwe_cve_pattern = r"(CWE-\d+|CVE-\d{4}-\d+)"
        for vuln in vulnerabilities:
            import re
            matches = re.findall(cwe_cve_pattern, vuln["title"] + vuln["description"])
            if matches:
                vuln["references"] = matches
        
        return vulnerabilities[:20]  # Return top 20 vulnerabilities
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract security recommendations from text"""
        recommendations = []
        lines = text.split('\n')
        
        for line in lines:
            # Look for recommendation markers
            if any(marker in line.lower() for marker in [
                'recommend', 'should', 'must', 'always', 'never',
                'best practice', 'ensure', 'use', 'avoid', 'implement'
            ]):
                clean_line = line.strip().lstrip('•-*123456789. ')
                if len(clean_line) > 20 and clean_line not in recommendations:
                    recommendations.append(clean_line)
        
        return recommendations[:15]  # Top 15 recommendations
    
    def analyze_code(self, code: str, language: str, framework: str = None) -> dict:
        """Perform comprehensive security analysis on code"""
        task = "Perform a comprehensive security analysis of this code"
        context = {
            "code": code,
            "language": language,
            "framework": framework,
            "focus_areas": [
                "injection vulnerabilities",
                "authentication/authorization",
                "sensitive data handling",
                "input validation",
                "error handling"
            ]
        }
        return self.execute(task, context)
    
    def scan_dependencies(self, dependencies: str, language: str) -> dict:
        """Scan dependencies for known vulnerabilities"""
        task = "Scan these dependencies for known security vulnerabilities"
        context = {
            "dependencies": dependencies,
            "language": language
        }
        return self.execute(task, context)
    
    def review_authentication(self, code: str, language: str) -> dict:
        """Review authentication implementation"""
        task = "Review the authentication implementation for security issues"
        context = {
            "code": code,
            "language": language,
            "focus_areas": [
                "password storage",
                "session management",
                "token handling",
                "multi-factor authentication",
                "brute force protection"
            ]
        }
        return self.execute(task, context)
    
    def check_api_security(self, code: str, language: str) -> dict:
        """Review API endpoints for security issues"""
        task = "Review API security including authentication, rate limiting, and input validation"
        context = {
            "code": code,
            "language": language,
            "focus_areas": [
                "authentication",
                "authorization",
                "rate limiting",
                "input validation",
                "CORS configuration"
            ]
        }
        return self.execute(task, context)


# Example usage
if __name__ == "__main__":
    agent = SecurityAgent()
    
    # Example 1: Analyze vulnerable code
    vulnerable_code = """
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/user/<user_id>')
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    return str(user)

@app.route('/search')
def search():
    query = request.args.get('q')
    # Vulnerable to XSS
    return f"<h1>Results for: {query}</h1>"
"""
    
    result = agent.analyze_code(
        code=vulnerable_code,
        language="python",
        framework="Flask"
    )
    
    print("Security Analysis Results:")
    print(f"Vulnerabilities found: {len(result['vulnerabilities'])}")
    for vuln in result['vulnerabilities'][:3]:
        print(f"\n{vuln['severity']}: {vuln['title']}")
    
    print(f"\nRecommendations: {len(result['recommendations'])}")
    for rec in result['recommendations'][:5]:
        print(f"  - {rec}")
    
    # Example 2: Dependency scanning
    deps = """
requests==2.25.0
flask==1.1.1
pyyaml==5.3.1
"""
    
    dep_result = agent.scan_dependencies(deps, "python")
    print("\n" + "="*50)
    print("Dependency Scan:")
    print(dep_result["response"][:400] + "...")
