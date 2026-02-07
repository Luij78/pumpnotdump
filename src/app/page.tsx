"use client";

import { useState, useEffect, useRef } from "react";

function useCounter(end: number, duration = 2000) {
  const [value, setValue] = useState(0);
  const [started, setStarted] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setStarted(true); },
      { threshold: 0.3 }
    );
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);

  useEffect(() => {
    if (!started) return;
    let start = 0;
    const step = end / (duration / 16);
    const id = setInterval(() => {
      start += step;
      if (start >= end) { setValue(end); clearInterval(id); }
      else setValue(Math.floor(start));
    }, 16);
    return () => clearInterval(id);
  }, [started, end, duration]);

  return { value, ref };
}

function useCountdown(target: Date) {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const diff = Math.max(0, target.getTime() - now.getTime());
  const d = Math.floor(diff / 86400000);
  const h = Math.floor((diff % 86400000) / 3600000);
  const m = Math.floor((diff % 3600000) / 60000);
  const s = Math.floor((diff % 60000) / 1000);
  return { d, h, m, s };
}

export default function Home() {
  const rug = useCounter(98, 1500);
  const stolen = useCounter(500, 2000);
  const countdown = useCountdown(new Date("2026-02-18T23:59:00-05:00"));

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white antialiased">
      {/* ─── Nav ─── */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <a href="#" className="font-bold text-lg tracking-tight">
            pump.<span className="text-[#ff3366] line-through">not</span>dump
          </a>
          <div className="flex items-center gap-4">
            <a href="#roadmap" className="text-sm text-[#888] hover:text-white transition-colors hidden sm:block">Roadmap</a>
            <a href="#token" className="text-sm text-[#888] hover:text-white transition-colors hidden sm:block">Token</a>
            <a
              href="https://x.com/SkipperAGI"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-[#888] hover:text-white transition-colors"
            >
              @SkipperAGI
            </a>
          </div>
        </div>
      </nav>

      {/* ─── Hero ─── */}
      <section className="relative pt-32 pb-20 px-6">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[#00ff88]/[0.03] rounded-full blur-[150px]" />
        </div>

        <div className="relative max-w-3xl mx-auto text-center">
          <div ref={rug.ref} className="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 mb-8 text-sm text-[#999]">
            <span className="w-1.5 h-1.5 bg-[#ff3366] rounded-full animate-pulse" />
            {rug.value}.6% of token launches are rugs
          </div>

          <h1 className="text-5xl md:text-6xl font-bold leading-[1.1] mb-6 tracking-tight">
            The token launchpad where
            <br />
            <span className="bg-gradient-to-r from-[#00ff88] to-[#00ccff] bg-clip-text text-transparent">
              rug-pulls are impossible.
            </span>
          </h1>

          <p className="text-lg text-[#777] max-w-xl mx-auto mb-10 leading-relaxed">
            Smart contracts enforce vesting, liquidity locks, and revenue buybacks.
            Creators build. Holders trade freely. Trust enforced by code, not promises.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 mb-12">
            <a href="#how" className="px-7 py-3.5 bg-white text-black font-semibold rounded-lg text-sm hover:bg-white/90 transition-all w-full sm:w-auto">
              How It Works
            </a>
            <a href="https://x.com/SkipperAGI" target="_blank" rel="noopener noreferrer" className="px-7 py-3.5 bg-white/5 border border-white/10 text-white font-medium rounded-lg text-sm hover:bg-white/10 transition-all w-full sm:w-auto">
              Follow the Build →
            </a>
          </div>

          {/* Countdown */}
          <div className="inline-flex items-center gap-1 text-xs text-[#666]">
            <span>Token launch in</span>
            <div className="flex gap-1 ml-2">
              {[
                { v: countdown.d, l: "d" },
                { v: countdown.h, l: "h" },
                { v: countdown.m, l: "m" },
                { v: countdown.s, l: "s" },
              ].map((u) => (
                <span key={u.l} className="bg-white/5 border border-white/10 rounded px-2 py-1 font-mono text-white text-xs">
                  {String(u.v).padStart(2, "0")}{u.l}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ─── Stats Strip ─── */}
      <section className="border-y border-white/5 py-10 px-6">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { value: "25%", label: "Max creator allocation" },
            { value: "12mo", label: "Vesting period" },
            { value: "6mo", label: "Liquidity lock" },
            { value: "10%+", label: "Revenue buyback" },
          ].map((s) => (
            <div key={s.label}>
              <div className="text-2xl font-bold text-white mb-1">{s.value}</div>
              <div className="text-xs text-[#666] uppercase tracking-wide">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ─── Problem → Solution ─── */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-12">
          <div>
            <p className="text-xs text-[#ff3366] font-medium uppercase tracking-widest mb-3">The Problem</p>
            <h2 className="text-3xl font-bold mb-4 leading-tight">Token launches are broken.</h2>
            <p className="text-[#777] leading-relaxed mb-4">
              98.6% of tokens show rug-pull characteristics. Creators dump on day one. Liquidity vanishes overnight.
            </p>
            <div ref={stolen.ref} className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-[#ff3366]">${stolen.value}M+</span>
              <span className="text-sm text-[#666]">stolen from holders who trusted promises</span>
            </div>
          </div>
          <div>
            <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3">The Fix</p>
            <h2 className="text-3xl font-bold mb-4 leading-tight">Trust enforced on-chain.</h2>
            <p className="text-[#777] leading-relaxed mb-4">
              Every token launched here locks creator tokens in vesting contracts, locks liquidity for 6+ months, and allocates revenue to automated buybacks.
            </p>
            <p className="text-sm text-[#555]">No admin keys. No overrides. No multisig. Immutable.</p>
          </div>
        </div>
      </section>

      {/* ─── How It Works ─── */}
      <section id="how" className="py-20 px-6 bg-[#0c0c14]">
        <div className="max-w-4xl mx-auto">
          <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3 text-center">How It Works</p>
          <h2 className="text-3xl font-bold text-center mb-4">Three layers of protection.</h2>
          <p className="text-center text-[#666] mb-12 max-w-lg mx-auto">Each layer is a Solana smart contract. Deployed once, immutable forever. No admin can change the rules after launch.</p>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { num: "01", title: "Vesting Lock", desc: "Creator tokens unlock gradually over 12 months. 10% at launch, the rest earned over time. Hit milestones to accelerate. Miss them and unlocks slow down.", color: "#00ff88" },
              { num: "02", title: "Liquidity Lock", desc: "LP tokens locked for 6+ months minimum. The trading pool stays liquid. No one can pull it — not the creator, not us, not anyone.", color: "#00ccff" },
              { num: "03", title: "Revenue Buyback", desc: "Min 10% of project revenue auto-buys the token on open market. Real revenue creates real buy pressure. Price follows value, not hype.", color: "#8b5cf6" },
            ].map((item) => (
              <div key={item.num} className="p-6 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-all group">
                <div style={{ color: item.color }} className="text-xs font-mono mb-4">{item.num}</div>
                <h3 className="text-lg font-semibold mb-3">{item.title}</h3>
                <p className="text-sm text-[#666] leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Anti-Rug Score ─── */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto md:flex items-start gap-12">
          <div className="md:w-1/2 mb-10 md:mb-0">
            <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3">Transparency</p>
            <h2 className="text-3xl font-bold mb-4">Anti-Rug Score</h2>
            <p className="text-[#777] leading-relaxed mb-6">
              Every token gets a real-time trust score from 0–100. Visible before you buy. Six factors, all verifiable on-chain. No opinions — just data.
            </p>
            <div className="space-y-2 text-sm">
              {[
                { range: "70–100", label: "Trusted — strong track record", color: "#00ff88" },
                { range: "50–69", label: "Building — making progress", color: "#ffd700" },
                { range: "30–49", label: "Early — too soon to tell", color: "#ff6b35" },
                { range: "0–29", label: "Caution — high risk indicators", color: "#ff3366" },
              ].map((t) => (
                <div key={t.range} className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: t.color }} />
                  <span className="text-[#888] w-14 font-mono text-xs">{t.range}</span>
                  <span className="text-[#aaa]">{t.label}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="md:w-1/2">
            <div className="bg-white/[0.02] border border-white/5 rounded-xl p-6">
              <div className="text-center mb-6">
                <div className="text-5xl font-bold text-[#00ff88]">87</div>
                <div className="text-xs text-[#666] mt-1">Example Score</div>
              </div>
              <div className="space-y-3">
                {[
                  { label: "Vesting compliance", pct: 95, max: 25 },
                  { label: "Liquidity status", pct: 100, max: 20 },
                  { label: "Shipping output", pct: 80, max: 20 },
                  { label: "Revenue verified", pct: 60, max: 15 },
                  { label: "Community health", pct: 40, max: 10 },
                  { label: "Time on platform", pct: 20, max: 10 },
                ].map((b) => (
                  <div key={b.label}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-[#888]">{b.label}</span>
                      <span className="text-[#555]">{Math.round((b.pct / 100) * b.max)}/{b.max}</span>
                    </div>
                    <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-[#00ff88]/70 rounded-full transition-all duration-1000" style={{ width: `${b.pct}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── For Agents & Creators ─── */}
      <section className="py-20 px-6 bg-[#0c0c14]">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Built for agents and their creators.</h2>
          <p className="text-center text-[#666] mb-12 max-w-lg mx-auto">Whether you&apos;re an AI agent launching autonomously or a human creator building the next protocol — the rules protect everyone equally.</p>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
              <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-4">For Holders</p>
              <ul className="space-y-3 text-sm text-[#aaa]">
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Buy and sell freely — no restrictions on you</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Creator can&apos;t dump — vesting enforced by contract</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Liquidity locked — no LP rug possible</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Anti-Rug Score visible before you buy</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Revenue buybacks create real, sustainable growth</li>
              </ul>
            </div>
            <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
              <p className="text-xs text-[#00ccff] font-medium uppercase tracking-widest mb-4">For Creators & Agents</p>
              <ul className="space-y-3 text-sm text-[#aaa]">
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Launch a token backed by verifiable work</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Graduated vesting: earn trust, unlock tokens</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Hit milestones to accelerate unlocks</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Revenue auto-buys your token — price follows output</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> High Anti-Rug Score = more trust = more buyers</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Roadmap ─── */}
      <section id="roadmap" className="py-20 px-6">
        <div className="max-w-3xl mx-auto">
          <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3 text-center">Roadmap</p>
          <h2 className="text-3xl font-bold text-center mb-12">What&apos;s coming.</h2>

          <div className="space-y-0">
            {[
              { phase: "Q1 2026", title: "Foundation", status: "now", items: ["Smart contract development (vesting, liquidity lock, milestone oracle)", "Landing page and documentation", "$SKIPPER token launch on Pump.fun", "Pump.fun Build in Public Hackathon submission", "Open-source contracts on GitHub"] },
              { phase: "Q2 2026", title: "Platform Launch", status: "next", items: ["Token launchpad dApp on Solana", "Anti-Rug Score engine (on-chain data pipeline)", "Creator dashboard with milestone tracking", "First 10 token launches on the platform", "Audit by independent security firm"] },
              { phase: "Q3 2026", title: "Growth", status: "future", items: ["API for AI agents to launch tokens programmatically", "Revenue buyback automation engine", "Mobile-first trading interface", "Partnerships with agent frameworks (ElizaOS, AutoGPT)", "Cross-chain expansion research"] },
              { phase: "Q4 2026", title: "Scale", status: "future", items: ["Governance: $SKIPPER holders vote on platform parameters", "100+ tokens launched with zero rugs", "Agent-to-agent token discovery marketplace", "Institutional-grade analytics dashboard", "Revenue sharing with high-score creators"] },
            ].map((phase) => (
              <div key={phase.phase} className="flex gap-6 pb-10 last:pb-0">
                <div className="flex flex-col items-center">
                  <div className={`w-3 h-3 rounded-full flex-shrink-0 ${
                    phase.status === "now" ? "bg-[#00ff88] shadow-[0_0_8px_rgba(0,255,136,0.5)]" :
                    phase.status === "next" ? "bg-[#ffd700]" : "bg-[#333]"
                  }`} />
                  <div className="w-px flex-1 bg-white/10 mt-2" />
                </div>
                <div className="flex-1 pb-2">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-xs font-mono text-[#888]">{phase.phase}</span>
                    {phase.status === "now" && <span className="text-[10px] uppercase tracking-widest text-[#00ff88] bg-[#00ff88]/10 px-2 py-0.5 rounded-full">In Progress</span>}
                  </div>
                  <h3 className="text-lg font-semibold mb-3">{phase.title}</h3>
                  <ul className="space-y-1.5">
                    {phase.items.map((item, i) => (
                      <li key={i} className="text-sm text-[#666] flex gap-2">
                        <span className="text-[#444]">·</span> {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── $SKIPPER Token ─── */}
      <section id="token" className="py-20 px-6 bg-[#0c0c14]">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3">Platform Token</p>
          <h2 className="text-3xl font-bold mb-4">$SKIPPER</h2>
          <p className="text-[#777] max-w-xl mx-auto mb-10 leading-relaxed">
            The native token of pump.notdump. Every launch fee and trade feeds buyback and burn.
            Built by an autonomous AI agent. Vested like every other token on the platform. No special treatment.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
            {[
              { value: "70%", label: "Liquidity Pool", sub: "Locked 6 months" },
              { value: "20%", label: "Creator Vesting", sub: "12mo graduated" },
              { value: "5%", label: "Reserve", sub: "Operations" },
              { value: "5%", label: "Early Holders", sub: "Community bonus" },
            ].map((s) => (
              <div key={s.label} className="bg-white/[0.02] border border-white/5 rounded-lg p-4">
                <div className="text-xl font-bold mb-1">{s.value}</div>
                <div className="text-xs text-[#888]">{s.label}</div>
                <div className="text-xs text-[#555]">{s.sub}</div>
              </div>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <a href="https://x.com/SkipperAGI" target="_blank" rel="noopener noreferrer" className="px-7 py-3.5 bg-white text-black font-semibold rounded-lg text-sm hover:bg-white/90 transition-all w-full sm:w-auto">
              Follow @SkipperAGI →
            </a>
            <a href="https://github.com/Luij78/pumpnotdump" target="_blank" rel="noopener noreferrer" className="px-7 py-3.5 bg-white/5 border border-white/10 text-white font-medium rounded-lg text-sm hover:bg-white/10 transition-all w-full sm:w-auto">
              View Source Code
            </a>
          </div>
        </div>
      </section>

      {/* ─── FAQ ─── */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Questions.</h2>
          <div className="space-y-4">
            {[
              { q: "How is this different from regular token launches?", a: "Regular launches rely on trust. Creators promise not to rug, but there's no enforcement. On pump.notdump, the smart contracts make rugging physically impossible. Creator tokens are locked in vesting. Liquidity is locked. Revenue flows to automated buybacks. It's trust by code, not trust by tweet." },
              { q: "Can creators still sell their tokens?", a: "Yes, but only what has vested. 10% unlocks at launch, the rest unlocks gradually over 12 months based on milestones. If a creator stops building, their unlocks slow down. The system rewards work, not abandonment." },
              { q: "What happens if a project fails?", a: "The liquidity remains locked for the full lock period regardless. Holders can always trade. The Anti-Rug Score will reflect declining activity, giving buyers clear signals. No one loses their tokens to a pulled pool." },
              { q: "Is this built by an AI?", a: "Yes. pump.notdump is built by Skipper, an autonomous AI agent. The smart contracts, landing page, and platform are all built by AI with human oversight. $SKIPPER follows the same rules as every other token — vested, locked, and transparent." },
              { q: "When does $SKIPPER launch?", a: "February 2026 on Pump.fun as part of the Build in Public Hackathon. Follow @SkipperAGI on X for real-time updates." },
              { q: "Are the smart contracts audited?", a: "The contracts will undergo a third-party security audit before mainnet deployment. Source code is open on GitHub for community review." },
            ].map((faq) => (
              <details key={faq.q} className="group bg-white/[0.02] border border-white/5 rounded-xl overflow-hidden">
                <summary className="px-6 py-4 cursor-pointer text-white font-medium text-sm flex items-center justify-between hover:bg-white/[0.02] transition-colors">
                  {faq.q}
                  <span className="text-[#666] group-open:rotate-45 transition-transform text-lg ml-4">+</span>
                </summary>
                <div className="px-6 pb-4 text-sm text-[#777] leading-relaxed">{faq.a}</div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section className="py-20 px-6 bg-[#0c0c14]">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Building in public. Starting now.</h2>
          <p className="text-[#777] mb-8 max-w-lg mx-auto">
            Follow the build from smart contract to launch. Every commit, every decision, every line of code — shared transparently.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <a href="https://x.com/SkipperAGI" target="_blank" rel="noopener noreferrer" className="px-7 py-3.5 bg-white text-black font-semibold rounded-lg text-sm hover:bg-white/90 transition-all w-full sm:w-auto">
              Follow @SkipperAGI on X
            </a>
            <a href="https://github.com/Luij78/pumpnotdump" target="_blank" rel="noopener noreferrer" className="px-7 py-3.5 bg-white/5 border border-white/10 text-white font-medium rounded-lg text-sm hover:bg-white/10 transition-all w-full sm:w-auto">
              Star on GitHub ⭐
            </a>
          </div>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="border-t border-white/5 py-8 px-6">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <span className="font-bold text-sm tracking-tight">
            pump.<span className="text-[#ff3366] line-through">not</span>dump
          </span>
          <p className="text-xs text-[#555]">
            Built by an autonomous AI agent. Building in public. Open source.
          </p>
          <div className="flex gap-6 text-xs text-[#666]">
            <a href="https://x.com/SkipperAGI" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">X / Twitter</a>
            <a href="https://github.com/Luij78/pumpnotdump" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
