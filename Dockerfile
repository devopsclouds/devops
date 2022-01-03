FROM centos:latest

RUN yum -y update

RUN yum -y install wget

RUN yum -y install httpd

RUN yum -y install git

WORKDIR /opt

COPY hi.txt .

WORKDIR /tmp
COPY hi.txt .

COPY hello.txt /opt

COPY welcome.txt .

ADD apache-maven-3.8.4-bin.tar.gz /opt

COPY sonarqube-8.9.6.50800.zip /opt

ADD https://maven.apache.org/download.cgi .

ENV name chintu



#COPY https://maven.apache.org/download.cgi .

CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]

CMD echo "$name"


ENTRYPOINT ["/bin/echo", "Welcome, $name"]

#ENTRYPOINT ["/bin/sh","-c", "echo $name"]
