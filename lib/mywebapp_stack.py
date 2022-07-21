from typing import Dict
from aws_cdk import (
    Stack,
    Duration,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ecs_patterns as patterns,
    aws_ecr_assets as assets
)
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_servicediscovery as servicediscovery
from constructs import Construct
from .structs.vpc import MyVpc
from .structs.sg import MySecurityGroup
from .structs.ecs import ECS
from .structs.iam import Role
from .structs.ecs import ECS
from .structs.task_definition import TaskDefinition
from utils.stack_util import add_tags_to_stack

class MyWebApp(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: Dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Apply common tags to stack resources.
        add_tags_to_stack(self, config)

        # Create VPC
        vpc_construct = MyVpc(self, 'Vpc', config)
        my_vpc = vpc_construct.vpc

        # Create security group
        ecs_sg = MySecurityGroup(self, "ECSSecurityGroup", my_vpc, "ECS SG")

        # Create ECS Cluster
        webAppCluster = ECS(self, "MyECS", my_vpc)

        # Create Service Discovery
        namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
            name="mywebapp.com",
            vpc=my_vpc
        )
        service = namespace.create_service("DiscoveryService",
            dns_record_type=servicediscovery.DnsRecordType.A,
            dns_ttl=Duration.seconds(30),
            load_balancer=True
        )
        # Create Take Definitions
        nginx_task_def = TaskDefinition(self, "nginx_td", config)
        webApp_task_def = TaskDefinition(self, "webapp_td", config)

        # Create containers and port mappings
        image_nginx = assets.DockerImageAsset(
            self, "nginx_image", directory="./lib/docker/nginx", file="Dockerfile"
        )

        myNginxContainer = nginx_task_def.td.add_container(
            'nginx_container', 
            cpu=256,
            memory_limit_mib=512,
            image=ecs.ContainerImage.from_docker_image_asset(image_nginx),
            ).add_port_mappings(ecs.PortMapping(container_port=80,protocol=ecs.Protocol.TCP))

        image_webapp = assets.DockerImageAsset(
            self, "webapp_image", directory="./lib/docker/httpd", file="Dockerfile"
        )

        myWebAppContainer = webApp_task_def.td.add_container(
            'webapp_container', 
            cpu=256,
            memory_limit_mib=512,
            image=ecs.ContainerImage.from_docker_image_asset(image_webapp),
            ).add_port_mappings(ecs.PortMapping(container_port=3000, protocol=ecs.Protocol.TCP))

        # Create ECS Services
        myWebAppService = ecs.FargateService(self, "webapp_service",
            cluster=webAppCluster.cluster,
            task_definition=webApp_task_def.td,
            security_groups=[ecs_sg.sg], 
            service_name="myWebApp",
            cloud_map_options=ecs.CloudMapOptions(
                name="webapp",
                dns_record_type=servicediscovery.DnsRecordType.A,
                cloud_map_namespace=namespace,
                container=myWebAppContainer,
                container_port=3000
            )
        ).connections.allow_internally(port_range=ec2.Port.tcp(3000))

        # Create ApplicationLoadBalanced FargateService
        load_balanced_fargate_service = patterns.ApplicationLoadBalancedFargateService(
            self, "myWebAppAlbFargateService",
            service_name="nginx",
            task_definition=nginx_task_def.td,
            cluster=webAppCluster.cluster,
            security_groups=[ecs_sg.sg],
            desired_count=1,
            cpu=256,
            memory_limit_mib=512,
            protocol=elbv2.ApplicationProtocol.HTTP,
            )

        #Create Roles 
        ecs_role = Role(
            scope=self, 
            construct_id="myECSRole", 
            assumed_by="ec2.amazonaws.com"
            )

        ecs_task_execution_role = Role(
            scope=self, 
            construct_id="myECSTaskExecutionRole", 
            assumed_by="ecs-tasks.amazonaws.com"
        )

        # Attach Policy statements to Roles
        ecs_role.iam_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ec2:AttachNetworkInterface",
                "ec2:CreateNetworkInterface",
                "ec2:CreateNetworkInterfacePermission",
                "ec2:DeleteNetworkInterface",
                "ec2:DeleteNetworkInterfacePermission",
                "ec2:Describe*",
                "ec2:DetachNetworkInterface",
                "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
                "elasticloadbalancing:DeregisterTargets",
                "elasticloadbalancing:Describe*",
                "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
                "elasticloadbalancing:RegisterTargets",
            ]
        ))

        ecs_task_execution_role.iam_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
            ]
        ))
