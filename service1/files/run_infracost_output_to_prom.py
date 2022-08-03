import json
import requests
from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway

print("Hello world...")
reg = CollectorRegistry()

g = Gauge(name='dummy_python_metrics', registry=reg, labelnames=["label1", "label2"],labelvalues=["val1","val2"])
g.set(99)
push_to_gateway(gateway='prometheus-pushgateway.monitoring.svc.cluster.local:9091',job='batchA', registry=reg)

exit()


api_response = requests.post()

#!/bin/sh
echo "hello world"
#printenv
# env var from secret
INFRACOST_OUTPUT=$(curl -X POST -H "x-api-key: $INFRACOST_API_KEY" -F "ci-platform=keptn" \
-F "path=@/keptn/files/plan.json" \
https://pricing.api.infracost.io/diff)
echo "Printing Infracost Output..."
echo $INFRACOST_OUTPUT
