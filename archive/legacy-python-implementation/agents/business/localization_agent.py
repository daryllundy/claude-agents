"""
Localization/i18n Agent - Specialized agent for internationalization
"""

from anthropic import Anthropic
import os

class LocalizationAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"

        self.system_prompt = """You are a localization and internationalization specialist with expertise in:

1. Internationalization (i18n):
   - String externalization
   - Translation key management
   - Pluralization rules
   - Gender-specific translations
   - Context-aware translations
   - Fallback strategies
   - Dynamic content translation

2. Localization (l10n):
   - Language-specific formatting
   - Cultural adaptations
   - Local conventions
   - Regional variations
   - Content adaptation
   - Image localization
   - Color symbolism

3. Text Formatting:
   - Date and time formats
   - Number formatting
   - Currency formatting
   - Measurement units
   - Address formats
   - Name formats
   - Phone number formats

4. Right-to-Left (RTL) Support:
   - Bidirectional text
   - RTL layout mirroring
   - Mixed directionality
   - Text alignment
   - UI component mirroring
   - Icon orientation

5. Character Encoding:
   - UTF-8 encoding
   - Unicode support
   - Special characters
   - Emoji handling
   - Character limits
   - Font support

6. Translation Management:
   - Translation files (JSON, YAML, PO, XLIFF)
   - Translation keys organization
   - Namespace management
   - Interpolation and variables
   - Plural forms
   - Context and comments for translators

7. Libraries & Frameworks:
   - i18next (JavaScript)
   - react-intl, react-i18next
   - Vue I18n
   - gettext (Python, PHP)
   - ICU Message Format
   - Format.js

8. Content Management:
   - Translation workflows
   - Translation memory
   - Machine translation integration
   - Crowdsourced translation
   - Quality assurance
   - Version control for translations

9. Testing:
   - Pseudo-localization
   - Language switching tests
   - Layout testing for different scripts
   - Text expansion testing
   - RTL testing
   - Locale-specific testing

Best practices:
- Externalize all user-facing strings
- Use meaningful translation keys
- Avoid string concatenation
- Support plural forms properly
- Consider text expansion (30-50%)
- Test with RTL languages
- Use ICU message format
- Provide context for translators
- Support locale fallbacks
- Handle missing translations gracefully
- Use UTF-8 everywhere
- Separate content from code
- Plan for translation workflows
- Test with actual translated content"""

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
            if context.get("languages"):
                prompt += f"- Target Languages: {context['languages']}\n"
            if context.get("framework"):
                prompt += f"- Framework: {context['framework']}\n"
            if context.get("content"):
                prompt += f"- Content to Localize:\n{context['content']}\n"
            prompt += "\n"

        return prompt

    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")

        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        translation_files = []

        for language, code in code_blocks:
            translation_files.append({"language": language, "content": code.strip()})

        return {"response": text_content, "translation_files": translation_files}


if __name__ == "__main__":
    agent = LocalizationAgent()
    result = agent.execute("Setup i18n for a React application",
                          {"languages": "English, Spanish, Arabic, Japanese",
                           "framework": "React with i18next"})
