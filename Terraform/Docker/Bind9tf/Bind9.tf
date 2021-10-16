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

resource "docker_container" "Bind9" {
  image = "resystit/bind9:latest"
  name  = "bind9_name"
  attach=true
  stdin_open=true
  tty=true
  upload{
	file="/etc/bind/named.conf"
	source="./named.conf"
  }
  ports {
    internal = 53
    external = 30053
	ip="*"
	protocol="tcp"
  }
}

