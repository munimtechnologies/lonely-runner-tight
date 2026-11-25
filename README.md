# lonely-runner-tight

Exact searches for **tight instances of the Lonely Runner Conjecture**: sets V of n - 1 speeds with
loneliness exactly 1/n. Apache-2.0 (code), CC BY 4.0 (text and data). By MV2, Munim, Inc.
(mv2@munimtech.com). This work was made with AI agents working in MV2's name; no human expert
has checked it yet.

## Current study: Zhang's Question 8.1 without a cap on the inserted speeds

Yuhan Zhang ([arXiv:2608.13599](https://arxiv.org/abs/2608.13599)) asks for the tight two-entry
modifications ([n-1] minus {r1, r2}) union {w1, w2} of the basic tight set {1, ..., n-1}. His
census covers 8 <= n <= 140 with w <= 8n. Here a short covering argument (bounds B1 and B2 in
[PREREG_q81.md](PREREG_q81.md)) makes the search finite for each n **with no cap on w**, so the
census is exhaustive for every n it completes.

- `tm2.py`: the census engine, two independent exact checkers, and the Goddyn-Wong Theorem 5.1
  matcher.
- `test_tm2.py`: tests T1-T6 (known tight sets, brute-force agreement for n <= 8, the n = 74
  doubling instance).
- `census_job.py`: the batch run (`--mode all` for every pair R, `--mode high` for
  r1, r2 > (n-1)/2).
- `PREREG_q81.md`: the question, the proofs of the bounds, and the predictions, fixed before
  any run.

Results will be added as `RESULTS_q81.md` when the runs finish, graded against the
pre-registration whatever they show.

## Credits

The question and the census it extends are Yuhan Zhang's. Theorem 5.1 is from Goddyn and Wong
("Tight instances of the lonely runner", Integers 6, 2006). Problem 1 is from Perarnau and Serra
([arXiv:2409.20160](https://arxiv.org/abs/2409.20160)).
