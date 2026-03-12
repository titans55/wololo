FROM node:12-slim AS build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
COPY gameConfig.json /gameConfig.json

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist/ng-wololo /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
