import aws_cdk.aws_ec2 as ec2
from constructs import Construct


class MySecurityGroup(Construct):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, description: str) -> None:
        super().__init__(scope, construct_id)

        self._description = description
        self._construct_id = construct_id
        self._vpc = vpc
        self.__create_sg()

    # Create alb security group
    def __create_sg(self):
        self.sg = ec2.SecurityGroup(
            self, self._construct_id,
            security_group_name=self._construct_id,
            vpc=self._vpc,
            description=self._description,
        )