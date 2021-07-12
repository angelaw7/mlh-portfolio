#! /usr/bin/bash

domain="https://www.angela-mlh.duckdns.org/"

while read endpoint; do
  response=$(curl -s -o /dev/null -w "%{http_code}" $domain$endpoint)
  if [[ $response == "200" ]]; then
    echo "$domain$endpoint | Success"
  elif [[ $endpoint == "login" || "register" ]] && [[ $response == "501" ]]; then
    echo "$domain$endpoint | Not yet implemented"
  else
    echo "$domain$endpoint | Error"
    exit 1
  fi
done < endpoint.txt
exit 0
