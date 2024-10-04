group "default" {
    targets = ["bake-workflow-app", "bake-workflow-app-test"]
}

variable "RESP_MESSAGE" {
  default = "hello"
}

target "bake-workflow-app" {
    context = "."
    dockerfile = "Dockerfile"
    args = {
        PING_RESPONSE = RESP_MESSAGE
    }
    tags = ["bake-workflow-app:latest"]
    output = ["type=docker"]
}

target "bake-workflow-app-test" {
    context = "."
    dockerfile = "tests.Dockerfile"
    args = {
        PING_RESPONSE = RESP_MESSAGE
    }
    tags = ["bake-workflow-app-test:latest"]
    output = ["type=docker"]
}
