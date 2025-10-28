"""
Database Agent - Specialized agent for database operations in Claude Code

This agent handles:
- Schema design and migrations
- Query optimization
- Index recommendations
- ORM configuration
- Database seeding
"""

from anthropic import Anthropic
import json
import os
from typing import List, Dict, Optional

class DatabaseAgent:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        
        self.system_prompt = """You are a database specialist agent with expertise in:

1. Schema Design:
   - Normalized database design (1NF, 2NF, 3NF, BCNF)
   - Denormalization for performance
   - Entity-relationship modeling
   - Primary and foreign key relationships
   - Constraints (unique, check, not null)
   - Data types selection

2. Query Optimization:
   - Query plan analysis (EXPLAIN)
   - Index usage optimization
   - JOIN optimization
   - Subquery vs JOIN performance
   - Query rewriting
   - N+1 query problem resolution

3. Indexing Strategy:
   - B-tree, Hash, GiST, GIN indexes
   - Composite indexes
   - Partial indexes
   - Covering indexes
   - Index maintenance
   - When NOT to use indexes

4. Database Systems:
   - PostgreSQL, MySQL, SQL Server
   - MongoDB, DynamoDB, Cassandra
   - Redis, Elasticsearch
   - SQLite for embedded use
   - Database-specific features and optimizations

5. Migrations:
   - Zero-downtime migrations
   - Data migration strategies
   - Rollback procedures
   - Version control for schemas
   - Migration tools (Alembic, Flyway, Liquibase)

6. ORM Best Practices:
   - SQLAlchemy, Django ORM, TypeORM, Prisma
   - Lazy vs eager loading
   - N+1 query prevention
   - Raw queries when needed
   - Transaction management

7. Data Integrity:
   - ACID properties
   - Transaction isolation levels
   - Concurrency control
   - Deadlock prevention
   - Constraint enforcement

8. Performance:
   - Connection pooling
   - Caching strategies
   - Partitioning and sharding
   - Read replicas
   - Query result caching

When designing databases:
- Follow normalization principles unless denormalization is justified
- Use appropriate data types
- Add proper indexes for query patterns
- Include audit columns (created_at, updated_at)
- Plan for scalability
- Consider data retention and archival
- Implement soft deletes when appropriate
- Use database constraints to enforce business rules"""

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
            if context.get("database_type"):
                prompt += f"- Database: {context['database_type']}\n"
            if context.get("orm"):
                prompt += f"- ORM: {context['orm']}\n"
            if context.get("schema"):
                prompt += f"- Current Schema:\n{context['schema']}\n"
            if context.get("query"):
                prompt += f"- Query:\n{context['query']}\n"
            if context.get("requirements"):
                prompt += f"- Requirements: {context['requirements']}\n"
            prompt += "\n"
        
        return prompt
    
    def _parse_response(self, response) -> dict:
        text_content = ""
        schemas = []
        queries = []
        migrations = []
        
        for block in response.content:
            if block.type == "text":
                text_content += block.text
        
        import re
        code_pattern = r"```(\w+)\n(.*?)```"
        code_blocks = re.findall(code_pattern, text_content, re.DOTALL)
        
        for language, code in code_blocks:
            if language.lower() in ['sql', 'postgresql', 'mysql']:
                if 'create table' in code.lower():
                    schemas.append({"language": language, "content": code.strip()})
                elif 'alter table' in code.lower() or 'add column' in code.lower():
                    migrations.append({"language": language, "content": code.strip()})
                else:
                    queries.append({"language": language, "content": code.strip()})
            elif language.lower() == 'python':
                if 'class' in code and ('Base' in code or 'Model' in code):
                    schemas.append({"language": language, "content": code.strip()})
        
        return {
            "response": text_content,
            "schemas": schemas,
            "queries": queries,
            "migrations": migrations
        }
    
    def design_schema(self, requirements: str, database_type: str = "postgresql") -> dict:
        task = "Design a database schema based on these requirements"
        return self.execute(task, {"requirements": requirements, "database_type": database_type})
    
    def optimize_query(self, query: str, database_type: str = "postgresql") -> dict:
        task = "Analyze and optimize this query for better performance"
        return self.execute(task, {"query": query, "database_type": database_type})


# Example usage
if __name__ == "__main__":
    agent = DatabaseAgent()
    
    result = agent.design_schema(
        requirements="E-commerce system with users, products, orders, and reviews",
        database_type="postgresql"
    )
    
    print(f"Schemas created: {len(result['schemas'])}")
    print(f"Migrations: {len(result['migrations'])}")
