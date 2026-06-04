from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import make_asgi_app
from fastapi import FastAPI
import os

def setup_telemetry(app: FastAPI, service_name: str):
    # Tracing
    resource = Resource.create(attributes={"service.name": service_name})
    trace_provider = TracerProvider(resource=resource)
    
    # Read OTLP endpoint from environment, fallback to Jaeger
    otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://jaeger:4317")
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    
    trace_provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(trace_provider)
    
    FastAPIInstrumentor.instrument_app(app)

    # Metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
