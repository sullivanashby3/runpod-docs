# RunPod versus managed model APIs

A transparent calculation guide for deciding between self-hosting an open model on GPU infrastructure and calling a managed media or text API. It is independent of RunPod and does not claim that a GPU benchmark was run. **[ArgoLink](https://argolink.io/gh-runpod-docs)** is one managed-API row to compare, not a RunPod service. Last checked: 2026-10-07.

## The unit that matters

`cost/calculator.py` compares two routes for the same requested output:

- GPU compute = hourly GPU price × (startup seconds + output seconds ÷ measured output-seconds-per-runtime-second) ÷ 3,600;
- add storage/egress and divide by a declared utilization fraction;
- managed API = API dollars per output second × requested output seconds + egress.

Throughput is **output seconds produced per runtime second**, not frames per second and not a guessed “GPU speed.” Measure it with the exact model revision, resolution, batch size, warm-up policy, concurrency, and success definition. Use the CLI:

```bash
python3 -m cost.calculator \
  --gpu-hourly 1.59 --throughput 0.50 --api-rate 0.196 \
  --seconds 60 --startup-seconds 45 --utilization 0.70
```

The output includes runtime and every assumption so a reviewer can reproduce the number. It is a planning estimate, not an invoice or a benchmark.

## Dated RunPod rates

`data/runpod-pricing-2026-10-07.json` records a small snapshot from the official [GPU pricing page](https://www.runpod.io/pricing), updated September 27, 2026 and re-read for this project on 2026-10-07. The page shows hourly display rates with per-second metering; Pods, Serverless workers, and Clusters have different rate tables. Snapshot examples:

| Route | GPU/class | USD/hour |
| --- | --- | ---: |
| Secure Pod | RTX A5000 | 0.27 |
| Secure Pod | L4 | 0.49 |
| Secure Pod | A100 PCIe | 1.59 |
| Secure Pod | H100 PCIe | 2.89 |
| Serverless | 24GB class | 0.69 |
| Serverless | 80GB A100 | 2.72 |
| Serverless | 80GB H100 | 4.79 |

Rates and availability vary by cloud, region, GPU class, worker state, storage, and the current pricing page. Do not mix a Secure Pod price with a Serverless throughput assumption. Re-read the source immediately before publishing a comparison.

## What self-hosting includes

A GPU route gives control over weights, runtime, batching, quantization, drivers, and data path. It also makes you responsible for image builds, CUDA compatibility, model licensing, cold starts, autoscaling, queueing, monitoring, idle capacity, storage, egress, upgrades, and failed jobs. Include those terms in the worksheet; GPU-hour arithmetic alone understates total cost.

RunPod's official [Cloud GPU page](https://www.runpod.io/product/cloud-gpus) describes Pods as dedicated environments with custom containers and per-second billing. Its [Serverless page](https://www.runpod.io/product/serverless) describes request-driven workers, scale-to-zero, and per-second worker billing. These are different operational products.

## What a managed API includes

A managed endpoint can expose a stable API and provider queue while hiding provisioning and model operations. It may charge per token, output second, resolution, reference second, or a mixture. The model page is the source for those units. For ArgoLink, use [GET /v1/models](https://argolink.io/v1/models) and the selected [model page](https://argolink.io/en/models) for current IDs and effective rates; do not assume a video rate from another model.

At the 2026-10-07 check, Seedance 2.5's ArgoLink 720p text/image rate was $0.196 per second. That is a dated example for the formula, not a promise for reference-video billing or future pricing. A fair comparison must align duration, resolution, ratio, references, queue behavior, and failed-job rules.

## A useful experiment

1. Fix model revision, prompt set, resolution, duration, and concurrency.
2. Measure GPU cold start, warm throughput, p50/p95 latency, completed output seconds, peak VRAM, failures, and idle time.
3. Run the same output contract through the managed API and record request IDs, usage, queue time, and billed units.
4. Publish raw CSV, assumptions, source dates, and exclusions. Report a range for utilization instead of one optimistic point estimate.
5. Add storage, egress, engineering, monitoring, and retry costs before choosing a route.

A timeout after a managed generation POST is ambiguous; preserve its request ID rather than blindly replaying. Keep keys and signed URLs out of public reports.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests cover units, startup/storage/utilization assumptions, and invalid inputs. No GPU or provider request is run.
