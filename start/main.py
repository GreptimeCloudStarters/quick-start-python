#!/usr/bin/env python

import time
import argparse
import base64
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry import metrics
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter


def main():
    parser = argparse.ArgumentParser(
                        prog='greptime-cloud-quick-start-python',
                        description='Quick start Python demo for greptime cloud')

    parser.add_argument('-host', required=True, help='The host address of the GreptimeCloud service')
    parser.add_argument('-db', '--database', required=True, help='The database of the GreptimeCloud service')
    parser.add_argument('-u', '--username', required=True, help='The username of the database')
    parser.add_argument('-p', '--password', required=True, help='The password of the database')
    args = parser.parse_args()
    host = args.host
    db = args.database
    username = args.username
    password = args.password

    auth = f"{username}:{password}"
    b64_auth = base64.b64encode(auth.encode()).decode("ascii")

    # Service name is required for most backends
    resource = Resource(attributes={
        SERVICE_NAME: "quick-start-python"
    })

    endpoint = f"https://{host}/v1/otlp/v1/metrics"

    exporter = OTLPMetricExporter(
        endpoint=endpoint,
        headers={"Authorization": f"Basic {b64_auth}", "x-greptime-db-name": db},
        timeout=5)
    # exporter = ConsoleMetricExporter()
    metric_reader = PeriodicExportingMetricReader(exporter, 2000)
    provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

    # Sets the global default meter provider
    metrics.set_meter_provider(provider)
    configuration = {
        "system.memory.usage": ["used", "free", "cached"],
        "system.cpu.time": ["idle", "user", "system", "irq"],
        "process.runtime.memory": ["rss", "vms"],
        "process.runtime.cpu.time": ["user", "system"],
    }
    SystemMetricsInstrumentor(config=configuration).instrument()

    print("Sending metrics...")

    while True:
        time.sleep(2)

if __name__ == "__main__":
    main()
    