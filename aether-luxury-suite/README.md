# AETHER° Autonomous Luxury Concierge

> A fully operational, multi-stack reference architecture for a high-converting luxury concierge landing experience backed by Python analytics, TypeScript orchestration, and Java identity attestation.

---

## What This Is

AETHER is a fictional but functionally complete private AI concierge brand. The project ships a single-page marketing site with a particle-driven WebGL-style canvas, animated metrics, interactive pricing tiers, and a live concierge form. Behind the front-end sit three real backend services that communicate over HTTP.

This is designed as a portfolio-grade demonstration: it looks expensive, converts visitors into leads, and exposes enough real code to impress technical reviewers without becoming unmaintainable.

## Product Structure

```
aether-luxury-suite/
├── index.html                         # Combined HTML/CSS/JS marketing page
├── backend/
│   ├── python/
│   │   ├── analytics_service.py       # Intent-vector recommender (numpy)
│   │   └── requirements.txt
│   ├── typescript/
│   │   ├── orchestrator.ts            # Lead ingestion + agent planning
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── java/
│       ├── IdentityService.java       # JWT + attestation service
│       └── pom.xml
└── README.md
```

## Stack Rationale

- **HTML/CSS/JS in one file** keeps the landing page trivial to deploy on any static host (Netlify, Vercel, S3, GitHub Pages). The particle network renders on a 2D canvas with no external dependencies.
- **Python analytics service** uses lightweight cosine-similarity intent vectors. It is intentionally simple to avoid over-engineering a demo, but it is a real HTTP service with stateful memory.
- **TypeScript orchestrator** acts as the API gateway. It routes leads, calls Python for enrichment, and returns structured agent plans. Type safety and explicit interfaces make it easy to extend.
- **Java identity service** demonstrates zero-trust JWT issuance with per-request attestation nonces. Java 21 virtual threads keep it concise and high-throughput.

## Running Locally

### 1. Start Python Analytics

```bash
cd backend/python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python analytics_service.py
```

Service runs on `http://localhost:8001`.

### 2. Start TypeScript Orchestrator

```bash
cd backend/typescript
npm install
npm run dev
```

Service runs on `http://localhost:4000`.

### 3. Start Java Identity Service

```bash
cd backend/java
mvn package
java -jar target/identity-service-1.0.0.jar
```

Service runs on `http://localhost:8002`.

### 4. Open the Site

Open `index.html` directly in a browser or serve it with any static server. The concierge form will hit `http://localhost:4000/leads` when running locally.

## API Endpoints

### Orchestrator (`:4000`)

- `GET /health` - service health
- `GET /leads` - list captured leads
- `POST /leads` - create a lead
  ```json
  {
    "email": "jordan@example.com",
    "tier": "patron",
    "request": "Book a private dinner in Kyoto next Thursday"
  }
  ```

### Analytics (`:8001`)

- `GET /health`
- `GET /history`
- `POST /analyze` - returns intent tokens, similar history, and recommended addons

### Identity (`:8002`)

- `GET /health`
- `POST /attest` - issue a JWT bound to a nonce
- `POST /verify` - verify a token

## Design Notes

- The color system uses deep charcoal, warm ivory, and antique gold. Typography is restrained. Motion is limited to fades, counters, and the ambient particle field so the page feels expensive rather than busy.
- The concierge form degrades gracefully. If the backend is unreachable, it shows a demo-mode message instead of crashing.
- All backend services are single-file reference implementations. They are not production-hardened (no persistent DB, no rate limiting, no TLS) but they are fully operational and wired together.

## Sources

- Fielding, R. (2000). *Architectural styles and the design of network-based software architectures* (Doctoral dissertation, University of California, Irvine). https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design patterns: Elements of reusable object-oriented software*. Addison-Wesley.
- IETF. (2015). RFC 7519: JSON Web Token (JWT). https://tools.ietf.org/html/rfc7519
- Mozilla Developer Network. (2024). *Canvas API*. https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API

---

Built as a reference implementation. Use it as a starting point, tear it apart, or adapt the architecture for a real product.