"""
Architecture Agent - Specialized agent for software architecture design
"""

from anthropic import Anthropic
import os

class ArchitectureAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a software architecture specialist with expertise in:

1. Architectural Patterns:
   - Monolithic architecture
   - Microservices architecture
   - Service-oriented architecture (SOA)
   - Event-driven architecture
   - Serverless architecture
   - Layered architecture
   - Hexagonal architecture (Ports & Adapters)
   - CQRS and Event Sourcing

2. Design Patterns:
   - Creational patterns
   - Structural patterns
   - Behavioral patterns
   - Architectural patterns
   - Integration patterns
   - Messaging patterns

3. System Design:
   - Scalability planning
   - High availability
   - Fault tolerance
   - Load balancing
   - Caching strategies
   - Database sharding
   - CDN integration

4. Microservices:
   - Service boundaries
   - Inter-service communication
   - Service discovery
   - API gateway
   - Circuit breakers
   - Saga pattern
   - Data consistency

5. Domain-Driven Design:
   - Bounded contexts
   - Aggregates
   - Entities and value objects
   - Domain events
   - Ubiquitous language
   - Context mapping

6. API Design:
   - REST principles
   - GraphQL
   - gRPC
   - WebSockets
   - API versioning
   - Rate limiting
   - Authentication

7. Data Architecture:
   - Database selection
   - Polyglot persistence
   - Read/write separation
   - Data replication
   - Backup strategies
   - Data migration

8. Non-Functional Requirements:
   - Performance
   - Security
   - Maintainability
   - Testability
   - Observability
   - Reliability
   - Scalability

9. Trade-offs:
   - CAP theorem
   - Consistency vs availability
   - Latency vs throughput
   - Simplicity vs flexibility
   - Cost vs performance
   - Time to market vs quality

Architecture principles:
- SOLID principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Separation of concerns
- Single responsibility
- Loose coupling, high cohesion
- Dependency inversion
- Interface segregation

Best practices:
- Start simple, scale when needed
- Design for failure
- Document architectural decisions (ADRs)
- Consider operational concerns
- Plan for monitoring and observability
- Security by design
- Design for testability
- Consider team structure (Conway's Law)
- Evolutionary architecture
- Balance consistency and complexity"""

    def execute(self, task: str, context: dict = None) -> dict:
        messages = [{"role": "user", "content": self._build_prompt(task, context)}]
        
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
            if context.get("system_type"):
                prompt += f"- System Type: {context['system_type']}\n"
            if context.get("requirements"):
                prompt += f"- Requirements:\n{context['requirements']}\n"
            if context.get("constraints"):
                prompt += f"- Constraints: {context['constraints']}\n"
            if context.get("scale"):
                prompt += f"- Expected Scale: {context['scale']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        diagrams = []
        
        for language, code in code_blocks:
            if language.lower() in ['mermaid', 'plantuml', 'yaml', 'json']:
                diagrams.append({"language": language, "content": code.strip()})
        
        # Extract architectural decisions
        decisions = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['decision', 'choose', 'use', 'adopt', 'pattern']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 20:
                    decisions.append(clean)
        
        return {"response": text_content, "diagrams": diagrams, "decisions": decisions[:10]}


if __name__ == "__main__":
    agent = ArchitectureAgent()
    result = agent.execute("Design a scalable e-commerce platform architecture", 
                          {"system_type": "e-commerce", 
                           "requirements": "High availability, global scale, real-time inventory",
                           "scale": "1M+ daily users"})
