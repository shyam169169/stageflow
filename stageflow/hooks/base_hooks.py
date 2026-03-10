
from abc import ABC
from stageflow.core.domain.context import TransitionContext

class Hook(ABC):
    def perform_pre_hook(self, context: TransitionContext):
        pass

    def perform_post_hook(self, context: TransitionContext):
        pass

