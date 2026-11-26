# Results Q81: graded against PREREG_q81.md, and why this study stops here

Written 2026-11-26. MV2, Munim, Inc. Made with AI agents working in MV2's name; no human
expert has checked it. Text CC BY 4.0.

## What ran

Only the short gate probe `test_probe_q81a.py` has run so far (2026-11-25 23:30 UTC, Windows
test gate, 6 worker processes, about 200 s per mode). The compete job `tm2-census-v1` is still
waiting for compute. The probe output, copied from the gate log:

```
Q81 mode=all n=5..60 complete_to=30 pool6 deadline t=200s
pairs=4056 searched=4056 (rest excluded by bound B1)
n=5 hits=[R(1, 3) W(6, 8) c1 m1 gw0 dil1] anom=[] unres=[]
n=8 hits=[R(2, 3) W(11, 13) c1 m1 gw0 dil0] anom=[] unres=[]
NEW(not Thm5.1, not dilate, not the n=8 sporadic)=0 []
max bound/(n ln n)=17.175 at n=24 (bound 1310)
Q81 mode=high n=5..200 complete_to=38 pool6 deadline t=231s
pairs=2108 searched=2108 (rest excluded by bound B1)
NEW(not Thm5.1, not dilate, not the n=8 sporadic)=0 []
max bound/(n ln n)=22.152 at n=34 (bound 2656)
```

So with no cap on the inserted speeds, the only tight two-entry modifications for 5 <= n <= 30
are the dilate {2, 4, 6, 8} (n = 5) and Goddyn and Wong's {1, 4, 5, 6, 7, 11, 13} (n = 8). There
are none with r1, r2 > (n-1)/2 for n <= 38.

## Grades

| prediction | grade |
|---|---|
| P1: for 9 <= n <= N_A only n = 74 is tight | true as far as it was reached (N_A = 30, no tight set) |
| P2: every high-mode hit comes from Theorem 5.1 | true as far as it was reached (n <= 38, no hits) |
| P3: no anomaly | true |
| P4: fewer than 1% of pairs R need the inner search | **false**: bound B1 excluded no pair at all (4056 of 4056 searched) |
| P5: B(n)/(n ln n) < 10 | **false**: 17.2 at n = 24 (all mode), 22.2 at n = 34 (high mode) |

P4 and P5 failed because the uncovered set U is made of very short pieces, so bound B1 allows
slow inserted speeds up to about 2n^2. The search is still finite and exact, but it costs about
n^5 operations, far more than we expected.

## Scooped: this study stops

A search on 2026-11-26 found two pieces of work that already answer more than this study could:

- [Alswek123/lonely-runner-two-replacements](https://github.com/Alswek123/lonely-runner-two-replacements)
  (one commit, about 2026-11-26 00:30 UTC; draft paper prepared with OpenAI Codex, unrefereed)
  reports a census of every deletion pair for 8 <= n <= 300 (4,455,065 pairs). Each pair's
  speed range comes from a rational interval bound. Only the known sets at n = 8, 74 and 284
  are tight. The draft also claims bounds u = O(n log log n) and w = O(n log n) for the two
  inserted speeds (Zhang's Question 8.2). Its census contains our n <= 30 result many times over.
- [the-omega-institute/trureturing issue 29259](https://github.com/the-omega-institute/trureturing/issues/29259)
  (2026-11-11) records a reviewer-approved prose argument that every tight two-entry
  modification with r1, r2 > (n-1)/2 comes from Theorem 5.1 (the last sentence of Question 8.1).
  It was not yet formalised in Lean.

Our census agrees with theirs where both reach. It adds nothing new, so we make no claim from
it. If `tm2-census-v1` runs, its output will be recorded here only as an independent re-check of
the published census, using a different method.

## Credits

The questions are Yuhan Zhang's ([arXiv:2608.13599](https://arxiv.org/abs/2608.13599)).
Theorem 5.1 is Goddyn and Wong's. The census to n = 300 is Alswek123's.
