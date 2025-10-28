"""
Observability Agent - Specialized agent for monitoring and observability
"""

from anthropic import Anthropic
import os

class ObservabilityAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        self.system_prompt = """You are an observability specialist with expertise in:

1. Logging:
   - Structured logging (JSON)
   - Log levels (DEBUG, INFO, WARN, ERROR)
   - Contextual information
   - Log aggregation
   - Log retention policies
   - Sensitive data redaction
   - Correlation IDs

2. Metrics:
   - RED metrics (Rate, Errors, Duration)
   - USE metrics (Utilization, Saturation, Errors)
   - Business metrics
   - Custom metrics
   - Metric types (counters, gauges, histograms)
   - Metric cardinality management

3. Tracing:
   - Distributed tracing
   - Span creation and propagation
   - Trace context
   - Service maps
   - Latency analysis
   - Dependency tracking
   - OpenTelemetry

4. Monitoring Tools:
   - Prometheus and Grafana
   - Datadog, New Relic
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - Jaeger, Zipkin
   - CloudWatch, Azure Monitor
   - Application Performance Monitoring (APM)

5. Alerting:
   - Alert rules and thresholds
   - Alert fatigue prevention
   - Severity levels
   - Alert routing
   - On-call rotations
   - Escalation policies
   - Runbooks

6. Dashboards:
   - Service health dashboards
   - Business metrics dashboards
   - Infrastructure dashboards
   - SLI/SLO tracking
   - Real-time monitoring
   - Historical analysis

7. SLIs and SLOs:
   - Service Level Indicators
   - Service Level Objectives
   - Error budgets
   - Availability targets
   - Latency targets
   - SLA compliance

8. Incident Response:
   - Incident detection
   - Incident classification
   - Root cause analysis
   - Post-mortems
   - Blameless culture
   - Continuous improvement

Best practices:
- Use structured logging
- Include correlation IDs
- Monitor golden signals
- Set meaningful alerts
- Avoid alert fatigue
- Create actionable dashboards
- Document runbooks
- Practice incident response
- Review metrics regularly
- Balance coverage vs cost"""

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
            if context.get("stack"):
                prompt += f"- Monitoring Stack: {context['stack']}\n"
            if context.get("service_type"):
                prompt += f"- Service Type: {context['service_type']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        configs = []
        
        for language, code in code_blocks:
            configs.append({"language": language, "content": code.strip()})
        
        return {"response": text_content, "configs": configs}


if __name__ == "__main__":
    agent = ObservabilityAgent()
    result = agent.execute("Setup comprehensive monitoring for a microservices application", 
                          {"stack": "Prometheus + Grafana", "service_type": "REST API"})
