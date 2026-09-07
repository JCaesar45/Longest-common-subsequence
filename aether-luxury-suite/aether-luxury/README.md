> # Aether LCS
>
> *Sequence alchemy for the obsessively precise.*
>
> Aether LCS is a case-sensitive **Longest Common Subsequence** engine rendered as a luminous, conversion-obsessed web experience. It ships with reference implementations in JavaScript, TypeScript, Python, and Java, plus a production-ready FastAPI backend.

---

## What it does

Given two strings, it returns one longest subsequence that appears in both, preserving order but not necessarily contiguity. Unlike a longest common substring problem, gaps are allowed. The canonical example:

```
"thisisatest"  +  "testing123testing"  →  "tsitest"
```

The algorithm is the classic Wagner–Fischer dynamic-programming approach: build an `(m+1) × (n+1)` score table, then backtrack from the bottom-right corner to reconstruct a solution (Wagner & Fischer, 1974).

---

## Product structure

```
aether-luxury/
├── index.html          # Single-file luxurious landing page + demo
├── python/
│   ├── lcs_engine.py   # Pure Python engine + tests
│   ├── api.py          # FastAPI service
│   └── requirements.txt
├── typescript/
│   ├── lcs.ts          # Typed engine
│   ├── lcs.test.ts     # Vitest suite
│   ├── package.json
│   └── tsconfig.json
├── java/
│   ├── LcsEngine.java      # Java reference engine
│   ├── LcsEngineTest.java  # JUnit tests
│   └── pom.xml
└── README.md
```

---

## Frontend

Open `index.html` in any modern browser. Everything is self-contained:

- Canvas particle network with connection thresholding
- Glassmorphism demo card with live LCS computation
- Tabbed code showcase for all four implementations
- Conversion-oriented pricing cards
- Reduced-motion and mobile responsive CSS

No build step, no dependencies, no CDN required beyond Google Fonts.

---

## Python

```bash
cd python
pip install -r requirements.txt
python lcs_engine.py
uvicorn api:app --reload
```

The API exposes:

- `GET /health`
- `POST /lcs` with JSON body `{ "a": "...", "b": "..." }`

---

## TypeScript

```bash
cd typescript
npm install
npm test
npm run build
```

---

## Java

```bash
cd java
mvn test
mvn compile exec:java -Dexec.mainClass="LcsEngine"
```

---

## Test coverage

All implementations cover the Rosetta Code test vectors and additional edge cases for empty strings and case sensitivity.

| Input A | Input B | Expected LCS |
|---|---|---|
| `thisisatest` | `testing123testing` | `tsitest` |
| `ABCDGH` | `AEDFHR` | `ADH` |
| `AGGTAB` | `GXTXAYB` | `GTAB` |
| `BDACDB` | `BDCB` | `BDCB` |
| `ABAZDC` | `BACBAD` | `ABAD` |

---

## Why these choices

I kept the frontend in a single HTML file because the brief demanded combined HTML, CSS, and JavaScript. Splitting the backend by language keeps each stack idiomatic and testable. The DP table is dense rather than space-optimized because clarity matters more than shaving an asymptotically negligible constant for demo code; production paths can switch to Hirschberg’s linear-space algorithm if inputs grow large (Hirschberg, 1975).

---

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Hirschberg, D. S. (1975). A linear space algorithm for computing maximal common subsequences. *Communications of the ACM*, 18(6), 341–343. https://doi.org/10.1145/360825.360861
- Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM*, 21(1), 168–173. https://doi.org/10.1145/321796.321811
