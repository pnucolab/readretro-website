FROM node:19-alpine
RUN mkdir /ecolab-web
ADD build /ecolab-web/build
ADD package.json /ecolab-web/
WORKDIR /ecolab-web
RUN npm install