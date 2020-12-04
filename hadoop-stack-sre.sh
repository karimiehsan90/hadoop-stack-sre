#!/usr/bin/env bash

set -euo pipefail

build() {
  dockerfiles=$(find . -name Dockerfile)

  for dockerfile in ${dockerfiles}; do
    docker_dir=$(dirname "${dockerfile}")
    docker_tag=$(head -n 1 "${dockerfile}" | cut -d ' ' -f 2)
    docker build -t "${docker_tag}" -f "${dockerfile}" "${docker_dir}"
  done
}

deploy() {
  dockerfiles=$(find . -name Dockerfile)
  username=$1

  for dockerfile in ${dockerfiles}; do
    docker_dir=$(dirname "${dockerfile}")
    docker_tag=$(head -n 1 "${dockerfile}" | cut -d ' ' -f 2)
    docker build -t "${docker_tag}" -f "${dockerfile}" "${docker_dir}"
    docker tag "${docker_tag}" "${username}/${docker_tag}"
    docker push "${username}/${docker_tag}"
  done
}

METHOD=${1}
shift

${METHOD} "${@}"
