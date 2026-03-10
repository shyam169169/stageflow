from stageflow.hooks.base_hooks import Hook

class AuditHook(Hook):
    def perform_pre_hook(self, context):
        print (f"Running pre-hooks")