from stageflow.hooks.base_hooks import Hook

class WebHook(Hook):
    def perform_post_hook(self, context):
        print (f"Running post-hooks")