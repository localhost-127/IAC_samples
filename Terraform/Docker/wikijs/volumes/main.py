#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.docker import DockerProvider , Volume


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        
        DockerProvider(self,id="docker_id", host="npipe:////.//pipe//docker_engine")
        dbVolume = Volume(self, id="post_volume", name="post_volume")


app = App()
MyStack(app, "volumes")

app.synth()
