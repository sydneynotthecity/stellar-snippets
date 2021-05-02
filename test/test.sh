#!/bin/bash

# run automated tests
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"recipe", "expires_in": 30, "snippet":"1 apple"}' http://localhost:5000/snippets

curl http://localhost:5000/snippets/recipe

sleep 60

curl http://localhost:5000/snippets/recipe
