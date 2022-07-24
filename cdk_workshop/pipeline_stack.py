from aws_cdk import Stack
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import pipelines as pipelines
from constructs import Construct
from cdk_workshop.pipeline_stage import WorkshopPipelineStage


class WorkshopPipelineStack(Stack):
    # Python CDK Boilerplate Stack code
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
    
        # Create a CommitCode repository called 'WorkshopRepo'
        repo = codecommit.Repository(self, 
                'WorkshopRepo', repository_name = 'WorkshopRepo'
        )
        
        # Creating a pipline 
        pipeline = pipelines.CodePipeline(
            self, 
            'Pipeline', 
            synth=pipelines.ShellStep(
                'Synth', 
                input=pipelines.CodePipelineSource.code_commit(repo,'main'),
                commands=[
                    "npm install -g aws-cdk", # Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt", # Instructs Codebuild to install required packages
                    'cdk synth'
                          ]
        
            )
        )
        deploy = WorkshopPipelineStage(self, 'Deploy')
        deploy_stage = pipeline.add_stage(deploy)
            
         