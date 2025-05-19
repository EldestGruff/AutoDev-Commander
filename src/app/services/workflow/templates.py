from typing import Dict, Any
from enum import Enum

class WorkflowTemplate(Enum):
    CODE_REVIEW = "code_review"
    DEPENDENCY_CHECK = "dependency_check"
    SECURITY_SCAN = "security_scan"
    TEST_GENERATION = "test_generation"

class WorkflowTemplateManager:
    @staticmethod
    def get_template(template_type: WorkflowTemplate) -> Dict[str, Any]:
        templates = {
            WorkflowTemplate.CODE_REVIEW: {
                "name": "Code Review Workflow",
                "nodes": [
                    {
                        "type": "ai.code_review",
                        "parameters": {
                            "model": "llama2",
                            "temperature": 0.7
                        }
                    },
                    {
                        "type": "github.create_review",
                        "parameters": {
                            "status": "{{$node.ai_review.output.status}}",
                            "comments": "{{$node.ai_review.output.comments}}"
                        }
                    }
                ]
            },
            WorkflowTemplate.TEST_GENERATION: {
                "name": "Test Generation Workflow",
                "nodes": [
                    {
                        "type": "ai.analyze_code",
                        "parameters": {
                            "model": "llama2"
                        }
                    },
                    {
                        "type": "ai.generate_tests",
                        "parameters": {
                            "framework": "pytest",
                            "coverage_target": 0.8
                        }
                    }
                ]
            }
        }
        return templates.get(template_type, {})
