"""Claude Code Agents - Specialized AI Agents for Software Development"""

# Infrastructure agents
from .infrastructure.docker_agent import DockerAgent
from .infrastructure.devops_agent import DevOpsAgent
from .infrastructure.observability_agent import ObservabilityAgent

# Development agents
from .development.database_agent import DatabaseAgent
from .development.frontend_agent import FrontendAgent
from .development.mobile_agent import MobileAgent

# Quality agents
from .quality.test_suite_agent import TestSuiteAgent
from .quality.security_agent import SecurityAgent
from .quality.code_review_agent import CodeReviewAgent
from .quality.refactoring_agent import RefactoringAgent
from .quality.performance_agent import PerformanceAgent

# Operations agents
from .operations.migration_agent import MigrationAgent
from .operations.dependency_agent import DependencyAgent
from .operations.git_agent import GitAgent

# Productivity agents
from .productivity.scaffolding_agent import ScaffoldingAgent
from .productivity.documentation_agent import DocumentationAgent
from .productivity.debugging_agent import DebuggingAgent

# Business agents
from .business.validation_agent import ValidationAgent
from .business.architecture_agent import ArchitectureAgent
from .business.localization_agent import LocalizationAgent
from .business.compliance_agent import ComplianceAgent

# Specialized agents
from .specialized.data_science_agent import DataScienceAgent

__all__ = [
    # Infrastructure
    'DockerAgent',
    'DevOpsAgent',
    'ObservabilityAgent',
    # Development
    'DatabaseAgent',
    'FrontendAgent',
    'MobileAgent',
    # Quality
    'TestSuiteAgent',
    'SecurityAgent',
    'CodeReviewAgent',
    'RefactoringAgent',
    'PerformanceAgent',
    # Operations
    'MigrationAgent',
    'DependencyAgent',
    'GitAgent',
    # Productivity
    'ScaffoldingAgent',
    'DocumentationAgent',
    'DebuggingAgent',
    # Business
    'ValidationAgent',
    'ArchitectureAgent',
    'LocalizationAgent',
    'ComplianceAgent',
    # Specialized
    'DataScienceAgent',
]
