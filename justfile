docker := require("docker")
uv := require("uv")

PACKAGE := "rnadvisor"
REPOSITORY := "rnadvisor"
SOURCES := "src"
TESTS := "tests"

default:
    @just --list

# IMPORTS

import 'tasks/build-slim.just'
import 'tasks/check.just'
import 'tasks/format.just'