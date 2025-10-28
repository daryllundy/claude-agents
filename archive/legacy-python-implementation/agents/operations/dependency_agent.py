"""
Dependency Management Agent - Specialized agent for dependency management
"""

from anthropic import Anthropic
import os

class DependencyAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a dependency management specialist with expertise in:

1. Dependency Analysis:
   - Dependency tree visualization
   - Circular dependency detection
   - Unused dependency identification
   - Transitive dependencies
   - Version conflicts
   - Dependency weight/size

2. Version Management:
   - Semantic versioning (SemVer)
   - Version pinning strategies
   - Range specifications
   - Lock files (package-lock.json, Pipfile.lock)
   - Version compatibility
   - Breaking change detection

3. Package Managers:
   - npm, yarn, pnpm (JavaScript)
   - pip, poetry, conda (Python)
   - Maven, Gradle (Java)
   - Cargo (Rust)
   - Go modules
   - Bundler (Ruby)

4. Security:
   - Vulnerability scanning
   - CVE tracking
   - Security advisories
   - Automated security updates
   - License compliance
   - Supply chain security

5. Updates:
   - Update strategies
   - Breaking change handling
   - Changelog review
   - Testing after updates
   - Automated update tools (Dependabot, Renovate)
   - Staged rollout

6. Monorepo Management:
   - Workspace management
   - Shared dependencies
   - Version synchronization
   - Build optimization
   - Dependency hoisting
   - Tools (Nx, Turborepo, Lerna)

7. Optimization:
   - Bundle size reduction
   - Tree shaking
   - Code splitting
   - Lazy loading
   - Dependency alternatives
   - Peer dependencies

8. License Compliance:
   - License types (MIT, Apache, GPL)
   - License compatibility
   - Commercial use restrictions
   - License auditing
   - Attribution requirements

Best practices:
- Keep dependencies up to date
- Use lock files
- Audit regularly for vulnerabilities
- Review changelogs before updating
- Test after dependency updates
- Minimize dependency count
- Prefer well-maintained packages
- Check license compatibility
- Use automated update tools
- Document dependency decisions"""

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
            if context.get("package_manager"):
                prompt += f"- Package Manager: {context['package_manager']}\n"
            if context.get("dependencies"):
                prompt += f"- Current Dependencies:\n{context['dependencies']}\n"
            if context.get("language"):
                prompt += f"- Language: {context['language']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        configs = []
        
        for language, code in code_blocks:
            configs.append({"language": language, "content": code.strip()})
        
        recommendations = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['update', 'upgrade', 'remove', 'replace', 'add']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 20:
                    recommendations.append(clean)
        
        return {"response": text_content, "configs": configs, "recommendations": recommendations[:15]}


if __name__ == "__main__":
    agent = DependencyAgent()
    result = agent.execute("Audit dependencies and suggest updates", 
                          {"package_manager": "npm", "language": "JavaScript"})
