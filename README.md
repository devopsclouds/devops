# Docker
virtualization software
developing and deploying application makes easier
packaging application with all the necessary dependencies ,configuration,system tools,runtime.
portable artifact easily shared and disributed.
lets take microservices app you will take top of base os  on that u will install packages, dependencies and everything to be packeed to create a docker image.
then u can start the container

# vm:
while vm u have to all install necessary functainoalities and services directly on their os on their local machine
installation process diferrent for each os environment.
many steps, where someting goes wrong.
if your app uses 10 services each developer need to install 10 services.


# dockerpause: 
when u pause the container the sig term send all the processs should be stopped
usecase: when container is not required now u can use pause command and when container is required in future then u can use unpause command.

# docker stop:
when u stop the container it will wait for 10 seconds to stop the process
# docker kill
when u kill the container it forecefully stop the container
usecase: when container is not responding this kill command will be use

# podman
Podman, like Docker, is an open source engine for deploying and managing containerized applications. Podman builds OCI-compliant containers from existing images or from Containerfiles and Dockerfiles.

The Podman engine was originally developed by Red Hat with the intention of providing a daemonless alternative to Docker. By employing a daemonless architecture, Podman seeks to remedy security concerns around Docker’s daemon-based process.

Additionally, Podman’s daemonless architecture grants it a truly rootless mode. Docker commands can be run by non-root users, but its daemon that executes those commands continues to run on root. Podman, instead, executes commands directly and avoids the need for root privileges.

podman is more secure then docker
