import json
import requests
from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
import os

print(os.environ)
exit()

KEPTN_PROJECT = "keptnProject1"
KEPTN_SERVICE = "keptnService1"
KEPTN_STAGE = "keptnStage1"

PROM_LABELS = [
    "ci_platform",
    "keptn_project",
    "keptn_service",
    "keptn_stage"
]

#INFRACOST_API_KEY = "G3ON2C4PP7vrLo4yS6Cj7YEwoNod3iTM"
print(f"Infracost API Key: {INFRACOST_API_KEY}")
# exit()
INCLUDED_FIELDS = [
    "totalHourlyCost",
    "totalMonthlyCost",
    "diffTotalHourlyCost",
    "diffTotalMonthlyCost"
]

plan_file = open("plan.json")

headers = {
    "x-api-key": INFRACOST_API_KEY
}

payload = {
    "format": "json",
    "ci-platform": "my-platform"
}

api_response = requests.post(url="https://pricing.api.infracost.io/breakdown",
  headers=headers,
  data=payload,
  files={'path': plan_file})

print(api_response.status_code)
print(api_response.text)

plan_file.close()

##########################
# PUSH METRICS TO PROM   #
##########################
reg = CollectorRegistry()

g = Gauge(name='dummy_python_metrics', documentation='docs', registry=reg, labelnames=["label1", "label2"])
g.labels(label1="foo", label2="bar").set(99)

push_to_gateway(gateway='prometheus-pushgateway.monitoring.svc.cluster.local:9091',job='batchA', registry=reg)
