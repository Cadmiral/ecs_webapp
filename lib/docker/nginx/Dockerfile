FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install nginx 
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80
CMD /usr/sbin/nginx && tail -f /dev/null
