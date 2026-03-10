from stageflow.rules.base_rule import Rule

class TimeWindowRule(Rule):
    def __init__(self, start_hour: int, end_hour: int):
        super().__init__()
        self.start_hour = start_hour
        self.end_hour = end_hour

    def evaluate(self, context) -> bool:
        current_hour = context.timestamp.hour
        return self.start_hour <= current_hour <= self.end_hour