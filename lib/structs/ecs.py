from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
)
from constructs import Construct

class ECS(Construct):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = vpc
        self.__create_ecs_cluster()

    def __create_ecs_cluster(self):
        self.cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=self.vpc
        )