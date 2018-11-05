FROM fedora:latest

RUN dnf install -y 'dnf-command(builddep)'
RUN dnf builddep -y kernel
