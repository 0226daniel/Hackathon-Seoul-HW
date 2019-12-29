FROM node:lts

WORKDIR /var/www/app

COPY package*.json /var/www/app/

RUN npm install

COPY . /var/www/app/

CMD ["npm", "start"]