import type { NextConfig } from "next";

// AD-11: én origin. Nettleseren kaller bare relative /api/*, og Next sender
// dem videre til backend. Port og frist er konstanter her, ingen miljøvariabler.
const nextConfig: NextConfig = {
  // next dev skriver ellers AGENTS.md på nytt når den oppdager en KI-agent.
  agentRules: false,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:8000/api/:path*",
      },
    ];
  },
  experimental: {
    proxyTimeout: 130000,
    agentUpgrade: false,
  },
};

export default nextConfig;
