"""
AETHER Analytics Service
Processes behavioral signals and concierge request patterns for
personalized recommendation tuning without exposing raw PII.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

import numpy as np


@dataclass(frozen=True)
class ConciergeRequest:
    user_tier: str
    raw_request: str
    timestamp: datetime

    def tokens(self) -> list[str]:
        return re.findall(r"[a-zA-Z]+", self.raw_request.lower())

    def intent_vector(self, vocabulary: dict[str, int]) -> np.ndarray:
        vec = np.zeros(len(vocabulary), dtype=np.float32)
        for token in self.tokens():
            if token in vocabulary:
                vec[vocabulary[token]] += 1.0
        norm = np.linalg.norm(vec)
        return vec if norm == 0 else vec / norm


class LightweightRecommender:
    """Collaborative-filtering style scorer using cosine similarity on intent vectors."""

    def __init__(self) -> None:
        self.vocabulary: dict[str, int] = {}
        self.request_history: list[ConciergeRequest] = []
        self.vectors: list[np.ndarray] = []

    def _ensure_vocab(self, tokens: list[str]) -> None:
        for token in tokens:
            if token not in self.vocabulary:
                self.vocabulary[token] = len(self.vocabulary)

    def ingest(self, request: ConciergeRequest) -> None:
        self._ensure_vocab(request.tokens())
        # Rebuild previous vectors if vocabulary grew.
        self.vectors = [
            r.intent_vector(self.vocabulary) for r in self.request_history
        ]
        self.request_history.append(request)
        self.vectors.append(request.intent_vector(self.vocabulary))

    def similar_requests(self, request: ConciergeRequest, top_k: int = 3) -> list[dict[str, Any]]:
        self._ensure_vocab(request.tokens())
        target = request.intent_vector(self.vocabulary)
        if not self.vectors:
            return []
        scores = [
            (float(np.dot(target, vec)), idx)
            for idx, vec in enumerate(self.vectors)
        ]
        scores.sort(reverse=True)
        return [
            {
                "request": self.request_history[idx].raw_request,
                "tier": self.request_history[idx].user_tier,
                "similarity": round(score, 4),
            }
            for score, idx in scores[:top_k]
            if score > 0.0 and self.request_history[idx].raw_request != request.raw_request
        ]


class AnalyticsHandler(BaseHTTPRequestHandler):
    recommender = LightweightRecommender()

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(200, {"status": "healthy", "service": "analytics", "version": "1.0.0"})
            return
        if self.path == "/history":
            self._send_json(
                200,
                {
                    "count": len(self.recommender.request_history),
                    "vocab_size": len(self.recommender.vocabulary),
                },
            )
            return
        self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/analyze":
            self._send_json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid json"})
            return

        request = ConciergeRequest(
            user_tier=data.get("tier", "resident"),
            raw_request=data.get("request", ""),
            timestamp=datetime.utcnow(),
        )
        self.recommender.ingest(request)
        similar = self.recommender.similar_requests(request)

        self._send_json(
            200,
            {
                "intent_tokens": request.tokens()[:10],
                "similar_history": similar,
                "recommended_addons": self._addons(request),
            },
        )

    @staticmethod
    def _addons(request: ConciergeRequest) -> list[str]:
        tokens = set(request.tokens())
        addons = []
        if {"travel", "flight", "trip", "hotel"} & tokens:
            addons.append("travel-insurance")
        if {"dinner", "restaurant", "chef", "wine"} & tokens:
            addons.append("private-dining-network")
        if {"meeting", "calendar", "schedule"} & tokens:
            addons.append("executive-calendar-sync")
        return addons

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    port = int(os.environ.get("ANALYTICS_PORT", "8001"))
    server = HTTPServer(("0.0.0.0", port), AnalyticsHandler)
    print(f"AETHER Analytics Service listening on :{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()