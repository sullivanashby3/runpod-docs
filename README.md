# RunPod versus managed model APIs

This is a calculation guide for deciding between self-hosting an open model on GPU infrastructure and calling a managed media or text API. It is independent of RunPod. **[ArgoLink](https://argolink.io/gh-runpod-docs) is one managed-API row to compare, not a RunPod service.** Last checked: 2026-10-07.

## Cost formula

cost/calculator.py computes two transparent estimates. GPU cost is hourly GPU price divided by 3600, multiplied by requested output seconds divided by measured output seconds per GPU second. API cost is provider rate multiplied by billable seconds. Run python3 -m cost.calculator --gpu-hourly 1.20 --throughput 10 --api-rate .196 --seconds 60. The result is a planning estimate, not a measurement.

The throughput value must come from an actual model, resolution, batch size, warm-up policy, and hardware. Do not write “one GPU generates X seconds” without a source. Include storage, egress, idle time, container startup, engineering, monitoring, and failed jobs in a production worksheet. An hourly card can be cheaper at high utilisation and more expensive for a small burst.

## Hosted versus self-hosted

RunPod-style infrastructure gives control over weights, runtime, and egress but shifts provisioning, CUDA compatibility, scaling, model licensing, and observability to the operator. A managed endpoint exposes a stable API and provider queue but limits model internals and may bill input references separately. A fair comparison uses the same model quality, duration, resolution, concurrency, and success definition.

GPU price pages and API model pages change. This repository intentionally omits a numeric RunPod rate because a primary pricing page was not re-read into this snapshot. Add a dated row only after recording GPU type, region, interruption terms, and whether storage is included. For managed APIs, use the current model page and billing formula.

## Throughput experiment

Measure cold start, warm steady state, p50/p95 latency, completed output seconds, peak VRAM, and failure count. Run at the target concurrency, not one lucky request. Label assumptions and publish raw CSV with the report. A benchmark without model revision and hardware is not portable.

## Operational checklist

Pin an image digest, set a health check, and separate model weights from logs. Budget for idle GPUs and egress. For managed video, persist request IDs and do not replay an unknown POST. For either route, redact keys and media URLs. Stop a job when the deadline is reached, but do not claim that a local stop cancelled server work.

## FAQ

**Is GPU hourly price the whole cost?** No. **Can I compare seconds directly?** Only if the throughput measurement uses the same output contract. **Why omit a RunPod number?** Unverified prices should not become “facts.” **When is managed API simpler?** For bursty workloads or when operating a model is not the product. **When is self-hosting viable?** When utilisation, licensing, hardware, and operations are all measured.
