"""
Git Agent - Specialized agent for Git operations and workflows
"""

from anthropic import Anthropic
import os

class GitAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a Git specialist with expertise in:

1. Commit Messages:
   - Conventional Commits format
   - Clear, descriptive messages
   - Semantic commit types (feat, fix, docs, etc.)
   - Breaking change notation
   - Issue/ticket references
   - Multi-line descriptions

2. Branching Strategies:
   - Git Flow
   - GitHub Flow
   - GitLab Flow
   - Trunk-based development
   - Feature branches
   - Release branches
   - Hotfix workflows

3. Merge Strategies:
   - Merge commits
   - Squash and merge
   - Rebase and merge
   - Fast-forward merges
   - Conflict resolution
   - Cherry-picking

4. Git Operations:
   - Interactive rebase
   - Stashing changes
   - Bisect for debugging
   - Reflog recovery
   - Submodules
   - Worktrees
   - Hooks (pre-commit, pre-push)

5. Repository Management:
   - .gitignore patterns
   - .gitattributes
   - Large file handling (LFS)
   - Monorepo strategies
   - Repository cleanup
   - History rewriting

6. Collaboration:
   - Pull request templates
   - Code review guidelines
   - Protected branches
   - CODEOWNERS
   - Issue templates
   - PR descriptions

7. Git Workflows:
   - Feature development
   - Bug fixing
   - Release management
   - Hotfix deployment
   - Version tagging
   - Changelog generation

8. Best Practices:
   - Atomic commits
   - Meaningful commit messages
   - Regular commits
   - Branch naming conventions
   - Keeping branches up to date
   - Cleaning up branches
   - Tag releases

Commit message format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build

Best practices:
- Commit early and often
- Write clear commit messages
- Use branches for features
- Review code before merging
- Keep commits atomic
- Rebase to clean history
- Tag releases semantically
- Use hooks for automation
- Document workflows
- Protect main branch"""

    def execute(self, task: str, context: dict = None) -> dict:
        messages = [{"role": "user", "content": self._build_prompt(task, context)}]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=self.system_prompt,
            messages=messages
        )
        
        return self._parse_response(response)
    
    def _build_prompt(self, task: str, context: dict = None) -> str:
        prompt = f"Task: {task}\n\n"
        
        if context:
            prompt += "Context:\n"
            if context.get("changes"):
                prompt += f"- Changes Made:\n{context['changes']}\n"
            if context.get("branch_strategy"):
                prompt += f"- Branch Strategy: {context['branch_strategy']}\n"
            if context.get("issue_number"):
                prompt += f"- Issue: #{context['issue_number']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        
        # Extract commit messages
        commit_messages = []
        code_blocks = re.findall(r"```(?:bash|shell|git)?\n(.*?)```", text_content, re.DOTALL)
        for block in code_blocks:
            if 'git commit' in block:
                commit_messages.append(block.strip())
        
        # Extract git commands
        commands = []
        git_pattern = r'(?:^|\n)(?:\$|>)?\s*(git [^\n]+)'
        git_commands = re.findall(git_pattern, text_content, re.MULTILINE)
        commands.extend(git_commands)
        
        return {"response": text_content, "commit_messages": commit_messages, "commands": commands}


if __name__ == "__main__":
    agent = GitAgent()
    result = agent.execute("Generate a commit message for adding user authentication", 
                          {"changes": "Added JWT authentication, login/logout endpoints, password hashing", 
                           "issue_number": "123"})
