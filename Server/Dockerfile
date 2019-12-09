FROM php:apache
ENV URL=ai-server

RUN docker-php-ext-install sockets
RUN docker-php-ext-install mysqli

COPY ./data /var/www/html
EXPOSE 80