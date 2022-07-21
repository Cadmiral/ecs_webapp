FROM alpine:3.14
RUN  apk update && apk upgrade && \
     apk add apache2 && \
     apk add apache2-proxy && \
     apk add apache2-ssl && \
     rm -rf /var/cache/apk/*

COPY httpd.conf /etc/apache2/httpd.conf

EXPOSE 3000
CMD  [ "/usr/sbin/httpd", "-D", "FOREGROUND"]
