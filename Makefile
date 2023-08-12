# Awesome reference: @see https://tech.davis-hansson.com/p/make/

# Tells Make, that this Makefile is written with Bash as the shell
SHELL := bash 

# Add the -T options to "docker compose exec" to avoid the 
# "panic: the handle is invalid"
# error on Windows and Linux 
# @see https://stackoverflow.com/a/70856332/413531
DOCKER_COMPOSE_EXEC_OPTIONS=-T

# Empty for Linux and Mac
WINPTY_PREFIX=

# OS is a defined variable for WIN systems, so "uname" will not be executed
OS?=$(shell uname)
# Values of OS:
#   Windows => Windows_NT 
#   Mac 	=> Darwin 
#   Linux 	=> Linux 
ifeq ($(OS),Windows_NT)
# Windows requires the .exe extension, otherwise the entry is ignored
# @see https://stackoverflow.com/a/60318554/413531
    SHELL := bash.exe
    # When allocating a terminal, the corresponding command must be prefixed
    # with `winpty` to avoid the "The input device is not a TTY" error
    # @see http://www.pascallandau.com/blog/setting-up-git-bash-mingw-msys2-on-windows/#the-role-of-winpty-fixing-the-input-device-is-not-a-tty
	WINPTY_PREFIX=winpty
# Export MSYS_NO_PATHCONV=1 as environment variable to avoid automatic path conversion
# (the export does only apply locally to `make` and the scripts that are invoked,
# it does not affect the global environment)
    # @see http://www.pascallandau.com/blog/setting-up-git-bash-mingw-msys2-on-windows/#fixing-the-path-conversion-issue-for-mingw-msys2
	export MSYS_NO_PATHCONV=1
else ifeq ($(OS),Darwin)
    # On Mac, the -T must be omitted to avoid cluttered output
    # @see https://github.com/moby/moby/issues/37366#issuecomment-401157643
	DOCKER_COMPOSE_EXEC_OPTIONS=
endif

# Use bash strict mode @see http://redsymbol.net/articles/unofficial-bash-strict-mode/
# -e | instructs bash to immediately exit if any command has a non-zero exit status
# -u | a reference to any variable you haven't previously defined, with the exceptions of $* and $@, is an error
# -o pipefail | if any command in a pipeline fails, that return code will be used as the return code of the whole pipeline. By default, the pipeline's return code is that of the last command - even if it succeeds.
# @see https://unix.stackexchange.com/a/179305
# -c | Read and execute commands from string after processing the options. Otherwise, arguments are treated  as filed. Example:
# bash -c "echo foo" # will excecute "echo foo"
# bash "echo foo"    # will try to open the file named "echo foo" and execute it 
.SHELLFLAGS := -euo pipefail -c

# @see https://tech.davis-hansson.com/p/make/
# Display a warning if variables are used but not defined
MAKEFLAGS += --warn-undefined-variables
# Remove some "magic make behavior"
MAKEFLAGS += --no-builtin-rules

# Don't print directory information by default
# @see https://stackoverflow.com/a/8080887
ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

# Include Default variables
include make/base.env

# Include info about environment
-include make/.env

# Common variable to pass arbitrary options to targets
ARGS?= 

# bash colors
RED:=\033[0;31m
GREEN:=\033[0;32m
YELLOW:=\033[0;33m
NO_COLOR:=\033[0m

# @see https://www.thapaliya.com/en/writings/well-documented-makefiles/
.DEFAULT_GOAL:=help

include make/*.mk

# Note:
# We are NOT using $(MAKEFILE_LIST) but defined the required make files manually via "Makefile .make/*.mk"
# because $(MAKEFILE_LIST) also contains the .env files AND we cannot force the order of the files
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\n\033[1mUsage:\033[0m\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-40s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' Makefile make/*.mk