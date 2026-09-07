package com.aether.identity;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

import javax.crypto.SecretKey;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Base64;
import java.util.Date;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;

/**
 * AETHER Identity Service
 * Issues short-lived JWTs bound to a per-request attestation nonce.
 * Demonstrates a zero-trust ring for the concierge mesh.
 */
public final class IdentityService {

    private static final int PORT = Integer.parseInt(System.getenv().getOrDefault("IDENTITY_PORT", "8002"));
    private static final SecretKey MASTER_KEY = Keys.secretKeyFor(SignatureAlgorithm.HS256);
    private static final Map<String, Attestation> ATTESTATIONS = new ConcurrentHashMap<>();

    record Attestation(String tier, String fingerprint, Instant issuedAt) {
    }

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", PORT), 0);
        server.createContext("/attest", new AttestHandler());
        server.createContext("/verify", new VerifyHandler());
        server.createContext("/health", new HealthHandler());
        server.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
        server.start();
        System.out.println("AETHER Identity Service listening on :" + PORT);
    }

    private static void respond(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    static final class AttestHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                respond(exchange, 405, "{\"error\":\"method not allowed\"}");
                return;
            }
            String body = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
            Map<?, ?> json = parseJson(body);
            String tier = String.valueOf(json.getOrDefault("tier", "resident"));
            String fingerprint = String.valueOf(json.getOrDefault("fingerprint", "anon"));
            String nonce = Base64.getUrlEncoder().withoutPadding().encodeToString(Keys.secretKeyFor(SignatureAlgorithm.HS256).getEncoded()).substring(0, 16);

            ATTESTATIONS.put(nonce, new Attestation(tier, fingerprint, Instant.now()));

            String jwt = Jwts.builder()
                    .setSubject(fingerprint)
                    .claim("tier", tier)
                    .claim("nonce", nonce)
                    .setIssuedAt(Date.from(Instant.now()))
                    .setExpiration(Date.from(Instant.now().plus(15, ChronoUnit.MINUTES)))
                    .signWith(MASTER_KEY)
                    .compact();

            respond(exchange, 200, "{\"token\":\"" + jwt + "\",\"nonce\":\"" + nonce + "\",\"expires_in_minutes\":15}");
        }
    }

    static final class VerifyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                respond(exchange, 405, "{\"error\":\"method not allowed\"}");
                return;
            }
            String body = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
            Map<?, ?> json = parseJson(body);
            String token = String.valueOf(json.getOrDefault("token", ""));
            try {
                var claims = Jwts.parserBuilder().setSigningKey(MASTER_KEY).build().parseClaimsJws(token).getBody();
                String nonce = claims.get("nonce", String.class);
                Attestation attestation = ATTESTATIONS.get(nonce);
                if (attestation == null) {
                    respond(exchange, 401, "{\"error\":\"attestation revoked\"}");
                    return;
                }
                respond(exchange, 200, "{\"valid\":true,\"tier\":\"" + attestation.tier() + "\",\"fingerprint\":\"" + attestation.fingerprint() + "\"}");
            } catch (Exception e) {
                respond(exchange, 401, "{\"error\":\"invalid token\"}");
            }
        }
    }

    static final class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            respond(exchange, 200, "{\"status\":\"healthy\",\"service\":\"identity\",\"attestations\":" + ATTESTATIONS.size() + "}");
        }
    }

    @SuppressWarnings("unchecked")
    private static Map<?, ?> parseJson(String raw) {
        if (raw == null || raw.isBlank()) {
            return Map.of();
        }
        Map<String, Object> result = new java.util.HashMap<>();
        raw = raw.trim().replaceAll("[{}\\\"]", "");
        for (String pair : raw.split(",")) {
            String[] kv = pair.split(":", 2);
            if (kv.length == 2) {
                result.put(kv[0].trim(), kv[1].trim());
            }
        }
        return result;
    }
}