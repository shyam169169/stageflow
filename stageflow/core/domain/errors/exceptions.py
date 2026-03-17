
class StageFlowException(Exception):
    """Base exception for StageFlow"""
    code = "STAGEFLOW_EXCEPTION"

class WorkflowNotFoundException(StageFlowException):
    code = "WORKFLOW_NOT_FOUND_EXCEPTION"

class InstanceNotFoundException(StageFlowException):
    code = "INSTANCE_NOT_FOUND_EXCEPTION"

class ConcurrentTransitionException(StageFlowException):
    code = "CONCURRENT_TRANSITION_EXCEPTION"

class InvalidTansitionException(StageFlowException):
    code = "INVALID_TRANSITION_EXCEPTION"

class RuleVoilationException(StageFlowException):
    code = "RULE_VIOLATION_EXCEPTION"

class WorkflowValidationException(StageFlowException):
    passcode = "WORKFLOW_VALIDATION_EXCEPTION"