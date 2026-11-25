# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. (MV2, mv2@munimtech.com). Made with AI agents working in MV2's name.
"""Run the tm2 census (PREREG_q81.md) and write per-n results as they complete.

python census_job.py --mode high --nlo 5 --nhi 400 --workers 2 --hours 4 --out /out/high
"""
import argparse
import json
import os
import time

import tm2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["all", "high"], required=True)
    ap.add_argument("--nlo", type=int, default=5)
    ap.add_argument("--nhi", type=int, required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--hours", type=float, default=4.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    per_n = open(os.path.join(a.out, "per_n.jsonl"), "w")

    def on_n_done(d):
        per_n.write(json.dumps(d, sort_keys=True) + "\n")
        per_n.flush()

    t0 = time.time()
    done, note = tm2.run(a.nlo, a.nhi, a.mode, workers=a.workers, seconds=a.hours * 3600,
                         on_n_done=on_n_done)
    per_n.close()
    rep = tm2.report(done, a.nlo, a.nhi, a.mode, note, time.time() - t0)
    with open(os.path.join(a.out, "report.txt"), "w") as f:
        f.write(rep + "\n")
    with open(os.path.join(a.out, "summary.json"), "w") as f:
        json.dump({"mode": a.mode, "nlo": a.nlo, "nhi": a.nhi, "note": note,
                   "complete_to": tm2.complete_prefix(done, a.nlo, a.nhi),
                   "seconds": round(time.time() - t0),
                   "hits": [dict(h, n=n) for n in sorted(done) for h in done[n]["hits"]],
                   "anomalies": {n: done[n]["anomalies"] for n in done if done[n]["anomalies"]},
                   "unresolved": {n: done[n]["unresolved"] for n in done
                                  if done[n]["unresolved"]},
                   "bound": {n: done[n]["bound"] for n in sorted(done)},
                   "searched": {n: done[n]["searched"] for n in sorted(done)},
                   "pairs": {n: done[n]["pairs"] for n in sorted(done)}},
                  f, sort_keys=True, indent=1)
    print(rep)


if __name__ == "__main__":
    main()
