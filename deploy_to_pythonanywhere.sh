#!/bin/bash

set -e

# Install dependencies and trigger deployment via PythonAnywhere API
pip install -r requirements.txt
curl "https://www.pythonanywhere.com/api/v0/user/${PYTHONANYWHERE_USERNAME}/webapps/${PYTHONANYWHERE_WEBAPP_DOMAIN}/reload/" \
  --request POST \
  --header "Authorization: Token ${PYTHONANYWHERE_API_TOKEN}"

echo "Deployment to PythonAnywhere completed successfully."
