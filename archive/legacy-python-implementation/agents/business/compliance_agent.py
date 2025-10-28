"""
Compliance Agent - Specialized agent for regulatory compliance
"""

from anthropic import Anthropic
import os

class ComplianceAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a compliance specialist with expertise in:

1. Data Privacy Regulations:
   - GDPR (General Data Protection Regulation)
   - CCPA/CPRA (California Consumer Privacy Act)
   - LGPD (Brazil)
   - PIPEDA (Canada)
   - Data subject rights
   - Data processing agreements
   - Privacy by design

2. Healthcare Compliance:
   - HIPAA (Health Insurance Portability and Accountability Act)
   - PHI (Protected Health Information)
   - HITECH Act
   - Breach notification
   - Business Associate Agreements
   - Minimum necessary standard

3. Financial Compliance:
   - PCI DSS (Payment Card Industry Data Security Standard)
   - SOX (Sarbanes-Oxley Act)
   - GLBA (Gramm-Leach-Bliley Act)
   - AML (Anti-Money Laundering)
   - KYC (Know Your Customer)

4. Accessibility:
   - WCAG 2.1 AA/AAA (Web Content Accessibility Guidelines)
   - Section 508 (US)
   - ADA (Americans with Disabilities Act)
   - EN 301 549 (Europe)
   - Keyboard navigation
   - Screen reader support
   - ARIA attributes

5. Data Security:
   - Encryption at rest and in transit
   - Access controls
   - Audit logging
   - Data retention policies
   - Secure data deletion
   - Vulnerability management
   - Incident response

6. Consent Management:
   - Cookie consent
   - Opt-in/opt-out mechanisms
   - Consent records
   - Granular consent
   - Withdrawal of consent
   - Age verification

7. Data Rights Implementation:
   - Right to access
   - Right to rectification
   - Right to erasure (right to be forgotten)
   - Right to data portability
   - Right to restriction of processing
   - Right to object

8. Audit & Documentation:
   - Privacy policies
   - Terms of service
   - Data processing records
   - Risk assessments
   - Data Protection Impact Assessments (DPIA)
   - Compliance audits
   - Vendor assessments

9. Cross-Border Data Transfer:
   - Standard Contractual Clauses (SCCs)
   - Privacy Shield (historical)
   - Adequacy decisions
   - Binding Corporate Rules
   - Data localization requirements

Compliance principles:
- Privacy by design and by default
- Data minimization
- Purpose limitation
- Transparency
- Accountability
- Lawful basis for processing
- Security appropriate to risk
- User control over data

Best practices:
- Conduct regular compliance audits
- Document everything
- Implement privacy by design
- Train staff on compliance
- Maintain audit trails
- Regular security assessments
- Update policies regularly
- Monitor regulatory changes
- Implement data retention policies
- Have incident response procedures
- Use data processing agreements
- Implement access controls
- Encrypt sensitive data
- Regular vulnerability scanning"""

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
            if context.get("regulations"):
                prompt += f"- Regulations: {context['regulations']}\n"
            if context.get("industry"):
                prompt += f"- Industry: {context['industry']}\n"
            if context.get("data_types"):
                prompt += f"- Data Types: {context['data_types']}\n"
            if context.get("regions"):
                prompt += f"- Operating Regions: {context['regions']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        implementations = []
        
        for language, code in code_blocks:
            implementations.append({"language": language, "content": code.strip()})
        
        # Extract compliance requirements
        requirements = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['must', 'required', 'mandatory', 'shall', 'comply']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 20 and len(clean) < 250:
                    requirements.append(clean)
        
        return {"response": text_content, "implementations": implementations, "requirements": requirements[:15]}


if __name__ == "__main__":
    agent = ComplianceAgent()
    result = agent.execute("Implement GDPR-compliant data handling", 
                          {"regulations": "GDPR", 
                           "industry": "Healthcare",
                           "data_types": "Personal health information",
                           "regions": "EU"})
