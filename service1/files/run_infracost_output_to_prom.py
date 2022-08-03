import json
import requests
from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway

print("Hello world...")
reg = CollectorRegistry()

g = Gauge(name='dummy_python_metrics', registry=reg, labelnames=["label1", "label2"],labelvalues=["val1","val2"])
g.set(99)
push_to_gateway(gateway='prometheus-pushgateway.monitoring.svc.cluster.local:9091',job='batchA', registry=reg)
