FROM nginx:alpine
# Static CK Service preview (Badkamergevoel?). Railway provides $PORT.
COPY . /usr/share/nginx/html
RUN rm -f /usr/share/nginx/html/Dockerfile /usr/share/nginx/html/.dockerignore
CMD ["/bin/sh","-c","sed -i \"s/listen\\s*80;/listen ${PORT:-80};/\" /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
