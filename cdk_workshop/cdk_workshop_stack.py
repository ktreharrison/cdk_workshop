from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from cdk_dynamo_table_view import TableViewer
from constructs import Construct

from .hitcounter import HitCounter


class CdkWorkshopStack(Stack):
    
    @property
    def hc_endpoint(self):
        return self._hc_endpoint
    
    
    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url
    
    # boilerplat code for Python CDK
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime = _lambda.Runtime.PYTHON_3_7,
            code = _lambda.Code.from_asset('lambda'),
            handler = 'hello.handler',                                     
        )
        
        # adding hit counter 
        hello_with_counter = HitCounter(
            self,
            'HelloHitCounter',
            downstream=my_lambda,
        )
        
        # Define an API Gateway resource 
        gateway = apigw.LambdaRestApi(self, "Endpoint", handler=hello_with_counter._handler)
        
        # Using the aws cdk ddb table viewer
        tv = TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
            sort_by='-hits'
        )
        
        self._hc_endpoint = CfnOutput(
            self, 
            'GatwayUrl',
            value=gateway.url
        )
        self._hc_viewer_url = CfnOutput(
            self,
            'TableViewerUrl',
            value=tv.endpoint
            
        )