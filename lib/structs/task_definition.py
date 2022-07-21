from typing import Dict, List
import aws_cdk.aws_ecs as ecs
from constructs import Construct


class TaskDefinition(Construct):

    def __init__(self, scope: Construct, id: str, config: Dict) -> None:
        super().__init__(scope, id)

        self.id = id
        self.__create_task_definition()

    def __create_task_definition(self):
        self.td = ecs.FargateTaskDefinition(
            scope=self,
            id=self.id,
            family=self.id,
            cpu=256,
            memory_limit_mib=512,
            )