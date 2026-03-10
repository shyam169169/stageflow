import pytest

from stageflow.hooks.base_hooks import Hook
from test_workflow_engine import create_instance, create_engine, create_workflow


class MockHook(Hook):
    def __init__(self):
        self.prehooks_called = False
        self.posthooks_called = False
    
    def perform_pre_hook(self, context):
        self.prehooks_called = True

    def perform_post_hook(self, context):
        self.posthooks_called = True

def test_hooks():
    engine = create_engine()
    workflow = create_workflow(engine)
    instance = create_instance(engine, workflow)
    
    hook = MockHook()
    engine.register_hooks(hook)

    engine.do_transition(instance.id, "PACKED")

    assert hook.prehooks_called is True
    assert hook.posthooks_called is True


    
    