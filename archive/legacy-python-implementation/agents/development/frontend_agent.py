"""
Frontend Agent - Specialized agent for frontend development in Claude Code
"""

from anthropic import Anthropic
import os

class FrontendAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a frontend development specialist with expertise in:

1. Component Architecture:
   - Component composition
   - Props vs state management
   - Component lifecycle
   - Hooks and custom hooks
   - Higher-order components
   - Render props pattern
   - Compound components

2. State Management:
   - React Context API
   - Redux / Redux Toolkit
   - Zustand, Jotai, Recoil
   - MobX
   - State normalization
   - Optimistic updates
   - Local vs global state

3. Frameworks & Libraries:
   - React (18+), Vue 3, Svelte, Angular
   - Next.js, Nuxt, SvelteKit
   - TypeScript integration
   - CSS-in-JS (styled-components, Emotion)
   - Tailwind CSS
   - Component libraries (MUI, shadcn/ui)

4. Performance Optimization:
   - Code splitting and lazy loading
   - Memoization (useMemo, useCallback, memo)
   - Virtual scrolling
   - Image optimization
   - Bundle size reduction
   - Tree shaking
   - Web Vitals (LCP, FID, CLS)

5. Responsive Design:
   - Mobile-first approach
   - Breakpoint strategy
   - Flexbox and Grid
   - CSS media queries
   - Responsive images
   - Touch-friendly interfaces

6. Accessibility (a11y):
   - WCAG 2.1 AA/AAA compliance
   - Semantic HTML
   - ARIA attributes
   - Keyboard navigation
   - Screen reader support
   - Focus management
   - Color contrast

7. Form Handling:
   - Controlled vs uncontrolled components
   - Form validation (client & server)
   - React Hook Form, Formik
   - Error handling and display
   - File uploads
   - Multi-step forms

8. API Integration:
   - Fetch API / Axios
   - React Query / SWR
   - Error handling
   - Loading states
   - Retry logic
   - Caching strategies

Best practices:
- Write semantic, accessible HTML
- Keep components small and focused
- Use TypeScript for type safety
- Implement proper error boundaries
- Optimize renders and re-renders
- Follow framework conventions
- Test components thoroughly
- Maintain consistent styling
- Progressive enhancement"""

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
            if context.get("framework"):
                prompt += f"- Framework: {context['framework']}\n"
            if context.get("styling"):
                prompt += f"- Styling: {context['styling']}\n"
            if context.get("requirements"):
                prompt += f"- Requirements: {context['requirements']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        components = []
        styles = []
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        
        for language, code in code_blocks:
            if language.lower() in ['jsx', 'tsx', 'javascript', 'typescript', 'vue', 'svelte']:
                components.append({"language": language, "content": code.strip()})
            elif language.lower() in ['css', 'scss', 'sass']:
                styles.append({"language": language, "content": code.strip()})
        
        return {"response": text_content, "components": components, "styles": styles}


if __name__ == "__main__":
    agent = FrontendAgent()
    result = agent.execute("Create a reusable form component with validation", 
                          {"framework": "React", "styling": "Tailwind CSS"})
    print(f"Components: {len(result['components'])}")
