#!/bin/bash

if [ $# -gt 0 ]; then
    ARG=$1
    docker buildx bake --print -f docker-bake.hcl -f docker-bake-override.hcl -f $ARG
    docker buildx bake -f docker-bake.hcl -f docker-bake-override.hcl -f $ARG
else
    docker buildx bake --print -f docker-bake.hcl -f docker-bake-override.hcl
    docker buildx bake -f docker-bake.hcl -f docker-bake-override.hcl
fi