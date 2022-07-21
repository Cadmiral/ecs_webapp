from aws_cdk import (
    aws_iam as iam
)
from constructs import Construct

class Role(Construct):

    def __init__(self, scope: Construct, construct_id: str, assumed_by: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.construct_id = construct_id
        self.assumed_by = assumed_by
        self.__create_role()

    def __create_role(self):
        self.iam_role = iam.Role(
            scope=self, 
            id=self.construct_id, 
            assumed_by=iam.ServicePrincipal(self.assumed_by)
            )