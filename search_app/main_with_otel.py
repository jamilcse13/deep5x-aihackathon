from fastapi import FastAPI, Request
from typing import List, Optional, Dict, Any
import time
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure the OTLP exporter to send data to the collector
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Create a FastAPI app instance
app = FastAPI(
    title="Product Search API",
    description="A simple API to search for products.",
    version="1.0.0"
)

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Define Prometheus metrics
REQUESTS = Counter("app_requests_total", "Total number of requests", ["endpoint", "method"])
LATENCY = Histogram("app_request_latency_seconds", "Request latency in seconds", ["endpoint"])

# Sample product data (in-memory database)
PRODUCTS = [
    {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 1200.00},
    {"id": 2, "name": "Mouse", "description": "Ergonomic wireless mouse", "price": 25.00},
    {"id": 3, "name": "Keyboard", "description": "Mechanical gaming keyboard", "price": 75.00},
    {"id": 4, "name": "Monitor", "description": "27-inch 4K monitor", "price": 300.00},
    {"id": 5, "name": "Webcam", "description": "1080p HD webcam", "price": 50.00},
    {"id": 6, "name": "LAPTOP", "description": "Case-insensitive test", "price": 1250.00}
]

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    REQUESTS.labels(endpoint=request.url.path, method=request.method).inc()
    LATENCY.labels(endpoint=request.url.path).observe(process_time)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

@app.get("/search", summary="Search for products", response_model=List[Dict[str, Any]])
async def search_products(name: Optional[str] = None):
    """
    Search for products by name.

    - If the **name** query parameter is provided, it returns a list containing
      the product(s) matching that name (case-insensitive).
    - If the **name** is not provided or no product matches the name,
      it returns the entire list of products.
    """
    # Create a span for the search operation
    with tracer.start_as_current_span("search_products") as span:
        span.set_attribute("search.name", name if name else "all")
        
        if name:
            # Perform a case-insensitive search
            filtered_products = [
                product for product in PRODUCTS
                if product.get("name", "").lower() == name.lower()
            ]
            span.set_attribute("search.result_count", len(filtered_products))
            
            if filtered_products:
                return filtered_products

        # If no name was provided, or if name was provided but no match was found, return all products
        span.set_attribute("search.result_count", len(PRODUCTS))
        return PRODUCTS

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancer"""
    return {"status": "healthy"}
