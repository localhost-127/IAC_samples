terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "2.15.0"
    }
  }
}

provider "docker" {
  host    = "npipe:////.//pipe//docker_engine"
}


resource "docker_container" "Anaconda" {
  image = "continuumio/anaconda3"
  name  = "Anaconda"

  #entrypoint = ["/bin/bash -c \"conda install jupyter -y && mkdir -p /opt/notebooks && jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser --allow-root\"" ]
  tty = true
  ports {
    internal = 8888
    external = 8888
  }
  #command = ["/usr/bin/conda install jupyter -y", "jupyter notebook --port=8888 --no-browser --allow-root" ]
  volumes {
	  container_path = "/home/user"
	  volume_name = "notebooks_vol"
  }
}

resource "docker_volume" "notebooks_vol" {
  name = "notebooks_vol"
}
