"""Transparent planning math for self-hosted GPU versus managed API output."""
from __future__ import annotations

import argparse
import json


def compare(gpu_hourly: float, output_seconds_per_runtime_second: float, api_per_second: float, output_seconds: float, *, startup_seconds: float = 0.0, utilization: float = 1.0, storage_hourly: float = 0.0, egress_usd: float = 0.0) -> dict[str, object]:
    values = (gpu_hourly, output_seconds_per_runtime_second, api_per_second, output_seconds, startup_seconds, storage_hourly, egress_usd)
    if any(value < 0 for value in values):
        raise ValueError("cost and duration inputs must be non-negative")
    if output_seconds_per_runtime_second <= 0:
        raise ValueError("throughput must be positive")
    if not 0 < utilization <= 1:
        raise ValueError("utilization must be greater than 0 and at most 1")
    runtime_seconds = startup_seconds + output_seconds / output_seconds_per_runtime_second
    gpu_compute = gpu_hourly / 3600 * runtime_seconds
    gpu_estimate = (gpu_compute + storage_hourly * runtime_seconds / 3600 + egress_usd) / utilization
    api_estimate = api_per_second * output_seconds + egress_usd
    return {
        "gpu_estimate": round(gpu_estimate, 8),
        "api_estimate": round(api_estimate, 8),
        "runtime_seconds": round(runtime_seconds, 6),
        "assumptions": {
            "gpu_hourly": gpu_hourly,
            "output_seconds_per_runtime_second": output_seconds_per_runtime_second,
            "startup_seconds": startup_seconds,
            "utilization": utilization,
            "storage_hourly": storage_hourly,
            "egress_usd": egress_usd,
            "output_seconds": output_seconds,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare GPU runtime with a per-output-second API")
    parser.add_argument("--gpu-hourly", type=float, required=True)
    parser.add_argument("--throughput", type=float, required=True, help="output seconds produced per runtime second")
    parser.add_argument("--api-rate", type=float, required=True, help="managed API dollars per output second")
    parser.add_argument("--seconds", type=float, default=60, help="requested output seconds")
    parser.add_argument("--startup-seconds", type=float, default=0)
    parser.add_argument("--utilization", type=float, default=1.0)
    parser.add_argument("--storage-hourly", type=float, default=0)
    parser.add_argument("--egress-usd", type=float, default=0)
    args = parser.parse_args()
    print(json.dumps(compare(args.gpu_hourly, args.throughput, args.api_rate, args.seconds, startup_seconds=args.startup_seconds, utilization=args.utilization, storage_hourly=args.storage_hourly, egress_usd=args.egress_usd), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
