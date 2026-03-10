from stageflow.rules.base_rule import Rule

class MetadataRule(Rule):
    def __init__(self, key: str, expected_value):
        super().__init__()
        self.key = key
        self.expected_value = expected_value

    def evaluate(self, context) -> bool:
        return context.instance.metadata.get(self.key) == self.expected_value