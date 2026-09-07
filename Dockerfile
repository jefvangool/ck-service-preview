FROM node:20-alpine
# ckservice.be — static reference site + lead relay (see server.js). No npm deps.
WORKDIR /app
COPY . /app
RUN rm -f /app/Dockerfile /app/.dockerignore /app/transform.py && \
    rm -rf /app/.git /app/blog.html /app/blog-post.html
ENV NODE_ENV=production
EXPOSE 80
CMD ["node", "server.js"]
