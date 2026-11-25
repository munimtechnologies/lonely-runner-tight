# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. (MV2, mv2@munimtech.com). Made with AI agents working in MV2's name.
"""tm2: exact census of tight two-entry modifications of [n-1] (Lonely Runner Conjecture).

Setting (Zhang, arXiv:2608.13599, Question 8.1). For n >= 5 and 1 <= r1 < r2 <= n-1 let
S = [n-1] minus {r1, r2} and V = S union {w1, w2} with w1 != w2 both >= n. V has n-1 speeds;
it is *tight* when its loneliness ML(V) = max_t min_v ||v t|| equals 1/n.

ML(V) <= 1/n  iff  the closed arcs A_v = {t : ||v t|| <= 1/n} (v in V) cover the circle.

Why the search over w1, w2 is finite with NO cap on the inserted speeds (see PREREG_q81.md):
  U = circle minus the arcs of S is a finite union of open intervals (pieces).
  (B1) If a speed w has w * n * l >= 2n - 2 for a piece of length l, that piece contains a whole
       open gap of w (gap length (n-2)/(n w), period 1/w). If BOTH inserted speeds did so for the
       longest piece, each one's full gap would have to sit inside one closed arc of the other
       (a connected set covered by disjoint closed arcs lies in one of them), giving
       w2 <= 2 w1/(n-2) and w1 <= 2 w2/(n-2), impossible for n >= 5. So one inserted speed,
       ws, satisfies n <= ws < (2n-2)/(n l_max).
  (B2) Given ws, every piece of U minus A_ws (a connected open set) lies inside ONE closed arc of
       the other speed wf; with lam the longest such piece, wf <= 2/(n lam), and for that piece
       (c, d) there is an integer k with (k - 1/n)/c <= wf <= (k + 1/n)/d.
  If U minus A_ws is empty, S + {ws} already covers: n-2 speeds with ML <= 1/n, which the Lonely
  Runner Conjecture forbids; this is reported as an anomaly and never silently skipped.
All arithmetic deciding tightness is exact (Fractions / integers). The sweep that finds U compares
floats, which is exact here (see all_arcs). Every hit is re-checked by two independent integer
checkers (is_cover, ml_at_least) that share no code with the sweep.
"""
import json
import math
import time
from fractions import Fraction as Fr
from math import gcd

HALF = Fr(1, 2)


# ----------------------------------------------------------------- independent exact checkers

def is_cover(speeds, n):
    """True iff the closed arcs {t : ||v t|| <= 1/n}, v in speeds, cover the circle.
    Criterion: the union is everything iff for every right endpoint e = (kn+1)/(nv) some arc
    contains [e, e + eps), i.e. frac(u e) in [0, 1/n) or [1 - 1/n, 1). Integer arithmetic only."""
    sp = list(speeds)
    for v in sp:
        b = n * v
        for k in range(v):
            a = k * n + 1
            for u in sp:
                r = (u * a) % b
                if n * r < b or n * r >= (n - 1) * b:
                    break
            else:
                return False
    return True


def ml_at_least(speeds, n):
    """True iff some time t has ||v t|| >= 1/n for every v (so ML >= 1/n). The set of such t is
    closed; if non-empty its boundary points are arc endpoints (kn +- 1)/(nv), which we test."""
    sp = list(speeds)
    for v in sp:
        b = n * v
        for k in range(v):
            for a in (k * n + 1, k * n + n - 1):
                ok = True
                for u in sp:
                    r = (u * a) % b
                    if n * min(r, b - r) < b:
                        ok = False
                        break
                if ok:
                    return True
    return False


def is_tight(speeds, n):
    return is_cover(speeds, n) and ml_at_least(speeds, n)


# ------------------------------------------------------------- Goddyn-Wong Theorem 5.1 test

def gw_criterion(n, r, m):
    """Goddyn-Wong condition for accelerating r by m (Zhang Thm 5.1): gcd(r, b) > 1 for every
    integer b in [n - r, m (n - r) - 1]. m = 1 (no acceleration) always passes."""
    if m == 1:
        return True
    s = n - r
    return all(gcd(r, b) > 1 for b in range(s, m * s))


def is_thm51(n, V):
    """True iff V = {m_r * r : r in [n-1]} for multipliers m_r >= 1 that all satisfy the
    Goddyn-Wong criterion (bipartite perfect matching r -> m_r r in V)."""
    V = sorted(V)
    if len(V) != n - 1:
        return False
    adj = {r: [t for t in V if t % r == 0 and gw_criterion(n, r, t // r)] for r in range(1, n)}
    match = {}

    def aug(r, seen):
        for t in adj[r]:
            if t in seen:
                continue
            seen.add(t)
            if t not in match or aug(match[t], seen):
                match[t] = r
                return True
        return False

    for r in sorted(range(1, n), key=lambda x: len(adj[x])):
        if not aug(r, set()):
            return False
    return True


# ------------------------------------------------------------------------- the census engine

def all_arcs(n):
    """Closed arcs {t : ||v t|| <= 1/n} that meet [0, 1/2], for v = 1..n-1, as tuples
    (L_float, R_float, v, L_num, R_num, den) with L = L_num/den, R = R_num/den, den = n v,
    sorted by L. The floats compare exactly: every endpoint is p/q with q <= n^2, so distinct
    endpoints differ by at least 1/n^4 (> 1e-12 for n <= 1000), far above double rounding, and
    Python's int/int division is correctly rounded, so equal rationals give equal doubles."""
    out = []
    for v in range(1, n):
        den = n * v
        k = 0
        while True:
            ln = k * n - 1
            if 2 * ln > den:
                break
            rn = k * n + 1
            out.append((ln / den, rn / den, v, ln, rn, den))
            k += 1
    out.sort(key=lambda a: a[0])
    return out


def uncovered(arcs, r1, r2):
    """Pieces (a, b) of [0, 1/2] not covered by the arcs of S = [n-1] minus {r1, r2}, exact.
    Pieces are open, except that a piece ending at 1/2 contains 1/2. By the symmetry t -> -t
    this half circle decides everything."""
    curf, curn, curd = 0.0, 0, 1
    gaps = []
    for lf, rf, v, ln, rn, den in arcs:
        if v == r1 or v == r2:
            continue
        if lf > curf:
            gaps.append((Fr(curn, curd), Fr(ln, den)))
        if rf > curf:
            curf, curn, curd = rf, rn, den
    if curf < 0.5:
        gaps.append((Fr(curn, curd), HALF))
    return gaps


def subtract(pieces, w, n):
    """Pieces minus the closed arcs of speed w (exact)."""
    out = []
    for a, b in pieces:
        x = a
        k = math.floor(w * a)
        while True:
            L = Fr(k * n - 1, n * w)
            if L >= b:
                break
            if L > x:
                out.append((x, L))
            R = Fr(k * n + 1, n * w)
            if R > x:
                x = R
            if x >= b:
                break
            k += 1
        if x < b:
            out.append((x, b))
    return out


def fits(pieces, w, n):
    """True iff every piece lies inside one closed arc of speed w."""
    inv = Fr(1, n)
    for c, d in pieces:
        k = math.floor(w * (c + d) / 2 + HALF)
        if w * c < k - inv or w * d > k + inv:
            return False
    return True


def classify_R(n, arcs, r1, r2, cap_ws=100000, cap_k=1000000):
    """All {w1, w2} (n <= w1 < w2) making ([n-1] minus {r1, r2}) + {w1, w2} cover the circle.
    Returns a dict with status 'excluded' (bound B1 leaves no slow speed >= n), 'searched',
    'anomaly_S_covers' or 'unresolved_ws'; hits; anomalies; unresolved count; bound = the
    largest inserted speed the bounds B1/B2 allow (an upper bound on any hit)."""
    rec = {"n": n, "R": [r1, r2], "hits": [], "anomalies": [], "unresolved": 0}
    U = uncovered(arcs, r1, r2)
    if not U:
        rec["status"] = "anomaly_S_covers"
        return rec
    lmax = max(b - a for a, b in U)
    ws_hi = math.ceil(Fr(2 * n - 2) / (n * lmax))  # slow speed: n <= ws < ws_hi
    rec["pieces"] = len(U)
    rec["ws_hi"] = ws_hi
    if ws_hi <= n:
        rec["status"] = "excluded"
        return rec
    if ws_hi - n > cap_ws:
        rec["status"] = "unresolved_ws"
        return rec
    rec["status"] = "searched"
    inv = Fr(1, n)
    hits = set()
    bound = ws_hi - 1
    for ws in range(n, ws_hi):
        R1 = subtract(U, ws, n)
        if not R1:
            rec["anomalies"].append(ws)
            continue
        c, d = max(R1, key=lambda p: p[1] - p[0])
        lam = d - c
        kmax = math.floor((c + d) / (n * lam))
        bound = max(bound, math.floor(2 / (n * lam)))
        if kmax > cap_k:
            rec["unresolved"] += 1
            continue
        for k in range(0, kmax + 1):
            lo = max(n, math.ceil((k - inv) / c))
            hi = math.floor((k + inv) / d)
            for wf in range(lo, hi + 1):
                if wf != ws and fits(R1, wf, n):
                    hits.add((min(ws, wf), max(ws, wf)))
    rec["hits"] = sorted(hits)
    rec["bound"] = bound
    return rec


def high(n, r1):
    return 2 * r1 > n - 1


def census_task(task):
    """One (n, mode, r1) slice: every r2 in (r1, n-1]. mode 'high' keeps only r1 > (n-1)/2."""
    n, mode, r1 = task
    t0 = time.time()
    arcs = all_arcs(n)
    res = {"n": n, "r1": r1, "mode": mode, "pairs": 0, "excluded": 0, "searched": 0,
           "hits": [], "anomalies": [], "unresolved": [], "bound": 0}
    if mode == "high" and not high(n, r1):
        return res
    for r2 in range(r1 + 1, n):
        rec = classify_R(n, arcs, r1, r2)
        res["pairs"] += 1
        st = rec["status"]
        if st == "excluded":
            res["excluded"] += 1
            continue
        if st == "anomaly_S_covers" or rec["anomalies"]:
            res["anomalies"].append([r1, r2, st, rec["anomalies"][:5]])
        if st == "unresolved_ws" or rec["unresolved"]:
            res["unresolved"].append([r1, r2, st, rec.get("ws_hi"), rec["unresolved"]])
        if st == "searched":
            res["searched"] += 1
            res["bound"] = max(res["bound"], rec["bound"])
            for w1, w2 in rec["hits"]:
                V = sorted([v for v in range(1, n) if v not in (r1, r2)] + [w1, w2])
                g = 0
                for v in V:
                    g = gcd(g, v)
                res["hits"].append({"R": [r1, r2], "W": [w1, w2],
                                    "cover": is_cover(V, n), "ml_ge": ml_at_least(V, n),
                                    "thm51": is_thm51(n, V), "dilate": g > 1})
    res["seconds"] = round(time.time() - t0, 3)
    return res


def tasks_for(n, mode):
    lo = 1 if mode == "all" else (n - 1) // 2 + 1
    return [(n, mode, r1) for r1 in range(lo, n - 1)]


def merge(agg, res):
    n = res["n"]
    a = agg.setdefault(n, {"n": n, "pairs": 0, "excluded": 0, "searched": 0, "hits": [],
                           "anomalies": [], "unresolved": [], "bound": 0, "tasks_done": 0,
                           "seconds": 0.0})
    for key in ("pairs", "excluded", "searched"):
        a[key] += res[key]
    a["hits"] += res["hits"]
    a["anomalies"] += res["anomalies"]
    a["unresolved"] += res["unresolved"]
    a["bound"] = max(a["bound"], res["bound"])
    a["tasks_done"] += 1
    a["seconds"] += res.get("seconds", 0.0)


def run(n_lo, n_hi, mode, workers=2, seconds=None, on_n_done=None):
    """Run the census for n_lo <= n <= n_hi. Returns (per-n dict of complete n only, note)."""
    t0 = time.time()
    tasks, need = [], {}
    for n in range(n_lo, n_hi + 1):
        ts = tasks_for(n, mode)
        need[n] = len(ts)
        tasks += ts
    agg, done = {}, {}
    note = "serial"

    def take(res):
        merge(agg, res)
        n = res["n"]
        if agg[n]["tasks_done"] == need[n]:
            done[n] = agg[n]
            if on_n_done:
                on_n_done(agg[n])

    for n in need:
        if need[n] == 0:
            agg[n] = {"n": n, "pairs": 0, "excluded": 0, "searched": 0, "hits": [],
                      "anomalies": [], "unresolved": [], "bound": 0, "tasks_done": 0,
                      "seconds": 0.0}
            done[n] = agg[n]
    if workers > 1:
        try:
            import multiprocessing as mp
            ctx = mp.get_context("spawn")
            with ctx.Pool(workers) as p:
                note = "pool%d" % workers
                for res in p.imap_unordered(census_task, tasks, chunksize=1):
                    take(res)
                    if seconds and time.time() - t0 > seconds:
                        note += " deadline"
                        p.terminate()
                        break
            return done, note
        except Exception as e:  # pragma: no cover - depends on the host
            note = "serial(%s:%s)" % (type(e).__name__, str(e)[:60])
            agg.clear()
            done = {n: d for n, d in done.items() if need[n] == 0}
    for t in tasks:
        take(census_task(t))
        if seconds and time.time() - t0 > seconds:
            note += " deadline"
            break
    return done, note


def complete_prefix(done, n_lo, n_hi):
    """Largest N such that every n in [n_lo, N] is complete."""
    top = n_lo - 1
    for n in range(n_lo, n_hi + 1):
        if n not in done:
            break
        top = n
    return top


def report(done, n_lo, n_hi, mode, note, seconds):
    top = complete_prefix(done, n_lo, n_hi)
    lines = ["Q81 mode=%s n=%d..%d complete_to=%d %s t=%ds" % (mode, n_lo, n_hi, top, note,
                                                                round(seconds))]
    pairs = sum(done[n]["pairs"] for n in done)
    searched = sum(done[n]["searched"] for n in done)
    lines.append("pairs=%d searched=%d (rest excluded by bound B1)" % (pairs, searched))
    worst = None
    for n in sorted(done):
        d = done[n]
        if d["bound"] and n >= 3:
            ratio = d["bound"] / (n * math.log(n))
            if worst is None or ratio > worst[0]:
                worst = (ratio, n, d["bound"])
        if d["hits"] or d["anomalies"] or d["unresolved"]:
            hs = ";".join("R%s W%s c%d m%d gw%d dil%d" % (tuple(h["R"]), tuple(h["W"]),
                                                          h["cover"], h["ml_ge"], h["thm51"],
                                                          h["dilate"]) for h in d["hits"])
            lines.append("n=%d hits=[%s] anom=%s unres=%s" % (n, hs, d["anomalies"][:3],
                                                               d["unresolved"][:3]))
    nonthm = [(n, h["R"], h["W"]) for n in sorted(done) for h in done[n]["hits"]
              if not h["thm51"] and not h["dilate"] and not (n == 8 and h["W"] == [11, 13])]
    lines.append("NEW(not Thm5.1, not dilate, not the n=8 sporadic)=%d %s"
                 % (len(nonthm), nonthm[:5]))
    if worst:
        lines.append("max bound/(n ln n)=%.3f at n=%d (bound %d)" % worst)
    return "\n".join(lines)


def brute(n, wmax):
    """Independent brute force: every R and every n <= w1 < w2 <= wmax, checked by is_tight."""
    hits = []
    for r1 in range(1, n - 1):
        for r2 in range(r1 + 1, n):
            S = [v for v in range(1, n) if v not in (r1, r2)]
            for w1 in range(n, wmax + 1):
                for w2 in range(w1 + 1, wmax + 1):
                    V = S + [w1, w2]
                    if is_tight(V, n):
                        hits.append((n, (r1, r2), (w1, w2)))
    return hits


def dump(done):
    return json.dumps([done[n] for n in sorted(done)], sort_keys=True)
