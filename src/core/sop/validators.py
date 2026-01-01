import json
import os
import re

class SOPValidators:
    @staticmethod
    def validate_ba(content):
        if not content: return False
        return "Goals" in content and "Risks" in content

    @staticmethod
    def validate_prd(content):
        if not content: return False
        return "Goal" in content and "Requirements" in content

    @staticmethod
    def validate_design(content):
        try:
            # Extract JSON if embedded in text
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            
            data = json.loads(content)
            expected = ["modules", "files"] 
            return any(key in data for key in expected)
        except:
            return False

    @staticmethod
    def validate_tasks(content):
        return len(content.strip()) > 0

    @staticmethod
    def validate_code(content):
        return "Stored in" in content or "Created" in content or len(content) > 10

    @staticmethod
    def validate_tests(content):
        return "test" in content.lower()

    @staticmethod
    def validate_governance(content):
        return "APPROVED" in content.upper()

    @staticmethod
    def validate_delivery(content):
        return "Artifacts" in content or "Ready" in content

    @staticmethod
    def validate_simplicity(content):
        """Checks if content follows the Clean Simple format."""
        required = ["TITLE:", "PURPOSE:", "OUTPUT:", "NEXT STEP:"]
        return all(tag in content for tag in required)

def get_validator(name):
    validators = {
        "validate_ba": SOPValidators.validate_ba,
        "validate_prd": SOPValidators.validate_prd,
        "validate_design": SOPValidators.validate_design,
        "validate_tasks": SOPValidators.validate_tasks,
        "validate_code": SOPValidators.validate_code,
        "validate_tests": SOPValidators.validate_tests,
        "validate_governance": SOPValidators.validate_governance,
        "validate_delivery": SOPValidators.validate_delivery,
        "validate_simplicity": SOPValidators.validate_simplicity
    }
    return validators.get(name, lambda x: True)
