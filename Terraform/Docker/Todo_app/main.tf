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


#TODO: disable Caching->on by default
resource "docker_image" "todo_app_image" {
  name = "todo_app_image:develop"
  
  build {
    path = "./todo_app"
    tag  = ["todo_app_image:develop"]
    build_arg = {
	#guess environmental varialbles should be here?
      foo : "zoo"
    }
    label = {
      author : "Rosh"
    }
	no_cache = true
  }
}

resource "docker_container" "todo_app" {
  image = docker_image.todo_app_image.name
  name  = "Terraform_check"
  ports {
    internal = 3000
    external = 3000
  }
  restart = "always"
  depends_on = [
    docker_image.todo_app_image,
  ]
}
