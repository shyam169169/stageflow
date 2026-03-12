import importlib
import pkgutil

from stageflow.engine.core_engine import WorkflowEngine


def workflows_loader(engine: WorkflowEngine, package):

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):

        module = importlib.import_module(
            f"{package.__name__}.{module_name}"
        )
        if hasattr(module, "workflow"):
            engine.register_workflow(module.workflow)