/**
 * AETHER Orchestrator
 * Routes concierge requests to downstream agents, tracks lead state,
 * and surfaces structured response plans to the marketing front-end.
 */

import { createServer, IncomingMessage, ServerResponse } from "http";
import { parse } from "url";

interface ConciergeLead {
  id: string;
  email: string;
  tier: "resident" | "patron" | "house";
  request: string;
  createdAt: string;
  status: "received" | "analyzing" | "planned" | "contacted";
  plan: PlanItem[];
}

interface PlanItem {
  agent: string;
  action: string;
  eta: string;
}

interface AnalyticsPayload {
  tier: string;
  request: string;
}

const leads = new Map<string, ConciergeLead>();
const ANALYTICS_URL = process.env.ANALYTICS_URL ?? "http://localhost:8001";
const PORT = parseInt(process.env.ORCHESTRATOR_PORT ?? "4000", 10);

const jsonBody = (req: IncomingMessage): Promise<unknown> =>
  new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => (data += chunk));
    req.on("end", () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch (e) {
        reject(e);
      }
    });
    req.on("error", reject);
  });

const sendJson = (
  res: ServerResponse,
  status: number,
  payload: unknown
): void => {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body),
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  });
  res.end(body);
};

const generatePlan = (request: string, tier: string): PlanItem[] => {
  const lower = request.toLowerCase();
  const plan: PlanItem[] = [];
  if (/\b(dinner|restaurant|chef|dining)\b/.test(lower)) {
    plan.push({ agent: "dining", action: "Reserve private table or chef", eta: "< 2h" });
  }
  if (/\b(flight|hotel|travel|trip|kyoto|tokyo|paris)\b/.test(lower)) {
    plan.push({ agent: "travel", action: "Build itinerary and transport options", eta: "< 4h" });
  }
  if (/\b(meeting|calendar|schedule|call)\b/.test(lower)) {
    plan.push({ agent: "calendar", action: "Block time and send invitations", eta: "< 30m" });
  }
  if (plan.length === 0) {
    plan.push({ agent: "general", action: "Clarify scope with member", eta: "< 1h" });
  }
  if (tier === "patron" || tier === "house") {
    plan.push({ agent: "concierge", action: "Assign dedicated account architect", eta: "< 24h" });
  }
  if (tier === "house") {
    plan.push({ agent: "security", action: "Identity attestation review", eta: "< 1h" });
  }
  return plan;
};

const callAnalytics = async (payload: AnalyticsPayload): Promise<unknown> => {
  try {
    const response = await fetch(`${ANALYTICS_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch {
    return { error: "analytics unreachable" };
  }
};

const createLead = async (body: {
  email?: string;
  tier?: string;
  request?: string;
}): Promise<ConciergeLead> => {
  const id = `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  const tier = (body.tier as ConciergeLead["tier"]) ?? "resident";
  const request = String(body.request ?? "").trim();
  const lead: ConciergeLead = {
    id,
    email: String(body.email ?? ""),
    tier,
    request,
    createdAt: new Date().toISOString(),
    status: "received",
    plan: [],
  };
  leads.set(id, lead);

  // Async enrichment via Python analytics service.
  const analytics = await callAnalytics({ tier, request });
  console.log(`Analytics enrichment for lead ${id}:`, analytics);

  lead.status = "planned";
  lead.plan = generatePlan(request, tier);
  return lead;
};

const server = createServer(async (req, res) => {
  if (req.method === "OPTIONS") {
    sendJson(res, 204, {});
    return;
  }

  const parsed = parse(req.url ?? "/", true);

  if (req.method === "GET" && parsed.pathname === "/health") {
    sendJson(res, 200, { status: "healthy", service: "orchestrator", leads: leads.size });
    return;
  }

  if (req.method === "GET" && parsed.pathname === "/leads") {
    sendJson(res, 200, Array.from(leads.values()));
    return;
  }

  if (req.method === "POST" && parsed.pathname === "/leads") {
    try {
      const body = (await jsonBody(req)) as {
        email?: string;
        tier?: string;
        request?: string;
      };
      if (!body.email || !body.request) {
        sendJson(res, 400, { error: "email and request are required" });
        return;
      }
      const lead = await createLead(body);
      sendJson(res, 201, {
        id: lead.id,
        status: lead.status,
        plan: lead.plan,
        message: `Request received. ${lead.plan.length} agent${lead.plan.length === 1 ? "" : "s"} assigned.`,
      });
    } catch (e) {
      sendJson(res, 400, { error: "invalid request body" });
    }
    return;
  }

  sendJson(res, 404, { error: "not found" });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`AETHER Orchestrator listening on :${PORT}`);
});