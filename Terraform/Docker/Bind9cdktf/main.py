#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformVariable
from imports.docker import DockerProvider,Container, ContainerPorts,DockerProviderConfig, Image, ContainerUpload
from local.sensitive_data import b9ConfigPath as configpath

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        
        conf_var = TerraformVariable(self, id="b9_ConfigPath", default=configpath, sensitive=True)

        DockerProvider(self,id="docker_id", host="npipe:////.//pipe//docker_engine")
        image = Image(self, id="Bind9_image",name="resystit/bind9",keep_locally=True)
        tPort = ContainerPorts(internal=53,external=53, protocol="tcp")
        uPort = ContainerPorts(internal=53,external=53, protocol="udp")
        upload_config = ContainerUpload(file="/etc/bind/named.conf", source=conf_var.default)
        Container(self, id="dns_id", ports=[tPort,uPort], image=image.name, name="DDNS", upload=[upload_config])


import os
cwd=os.getcwd()
print(cwd)
app = App()
MyStack(app, "Bind9DDNS")

app.synth()
