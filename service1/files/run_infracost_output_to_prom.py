import json
import requests
from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway

print("Hello world...")
reg = CollectorRegistry()

g = Gauge(name='dummy_python_metrics', registry=reg, labelnames=["label1", "label2"])
g.labels(label1="foo", label2="bar").set(99)

push_to_gateway(gateway='prometheus-pushgateway.monitoring.svc.cluster.local:9091',job='batchA', registry=reg)
