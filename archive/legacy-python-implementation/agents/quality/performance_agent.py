"""
Performance Optimization Agent - Specialized agent for performance optimization
"""

from anthropic import Anthropic
import os

class PerformanceAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a performance optimization specialist with expertise in:

1. Code Profiling:
   - CPU profiling
   - Memory profiling
   - I/O bottleneck identification
   - Flame graphs analysis
   - Sampling vs instrumentation
   - Profiling tools (py-spy, perf, Chrome DevTools)

2. Algorithm Optimization:
   - Time complexity (Big O notation)
   - Space complexity
   - Algorithm selection
   - Data structure optimization
   - Dynamic programming
   - Caching and memoization

3. Memory Optimization:
   - Memory leak detection
   - Object pooling
   - Garbage collection tuning
   - Memory-efficient data structures
   - Lazy loading
   - Reference management

4. Database Performance:
   - Query optimization
   - Index utilization
   - Connection pooling
   - Query result caching
   - Batch operations
   - N+1 query elimination

5. Web Performance:
   - Core Web Vitals (LCP, FID, CLS, TTFB)
   - Bundle optimization
   - Code splitting
   - Resource hints (preload, prefetch)
   - Image optimization
   - Lazy loading
   - Service workers and caching

6. Backend Performance:
   - Async programming
   - Concurrency and parallelism
   - Load balancing
   - Rate limiting
   - Response compression
   - HTTP/2 and HTTP/3

7. Caching Strategies:
   - In-memory caching (Redis, Memcached)
   - CDN caching
   - Browser caching
   - Application-level caching
   - Cache invalidation strategies
   - Cache warming

8. Monitoring & Metrics:
   - APM tools
   - Performance budgets
   - Real User Monitoring (RUM)
   - Synthetic monitoring
   - Key performance indicators
   - Benchmarking

Optimization principles:
- Measure before optimizing
- Focus on bottlenecks first
- Consider trade-offs (speed vs memory)
- Use appropriate data structures
- Minimize I/O operations
- Implement caching strategically
- Optimize critical paths
- Profile in production-like environments
- Set performance budgets
- Monitor continuously"""

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
            if context.get("code"):
                prompt += f"- Code:\n```{context.get('language', '')}\n{context['code']}\n```\n"
            if context.get("performance_issue"):
                prompt += f"- Performance Issue: {context['performance_issue']}\n"
            if context.get("metrics"):
                prompt += f"- Current Metrics: {context['metrics']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = "".join(block.text for block in response.content if block.type == "text")
        
        import re
        optimizations = []
        code_blocks = re.findall(r"```(\w+)\n(.*?)```", text_content, re.DOTALL)
        
        for language, code in code_blocks:
            optimizations.append({"language": language, "content": code.strip()})
        
        recommendations = []
        for line in text_content.split('\n'):
            if any(marker in line.lower() for marker in ['optimize', 'improve', 'reduce', 'increase', 'cache']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 20:
                    recommendations.append(clean)
        
        return {"response": text_content, "optimizations": optimizations, "recommendations": recommendations[:10]}


if __name__ == "__main__":
    agent = PerformanceAgent()
    result = agent.execute("Optimize this nested loop", 
                          {"code": "for i in range(n):\n    for j in range(n):\n        result.append(arr[i] + arr[j])", 
                           "language": "python", "performance_issue": "O(n^2) complexity"})
    print(f"Optimizations: {len(result['optimizations'])}")
