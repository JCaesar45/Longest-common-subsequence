> # Aether LCS
>
> *Sequence intelligence, wrapped in digital luxury.*
>
> Aether LCS is a case-sensitive **Longest Common Subsequence** engine delivered as a luminous, conversion-focused web experience. It ships with reference implementations in JavaScript, TypeScript, Python, and Java, plus a production-ready FastAPI backend.

---

## What it does

Given two strings, Aether LCS returns one longest subsequence common to both, preserving order while allowing gaps. Unlike longest common substring, the matched elements need not be contiguous.

```
"thisisatest"  +  "testing123testing"  →  "tsitest"
```

The algorithm follows the classic Wagner–Fischer dynamic-programming approach: fill an `(m+1) × (n+1)` score table, then backtrack from the bottom-right corner to reconstruct a maximum-length solution (Wagner & Fischer, 1974).

---

## Product structure

```
aether-luxury/
├── index.html              # Single-file luxurious landing page + live demo
├── python/
│   ├── lcs_engine.py       # Pure Python engine + test runner
│   ├── api.py              # FastAPI service
│   └── requirements.txt
├── typescript/
│   ├── lcs.ts              # Typed engine
│   ├── lcs.test.ts         # Vitest suite
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

Open `index.html` in any modern browser. It is fully self-contained:

- Animated canvas starfield with proximity connection lines
- Glassmorphism live LCS demo card
- Tabbed code showcase for all four language implementations
- Conversion-oriented pricing section
- Responsive CSS with reduced-motion support

No build step and no runtime dependencies except Google Fonts.

---

## Python

```bash
cd python
pip install -r requirements.txt
python lcs_engine.py
uvicorn api:app --reload
```

API endpoints:

- `GET /health`
- `POST /lcs` with body `{ "a": "...", "b": "..." }`

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

All implementations cover the canonical Rosetta Code vectors plus edge cases for empty strings and case sensitivity.

| Input A | Input B | Expected LCS |
|---|---|---|
| `thisisatest` | `testing123testing` | `tsitest` |
| `ABCDGH` | `AEDFHR` | `ADH` |
| `AGGTAB` | `GXTXAYB` | `GTAB` |
| `BDACDB` | `BDCB` | `BDCB` |
| `ABAZDC` | `BACBAD` | `ABAD` |

---

## Design rationale

I combined HTML, CSS, and JavaScript into one file because the brief asked for it. The backend is split by language so each stack stays idiomatic and independently testable. The DP table is dense rather than space-optimized for readability; for very large inputs, Hirschberg’s linear-space algorithm can be swapped in without changing the public interface (Hirschberg, 1975).

---

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Hirschberg, D. S. (1975). A linear space algorithm for computing maximal common subsequences. *Communications of the ACM*, 18(6), 341–343. https://doi.org/10.1145/360825.360861
- Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM*, 21(1), 168–173. https://doi.org/10.1145/321796.321811
