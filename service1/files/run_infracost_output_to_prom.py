import json
import requests
from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
import os

KEPTN_PROJECT = os.getenv("KEPTN_PROJECT", "NULL")
KEPTN_SERVICE = os.getenv("KEPTN_SERVICE", "NULL")
KEPTN_STAGE = os.getenv("KEPTN_STAGE", "NULL")
INFRACOST_API_KEY = os.getenv("INFRACOST_API_KEY", "")

PROM_LABELS = [
    "ci_platform",
    "keptn_project",
    "keptn_service",
    "keptn_stage"
]

INCLUDED_FIELDS = [
    "totalHourlyCost",
    "totalMonthlyCost",
    "diffTotalHourlyCost",
    "diffTotalMonthlyCost"
]

plan_file = open("/keptn/files/plan.json")

headers = {
    "x-api-key": INFRACOST_API_KEY
}

payload = {
    "format": "json",
    "ci-platform": "keptn"
}

print("Retrieving Costs from Infracost API")
api_response = requests.post(url="https://pricing.api.infracost.io/breakdown",
  headers=headers,
  data=payload,
  files={'path': plan_file})


print(api_response.status_code)
print(api_response.text)

plan_file.close()

response_json = api_response.json()

##########################
# PUSH METRICS TO PROM   #
##########################
print("Pushing Metrics to Prometheus")

reg = CollectorRegistry()

for field in response_json:
    print(field)
    if field in INCLUDED_FIELDS:
      metric_value = response_json[field]
      print(f"Got value: {metric_value} for metric: {field}")
      g = Gauge(name=f"keptn_infracost_{field}", documentation='docs', registry=reg, labelnames=PROM_LABELS)
      g.labels(
          ci_platform="keptn",
          keptn_project=KEPTN_PROJECT,
          keptn_service=KEPTN_SERVICE,
          keptn_stage=KEPTN_STAGE,
      ).set(metric_value)

push_to_gateway(gateway='prometheus-pushgateway.monitoring.svc.cluster.local:9091',job='jes_infracost', registry=reg)

# Give Prometheus time to scrape the push gateway. Sleep for 1 minute
print("Give enough time to gather metrics. Sleeping for 1min")
time.sleep(60)
