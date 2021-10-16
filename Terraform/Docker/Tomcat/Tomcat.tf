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


resource "docker_container" "Tomcat" {
  image = "tomcat:7.0.8"
  name  = "tomcat"

  ports {
    internal = 8080
    external = 8080
  }
}
