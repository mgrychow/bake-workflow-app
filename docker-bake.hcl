group "default" {
    targets = ["bake-workflow-app"]
}

target "bake-workflow-app" {
    context = "."
    dockerfile = "Dockerfile"
    args = {
        PING_RESPONSE = "aaargh!"
    }
    tags = ["bake-workflow-app:latest"]
    output = ["type=docker"]
}
