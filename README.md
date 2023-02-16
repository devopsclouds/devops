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


