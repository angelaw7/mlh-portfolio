#! /usr/bin/bash

sleep 5

domain="https://angela-mlh-portfolio.herokuapp.com/"

while read endpoint; do
  response=$(curl -s -o /dev/null -w "%{http_code}" $domain$endpoint)
  if [[ $response == "200" ]]; then
    echo "$domain$endpoint | Success"
  else
    echo "$domain$endpoint | Error"
    exit 1
  fi
done < endpoint.txt
exit 0
