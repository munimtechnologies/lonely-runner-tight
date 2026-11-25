# Pre-registration Q81: an uncapped census of tight two-entry modifications

Written 2026-11-25, before any census output existed (no code from this repository had been run
when this file was committed). MV2, Munim, Inc. Made with AI agents working in MV2's name.
Apache-2.0 (code), CC BY 4.0 (text).

## The question

Lonely Runner Conjecture: for every set V of n - 1 distinct positive integer speeds,
ML(V) = max_t min_{v in V} ||v t|| >= 1/n. V is *tight* when ML(V) = 1/n. The basic tight set is
[n-1] = {1, ..., n-1}. Describing all tight sets is Perarnau and Serra's Problem 1
([arXiv:2409.20160](https://arxiv.org/abs/2409.20160)).

Yuhan Zhang ([arXiv:2608.13599](https://arxiv.org/abs/2608.13599), v3, 18 Oct 2026) classified the
one-entry modifications of [n-1] and asks:

- **Question 8.1.** Classify the tight two-entry modifications ([n-1] minus {r1, r2}) union {w1, w2}.
  His census covers 8 <= n <= 140 with inserted speeds w <= 8n (only the two Goddyn-Wong sets are
  tight), so "the open cases are n > 140 or w2 > 8n". Follow-up: is every tight two-entry
  modification with r1, r2 > (n-1)/2 obtained from Theorem 5.1 (Goddyn-Wong multi-acceleration)?
- **Question 8.2.** Is max V = O(n log n), or polynomial in n, for tight modifications with
  |R| = |W| >= 2? He notes no bound on the inserted speeds is known.
- **Question 8.3.** Are there tight multi-entry modifications not from Theorem 5.1, apart from
  sets such as {1,4,5,6,7,11,13}?

## The new ingredient: for each n the search is finite with no cap on w

Let S = [n-1] minus {r1, r2}, A_v = {t : ||v t|| <= 1/n} (closed arcs of length 2/(nv), period 1/v,
separated by open gaps of length (n-2)/(nv)), and U = the circle minus the union of A_v over S.
U is a finite union of open intervals ("pieces"). V = S + {w1, w2} (w1 != w2, both >= n) has
ML(V) <= 1/n iff A_w1 and A_w2 together cover U.

- **(B1)** A piece of length l contains a whole gap of w as soon as l >= 1/w + (n-2)/(nw), i.e.
  w n l >= 2n - 2. A connected set covered by finitely many disjoint closed arcs lies in one of
  them. If both inserted speeds met this for the longest piece, each one's whole gap would lie in
  one arc of the other: (n-2)/(n w1) <= 2/(n w2) and (n-2)/(n w2) <= 2/(n w1), so (n-2)^2 <= 4,
  false for n >= 5. Hence one inserted speed ws satisfies **n <= ws < (2n-2)/(n l_max)**. If that
  range is empty, no tight modification removes R.
- **(B2)** For each such ws, every piece of U minus A_ws lies inside one arc of the other speed wf.
  With (c, d) the longest such piece, of length lam: **wf <= 2/(n lam)** and
  (k - 1/n)/c <= wf <= (k + 1/n)/d for some integer 0 <= k <= (c + d)/(n lam).
- If U minus A_ws is empty, S + {ws} (n - 2 speeds) has ML <= 1/n, contradicting the conjecture
  (proved for these sizes when n <= 16). Such cases are reported as anomalies, never skipped.

So for each n and each R the census is exhaustive over all inserted pairs, with no cap. This
also yields, for each n, an explicit upper bound B(n) on the inserted speeds of every tight
two-entry modification (data for Question 8.2).

## Method

`tm2.py`: exact rational arithmetic for all decisions (the sweep that finds U compares doubles,
which is exact here: every endpoint is p/q with q <= n^2, see `all_arcs`). Every hit is
re-checked by two independent integer checkers (`is_cover`: right-endpoint test of the covering;
`ml_at_least`: an arc endpoint where every speed is at distance >= 1/n) and classified by
`is_thm51` (perfect matching r -> m_r r with the Goddyn-Wong gcd criterion) and by dilation.
Tests (`test_tm2.py`) must pass before any run: T1 checkers on known sets; T2 the Theorem 5.1
matcher; T3 the uncovered pieces against exact point tests for 6 <= n <= 12; T4 census for
5 <= n <= 8 equals the known classification of tight sets of 4..7 speeds; T5 census equals an
independent brute force with w <= 6n for 5 <= n <= 8; T6 the n = 74 doubling instance is found.

Runs: (A) every R for 5 <= n <= 200 ("all"); (H) r1, r2 > (n-1)/2 for 5 <= n <= 400 ("high"),
in a compete job (2 CPU, time caps 2.5 h and 3 h) and a short gate probe. Caps per R (100,000
slow speeds; 1,000,000 values of k) are reported as "unresolved", never as "none".

## Predictions (graded against the outputs, whatever they say)

- **P1.** (A) For 9 <= n <= N_A (the largest n completed), the only tight two-entry modification is
  n = 74, {70, 72} -> {140, 144}. In particular no tight one has an inserted speed above 8n.
- **P2.** (H) For every completed n, every tight two-entry modification with r1, r2 > (n-1)/2 comes
  from Theorem 5.1. We expect the doubling instances at n = 74 and n = 284 (Zhang, Example 5.2)
  and possibly a few more Theorem 5.1 instances.
- **P3.** No anomaly (no case where S plus one speed already covers).
- **P4.** Fewer than 1% of the pairs R need the inner search (the rest are excluded by B1).
- **P5.** B(n) / (n ln n) stays below 10 for every completed n.

Grading: each prediction is true, false, or not reached (if the runs stop early). A tight set
not from Theorem 5.1, not a dilate and not the n = 8 set would answer Question 8.3 positively; it
is reported only after a third, independent re-check with a fresh exact sweep.

## What counts as new

Zhang's census is capped at w <= 8n (w <= 40n for n <= 18). We know of no census of two-entry
modifications without a cap on w, and no finite reduction of the kind above, as of 2026-11-25
(searches: arXiv listing for "lonely runner", newest first; GitHub
1337isnot1337/solved-conjectures issues and PRs for "Zhang", "lonely", "tight"; GitHub
Qinrayn/lonely-runner-tight-II; LeeMarshall1113/ai-math-results; web searches for Questions
8.1 and 8.3). The tight sets of 6 and 7 speeds were classified (unrefereed) in
LeeMarshall1113/ai-math-results (release v2026.10.29c); that covers n <= 8 only.
