#!/bin/bash

ssh root@167.99.31.178 'rm -r ~/bookstore/bookstore-api'
scp -r ../bookstore-api root@167.99.31.178:~/bookstore

ssh root@167.99.31.178 'docker stop bookstore-api'
ssh root@167.99.31.178 'docker rm bookstore-api'

ssh root@167.99.31.178 'docker build -t bookstore-build ~/bookstore/bookstore-api'
ssh root@167.99.31.178 'docker run -idt -e MODULE_NAME="run" -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 --name=bookstore-api bookstore-build'

ssh root@167.99.31.178 'docker stop api-nginx'
ssh root@167.99.31.178 'docker rm api-nginx'

ssh root@167.99.31.178 'docker build -t bookstore-nginx ~/bookstore/bookstore-api/nginx-https'
ssh root@167.99.31.178 'docker run -idt --name=api-nginx -p 80:80 -p 443:443 -e DOMAIN=167.99.31.178 -e EMAIL=kueijunghu@gmail.com bookstore-nginx'