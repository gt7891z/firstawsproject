import os
import aws_cdk as core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_route53 as r53
from aws_cdk import aws_route53_targets as r53targets
from aws_cdk import aws_certificatemanager as certs
from constructs import Construct


class FirstAwsProjectStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        zone_name = "gt7891z.com"
        host_name = "www"
        fqdn = f"{host_name}.{zone_name}"

        bucket = s3.Bucket(
            self,
            "WebBucket",
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        zone = r53.HostedZone.from_lookup(self, "HostedZone", domain_name=zone_name)

        certificate = certs.Certificate(
            self,
            "Cert",
            domain_name=fqdn,
            validation=certs.CertificateValidation.from_dns(hosted_zone=zone),
        )

        cdn = cloudfront.Distribution(
            self,
            "webDist",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket)
            ),
            default_root_object="index.html",
            certificate=certificate,
            domain_names=[fqdn],
        )

        r53.ARecord(
            self,
            "Record",
            zone=zone,
            target=r53.RecordTarget.from_alias(r53targets.CloudFrontTarget(cdn)),
            record_name=host_name
        )

        s3deploy.BucketDeployment(
            self,
            "deployment",
            sources=[
                s3deploy.Source.asset(
                    os.path.join(os.path.dirname(__file__), "..", "website")
                )
            ],
            destination_bucket=bucket,
            distribution=cdn,
        )
