#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, TerraformVariable
from imports.docker import DockerProvider, Container, Image, ContainerPorts, ContainerUpload, ContainerVolumes, Network
from sensitives.sensitive import wiki_conf

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        DockerProvider(self,id="docker_id", host="npipe:////.//pipe//docker_engine")
        image_wiki = Image(self, id="wikiJs_image",name="linuxserver/wikijs",keep_locally=True)
        image_postgres = Image(self, id="postgres_image", name="postgres", keep_locally=True) 
        wPort = ContainerPorts(internal=3000,external=3001, protocol="tcp")
        pPort = ContainerPorts(internal=5432,external=5432, protocol="tcp")
        upload_config = ContainerUpload(file="/config/config.yml", source=wiki_conf)
        
        network = Network(self, id="local_Network", name="local_Network")
        
        
        conVolume = ContainerVolumes(container_path="/var/lib/postgresql/data", volume_name="post_volume" )
        postgres = Container(self, id="postgres", ports=[pPort], image=image_postgres.name, name="postgres",
                  volumes=[conVolume],
                  networks=["local_Network"],
                  network_alias=["postgres"],
                  env=[ 
                       "POSTGRES_USER=wiki",
                       "POSTGRES_PASSWORD=secret"
                    ],
                  depends_on=[network]
                  )

        wikijs = Container( self, id="wikiJs", ports=[wPort], image=image_wiki.name, name="wikiJs", upload=[upload_config],
                            networks=["local_Network"],
                            env=[ "PUID=1000", "PGID=1000",
                                    "TZ=Asia/Kolkata",
                                    "DB_TYPE=postgres",
                                    "DB_HOST=postgres",
                                    "DB_PORT=5432",
                                    "DB_USER=wiki",
                                    "DB_PASS=secret" 
                                ],
                            #restart="unless-stopped" ,
                            depends_on=[postgres, network]
                  )


app = App()
MyStack(app, "wikijs")

app.synth()
