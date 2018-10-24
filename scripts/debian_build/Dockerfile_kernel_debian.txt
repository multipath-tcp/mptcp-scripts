FROM debian:stable

RUN printf "\ndeb-src http://deb.debian.org/debian stable main\n \
deb-src http://security.debian.org/debian-security stable/updates main\n \
deb-src http://deb.debian.org/debian stable-updates main\n" >> /etc/apt/sources.list

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get build-dep -y linux && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y git
