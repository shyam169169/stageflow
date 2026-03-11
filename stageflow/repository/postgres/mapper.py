from stageflow.core.domain.models.models import WorkflowInstance, TransitionRecord
from stageflow.repository.postgres.models import WorkflowInstanceModel, TransitionHistoryModel


class WorkflowIntanceWrapper:
    @staticmethod
    def to_domain(model: WorkflowInstanceModel) -> WorkflowInstance:
        return WorkflowInstance(
            id=model.id,
            workflow_name=model.workflow_name,
            current_stage=model.current_stage,
            reference_id=model.reference_id,
            reference_domain=model.reference_domain,
            metadata=model.metadata_json or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
            version=model.version,
            workflow_version=model.workflow_version
        )

    @staticmethod
    def to_model(domain: WorkflowInstance) -> WorkflowInstanceModel:
        return WorkflowInstanceModel(
            id=domain.id,
            workflow_name=domain.workflow_name,
            current_stage=domain.current_stage,
            reference_id=domain.reference_id,
            reference_domain=domain.reference_domain,
            metadata_json=domain.metadata or {},
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            version=domain.version,
            workflow_version=domain.workflow_version
        )

class TransitionHistoryWrapper:
    @staticmethod
    def to_domain(model: TransitionHistoryModel) -> TransitionRecord:
        return TransitionRecord(
            id=model.id,
            instance_id=model.instance_id,
            from_stage=model.from_stage,
            to_stage=model.to_stage,
            created_at=model.created_at,
            metadata_snapshot=model.metadata_snapshot_json or {}
        )
    
    @staticmethod
    def to_model(transtion: TransitionRecord) -> TransitionHistoryModel:
        return TransitionHistoryModel(
            id=transtion.id,
            instance_id=transtion.instance_id,
            from_stage=transtion.from_stage,
            to_stage=transtion.to_stage,
            created_at=transtion.created_at,
            metadata_snapshot_json=transtion.metadata_snapshot or {}
        )