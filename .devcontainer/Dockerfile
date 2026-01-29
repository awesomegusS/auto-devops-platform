# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.9

# Remove Yarn APT source to avoid unsigned repo errors during feature installs.
RUN if [ -f /etc/apt/sources.list.d/yarn.list ]; then rm /etc/apt/sources.list.d/yarn.list; fi
