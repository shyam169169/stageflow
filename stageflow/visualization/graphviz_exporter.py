from stageflow.core.domain.models.models import WorkflowDefinition

class GraphvizExporter:
    @staticmethod
    def to_dot(workflow: WorkflowDefinition) -> str:

        lines = []

        lines.append(f"digraph {workflow.name} {{")
        lines.append("    rankdir=LR;")

        # declare stages
        for stage in workflow.stages:

            if stage.is_terminal:
                lines.append(
                    f'    "{stage.name}" [shape=doublecircle];'
                )
            else:
                lines.append(
                    f'    "{stage.name}" [shape=circle];'
                )

        # transitions
        for transition in workflow.transitions:

            lines.append(
                f'    "{transition.from_stage}" -> "{transition.to_stage}";'
            )

        lines.append("}")

        return "\n".join(lines)