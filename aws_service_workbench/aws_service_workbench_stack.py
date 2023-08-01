from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput, aws_ec2 as ec2,
)
from constructs import Construct

from aws_service_workbench.hosting.instance_stack import InstanceStack
from aws_service_workbench.networking.networking_stack import NetworkingStack
from aws_service_workbench.security.security_stack import SecurityStack


class AwsServiceWorkbenchStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =====================
        # NETWORKING
        # =====================
        net = NetworkingStack(
            self,
            "NetworkingStack",
        )

        CfnOutput(
            self,
            "VpcId",
            description="Identifier for this VPC.",
            value=net.vpc.vpc_id,
        )

        # =====================
        # SECURITY
        # =====================
        sec = SecurityStack(
            self,
            "SecurityStack",
            vpc=net.vpc,
            whitelisted_peer=ec2.Peer.prefix_list(self.node.try_get_context("peers"))
        )

        # =====================
        # COMPUTE
        # =====================
        instance = InstanceStack(
            self,
            "InstanceStack",
            vpc=net.vpc,
            security_group=sec.outer_perimeter_security_group,
            key_name=self.node.try_get_context("key_name"),
            debug_mode=True,
        )
