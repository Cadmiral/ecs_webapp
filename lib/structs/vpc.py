from typing import Dict, List
import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct


class MyVpc(Construct):
    config : Dict
    vpc = ec2.Vpc
    subnet_configuration: List[ec2.SubnetConfiguration] = []

    def __init__(self, scope: Construct, id: str, config: Dict) -> None:
        super().__init__(scope, id)
        self.config = config

        self.__create_subnets()
        self.__create_vpc()

    def __create_vpc(self):
        vpc_config = self.config['network']['vpc']
        self.vpc = ec2.Vpc(
            scope=self,
            id=self.config['name'],
            subnet_configuration=self.subnet_configuration,
            max_azs=vpc_config['maxAzs'],
            cidr=vpc_config['cidr'],
            enable_dns_hostnames=vpc_config['enableDnsHostnames'],
            enable_dns_support=vpc_config['enableDnsSupport'],
            nat_gateways= 1,
            nat_gateway_subnets=ec2.SubnetSelection(
                subnet_group_name=vpc_config['natGatewaySubnetName']
            ),
        )

    def __create_subnets(self):
        for subnet in self.config['network']['subnets']:
            self.subnet_configuration.append(ec2.SubnetConfiguration(
                name=subnet['name'],
                subnet_type=ec2.SubnetType[subnet['subnetType']],
                cidr_mask=subnet['cidrMask'],
            ))