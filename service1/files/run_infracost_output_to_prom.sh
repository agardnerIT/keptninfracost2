#!/bin/sh
echo "hello world"
#printenv
# env var from secret
INFRACOST_OUTPUT=$(curl -X POST -H "x-api-key: $INFRACOST_API_KEY" -F "ci-platform=keptn" \
-F "path=@/keptn/files/plan.json" \
https://pricing.api.infracost.io/diff)
echo "Printing Infracost Output..."
echo $INFRACOST_OUTPUT
