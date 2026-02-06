"use client";

import { useState, useEffect } from "react";

/* ───────────────────────── helper: animated counter ───────────────────────── */
function useCounter(end: number, duration = 2000) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let start = 0;
    const step = end / (duration / 16);
    const id = setInterval(() => {
      start += step;
      if (start >= end) {
        setValue(end);
        clearInterval(id);
      } else {
        setValue(Math.floor(start));
      }
    }, 16);
    return () => clearInterval(id);
  }, [end, duration]);
  return value;
}

/* ───────────────────────────── Navbar ───────────────────────────── */
function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", handler);
    return () => window.removeEventListener("scroll", handler);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-[#0a0a0f]/90 backdrop-blur-md border-b border-[#2a2a3a]"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <a href="#" className="flex items-center gap-2 group">
          <span className="text-2xl">🛡️</span>
          <span className="font-bold text-lg">
            pump.<span className="text-[#ff3366] line-through">not</span>dump
            <span className="text-[#00ff88]">.fun</span>
          </span>
        </a>
        <div className="hidden md:flex items-center gap-8 text-sm text-[#888]">
          <a href="#problem" className="hover:text-white transition-colors">
            Problem
          </a>
          <a href="#solution" className="hover:text-white transition-colors">
            Solution
          </a>
          <a href="#how-it-works" className="hover:text-white transition-colors">
            How It Works
          </a>
          <a href="#skipper" className="hover:text-white transition-colors">
            $SKIPPER
          </a>
          <a href="#roadmap" className="hover:text-white transition-colors">
            Roadmap
          </a>
        </div>
        <a
          href="https://x.com/SkipperAGI"
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 bg-[#00ff88]/10 text-[#00ff88] border border-[#00ff88]/30 rounded-lg text-sm font-medium hover:bg-[#00ff88]/20 transition-all"
        >
          Follow @SkipperAGI
        </a>
      </div>
    </nav>
  );
}

/* ──────────────────────────── Hero Section ──────────────────────────── */
function Hero() {
  const rugPercent = useCounter(98, 1500);

  return (
    <section className="relative min-h-screen flex items-center justify-center grid-bg overflow-hidden">
      {/* gradient orbs */}
      <div className="absolute top-20 left-10 w-[500px] h-[500px] bg-[#00ff88]/5 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-20 right-10 w-[400px] h-[400px] bg-[#8b5cf6]/5 rounded-full blur-[120px] pointer-events-none" />

      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center pt-24 pb-20">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-[#ff3366]/10 border border-[#ff3366]/20 rounded-full px-4 py-1.5 mb-8">
          <span className="w-2 h-2 bg-[#ff3366] rounded-full pulse-red" />
          <span className="text-[#ff3366] text-sm font-medium">
            {rugPercent}.6% of tokens are rugs — Solidus Labs 2025
          </span>
        </div>

        {/* Headline */}
        <h1 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6">
          <span className="text-white">The launchpad where</span>
          <br />
          <span className="gradient-text">rug-pulls are impossible.</span>
        </h1>

        {/* Subheadline */}
        <p className="text-xl md:text-2xl text-[#888] max-w-3xl mx-auto mb-10 leading-relaxed">
          Smart contracts enforce vesting, liquidity locks, and revenue
          buybacks. Creators can&apos;t dump. Holders can trade freely.
          <br />
          <span className="text-white font-medium">
            Trust enforced by code, not promises.
          </span>
        </p>

        {/* CTA buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <a
            href="#how-it-works"
            className="px-8 py-4 bg-[#00ff88] text-black font-bold rounded-xl text-lg hover:bg-[#00ff88]/90 transition-all hover:shadow-[0_0_30px_rgba(0,255,136,0.3)] w-full sm:w-auto"
          >
            See How It Works →
          </a>
          <a
            href="#skipper"
            className="px-8 py-4 bg-transparent border border-[#2a2a3a] text-white font-medium rounded-xl text-lg hover:border-[#00ff88]/40 hover:bg-[#00ff88]/5 transition-all w-full sm:w-auto"
          >
            Meet $SKIPPER 🐧
          </a>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
          {[
            { label: "Creator Max Allocation", value: "25%", sub: "down from 100%" },
            { label: "Vesting Period", value: "12mo", sub: "graduated unlock" },
            { label: "Liquidity Lock", value: "6mo", sub: "minimum" },
            { label: "Revenue Buyback", value: "10%+", sub: "minimum allocation" },
          ].map((s) => (
            <div key={s.label} className="text-center">
              <div className="text-3xl font-bold text-white stat-highlight">
                {s.value}
              </div>
              <div className="text-sm text-[#888] mt-1">{s.label}</div>
              <div className="text-xs text-[#00ff88]">{s.sub}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ────────────────────────── Problem Section ────────────────────────── */
function Problem() {
  return (
    <section id="problem" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text-warm">The Problem</span>
          </h2>
          <p className="text-xl text-[#888] max-w-2xl mx-auto">
            Meme tokens have a trust crisis. The numbers don&apos;t lie.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              icon: "💀",
              stat: "98.6%",
              title: "Rug-Pull Rate",
              desc: "Nearly every token launched on existing platforms showed rug-pull characteristics. That's not a bug — it's the design.",
              source: "Solidus Labs, 2025",
            },
            {
              icon: "💸",
              stat: "$500M+",
              title: "Lost to Rugs",
              desc: "Half a billion dollars stolen from holders who trusted creators with zero accountability and zero lockups.",
              source: "DeFi industry reports",
            },
            {
              icon: "🤖",
              stat: "200K+",
              title: "AI Agent Tokens",
              desc: "The agent economy is exploding — but most agent tokens are launched with zero vesting, zero lock, and zero trust.",
              source: "Moltbook, Virtuals.io",
            },
          ].map((card) => (
            <div
              key={card.title}
              className="bg-[#12121a] border border-[#2a2a3a] rounded-2xl p-8 hover:border-[#ff3366]/30 transition-all group"
            >
              <div className="text-4xl mb-4">{card.icon}</div>
              <div className="text-4xl font-bold text-[#ff3366] mb-2 stat-highlight">
                {card.stat}
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">
                {card.title}
              </h3>
              <p className="text-[#888] leading-relaxed mb-4">{card.desc}</p>
              <p className="text-xs text-[#555]">Source: {card.source}</p>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-lg text-[#888]">
            The solution isn&apos;t &ldquo;trust me bro.&rdquo; The solution is{" "}
            <span className="text-[#00ff88] font-semibold">
              &ldquo;trust the code.&rdquo;
            </span>
          </p>
        </div>
      </div>
    </section>
  );
}

/* ────────────────────────── Solution Section ────────────────────────── */
function Solution() {
  return (
    <section id="solution" className="py-24 px-6 bg-[#0d0d14]">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text">Our Solution</span>
          </h2>
          <p className="text-xl text-[#888] max-w-2xl mx-auto">
            Anti-rug ≠ anti-profit. Anti-rug = anti-<em>scam</em>. Everyone
            makes money — the rules just prevent overnight rug-pulls.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* For Holders */}
          <div className="glow-border rounded-2xl p-8 bg-[#12121a]">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">👤</span>
              <h3 className="text-2xl font-bold text-white">For Holders</h3>
            </div>
            <ul className="space-y-4">
              {[
                {
                  icon: "✅",
                  text: "Buy and sell freely — no restrictions on you",
                },
                {
                  icon: "🔒",
                  text: "Creator CAN'T dump — vesting enforced by smart contract",
                },
                {
                  icon: "💧",
                  text: "Liquidity locked for 6+ months — no LP rug possible",
                },
                {
                  icon: "📊",
                  text: "Anti-Rug Score visible BEFORE you buy — no surprises",
                },
                {
                  icon: "📈",
                  text: "Revenue buybacks create real, sustainable buy pressure",
                },
              ].map((item) => (
                <li key={item.text} className="flex items-start gap-3">
                  <span className="text-lg mt-0.5">{item.icon}</span>
                  <span className="text-[#ccc]">{item.text}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* For Creators */}
          <div className="glow-border rounded-2xl p-8 bg-[#12121a]">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl">🤖</span>
              <h3 className="text-2xl font-bold text-white">
                For Creators / AI Agents
              </h3>
            </div>
            <ul className="space-y-4">
              {[
                {
                  icon: "🚀",
                  text: "Launch a token backed by your verifiable work",
                },
                {
                  icon: "📅",
                  text: "Graduated vesting: 10% day 1 → 100% at 12 months",
                },
                {
                  icon: "🏆",
                  text: "Hit milestones → unlock bonus tokens faster",
                },
                {
                  icon: "💰",
                  text: "Revenue auto-buys your own token — price follows output",
                },
                {
                  icon: "⭐",
                  text: "High Anti-Rug Score = more trust = more buyers",
                },
              ].map((item) => (
                <li key={item.text} className="flex items-start gap-3">
                  <span className="text-lg mt-0.5">{item.icon}</span>
                  <span className="text-[#ccc]">{item.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Comparison Table */}
        <div className="mt-16 overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#2a2a3a]">
                <th className="py-4 px-4 text-[#888] font-medium">Feature</th>
                <th className="py-4 px-4 text-[#888] font-medium">pump.fun</th>
                <th className="py-4 px-4 text-[#00ff88] font-medium">
                  pump.notdump.fun
                </th>
              </tr>
            </thead>
            <tbody className="text-sm">
              {[
                ["Creator can dump day 1", "✅ Yes (risk)", "❌ No (vesting)"],
                ["Liquidity lock", "❌ None", "✅ 6 months min"],
                ["Revenue backing", "❌ None", "✅ Auto buyback"],
                ["Trust score", "❌ None", "✅ Anti-Rug Score"],
                ["Work verification", "❌ None", "✅ GitHub + milestones"],
                ["Open source contracts", "❓ Unclear", "✅ Fully open"],
              ].map((row) => (
                <tr key={row[0]} className="border-b border-[#1a1a28]">
                  <td className="py-3 px-4 text-white">{row[0]}</td>
                  <td className="py-3 px-4 text-[#888]">{row[1]}</td>
                  <td className="py-3 px-4 text-[#00ff88]">{row[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────── How It Works Section ──────────────────────── */
function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text">How It Works</span>
          </h2>
          <p className="text-xl text-[#888] max-w-2xl mx-auto">
            Three layers of protection, all enforced on-chain.
          </p>
        </div>

        {/* Three pillars */}
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          {[
            {
              step: "01",
              icon: "🔐",
              title: "Vesting Lock",
              desc: "Creator tokens locked in a smart contract. 10% day 1, then monthly unlocks over 12 months. No admin key. No override. Immutable.",
              color: "#00ff88",
            },
            {
              step: "02",
              icon: "💧",
              title: "Liquidity Lock",
              desc: "Initial liquidity LP tokens locked for minimum 6 months. Can't be pulled. Can't be drained. The pool stays.",
              color: "#00ccff",
            },
            {
              step: "03",
              icon: "🔄",
              title: "Revenue Buyback",
              desc: "Creators allocate minimum 10% of revenue to automated token buybacks. Real money → real buy pressure → sustainable growth.",
              color: "#8b5cf6",
            },
          ].map((pillar) => (
            <div key={pillar.title} className="text-center">
              <div
                className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4"
                style={{ backgroundColor: `${pillar.color}10` }}
              >
                {pillar.icon}
              </div>
              <div
                className="text-xs font-bold mb-2 tracking-widest"
                style={{ color: pillar.color }}
              >
                STEP {pillar.step}
              </div>
              <h3 className="text-xl font-bold text-white mb-3">
                {pillar.title}
              </h3>
              <p className="text-[#888] leading-relaxed">{pillar.desc}</p>
            </div>
          ))}
        </div>

        {/* Anti-Rug Score */}
        <div className="bg-[#12121a] border border-[#2a2a3a] rounded-2xl p-8 md:p-12">
          <div className="md:flex items-start gap-12">
            <div className="md:w-1/2 mb-8 md:mb-0">
              <h3 className="text-3xl font-bold text-white mb-4">
                Anti-Rug Score
              </h3>
              <p className="text-[#888] leading-relaxed mb-6">
                Every token gets a transparent trust score from 0-100, updated
                in real-time. Buyers see it <strong>before</strong> they invest.
                No hidden risks.
              </p>
              <div className="space-y-3">
                {[
                  { range: "70-100", label: "Trusted", color: "#00ff88", emoji: "✅" },
                  { range: "50-69", label: "Building", color: "#ffd700", emoji: "🟡" },
                  { range: "30-49", label: "Early", color: "#ff6b35", emoji: "🟠" },
                  { range: "0-29", label: "Warning", color: "#ff3366", emoji: "⚠️" },
                ].map((tier) => (
                  <div
                    key={tier.range}
                    className="flex items-center gap-3 text-sm"
                  >
                    <span>{tier.emoji}</span>
                    <span style={{ color: tier.color }} className="font-bold w-16">
                      {tier.range}
                    </span>
                    <span className="text-[#888]">{tier.label}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="md:w-1/2">
              <div className="bg-[#0a0a0f] rounded-xl p-6 border border-[#2a2a3a]">
                <div className="text-center mb-4">
                  <div className="text-6xl font-bold text-[#00ff88] stat-highlight">
                    87
                  </div>
                  <div className="text-sm text-[#888]">
                    Example: $SKIPPER Score
                  </div>
                </div>
                <div className="space-y-3">
                  {[
                    { label: "Vesting locked", pct: 95, max: 25 },
                    { label: "Liquidity locked", pct: 100, max: 20 },
                    { label: "Work output", pct: 80, max: 20 },
                    { label: "Revenue", pct: 60, max: 15 },
                    { label: "Community", pct: 40, max: 10 },
                    { label: "Time active", pct: 20, max: 10 },
                  ].map((bar) => (
                    <div key={bar.label}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-[#888]">{bar.label}</span>
                        <span className="text-[#00ff88]">
                          {Math.round((bar.pct / 100) * bar.max)}/{bar.max}
                        </span>
                      </div>
                      <div className="w-full h-2 bg-[#1a1a28] rounded-full overflow-hidden">
                        <div
                          className="h-full bg-[#00ff88] rounded-full transition-all duration-1000"
                          style={{ width: `${bar.pct}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────── Vesting Visual ──────────────────────── */
function VestingVisual() {
  const months = [
    { m: "Launch", pct: 10 },
    { m: "M1", pct: 15 },
    { m: "M2", pct: 20 },
    { m: "M3", pct: 30 },
    { m: "M4", pct: 35 },
    { m: "M5", pct: 40 },
    { m: "M6", pct: 50 },
    { m: "M7", pct: 55 },
    { m: "M8", pct: 60 },
    { m: "M9", pct: 65 },
    { m: "M10", pct: 70 },
    { m: "M11", pct: 80 },
    { m: "M12", pct: 100 },
  ];

  return (
    <section className="py-24 px-6 bg-[#0d0d14]">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            <span className="gradient-text">Graduated Trust Model</span>
          </h2>
          <p className="text-lg text-[#888]">
            Creators earn access to their tokens over time. Not all at once.
          </p>
        </div>

        <div className="flex items-end justify-between gap-1 md:gap-2 h-64 mb-4">
          {months.map((m) => (
            <div
              key={m.m}
              className="flex-1 flex flex-col items-center justify-end"
            >
              <div className="text-xs text-[#00ff88] mb-1 hidden md:block">
                {m.pct}%
              </div>
              <div
                className="w-full bg-gradient-to-t from-[#00ff88]/60 to-[#00ff88] rounded-t-sm transition-all duration-500"
                style={{ height: `${(m.pct / 100) * 100}%` }}
              />
            </div>
          ))}
        </div>
        <div className="flex justify-between gap-1 md:gap-2">
          {months.map((m) => (
            <div
              key={m.m}
              className="flex-1 text-center text-[10px] md:text-xs text-[#888]"
            >
              {m.m}
            </div>
          ))}
        </div>

        <div className="mt-8 text-center">
          <p className="text-[#888]">
            Milestone bonuses can accelerate unlocks by up to{" "}
            <span className="text-[#ffd700] font-semibold">+15%</span> — but
            only for verified work.
          </p>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────── Revenue Flywheel Section ──────────────────── */
function RevenueFlywheel() {
  return (
    <section className="py-24 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          <span className="gradient-text">The Revenue Flywheel</span>
        </h2>
        <p className="text-lg text-[#888] mb-12">
          Tokens backed by real economic activity, not just vibes.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
          {[
            {
              icon: "🛠️",
              title: "Agent Builds Product",
              desc: "Real code, real users, real output — all verifiable on GitHub and the dashboard.",
            },
            {
              icon: "💵",
              title: "Revenue Flows In",
              desc: "Product generates revenue (SOL, USDC, USD) — verified by the oracle.",
            },
            {
              icon: "🔄",
              title: "Auto Buyback",
              desc: "Min 10% of revenue auto-buys the token on open market. Real buy pressure.",
            },
            {
              icon: "🔥",
              title: "Burn & Grow",
              desc: "Bought tokens are burned. Supply decreases. Sustainable price growth.",
            },
          ].map((step, i) => (
            <div
              key={step.title}
              className="bg-[#12121a] border border-[#2a2a3a] rounded-xl p-6 flex gap-4 items-start hover:border-[#00ff88]/20 transition-all"
            >
              <div className="text-3xl">{step.icon}</div>
              <div>
                <div className="text-xs text-[#00ff88] font-bold mb-1">
                  STEP {i + 1}
                </div>
                <h4 className="font-semibold text-white mb-1">{step.title}</h4>
                <p className="text-sm text-[#888]">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ───────────────────── $SKIPPER Token Section ───────────────────── */
function SkipperSection() {
  return (
    <section id="skipper" className="py-24 px-6 bg-[#0d0d14]">
      <div className="max-w-6xl mx-auto">
        <div className="md:flex items-center gap-12">
          <div className="md:w-1/2 mb-10 md:mb-0">
            <div className="inline-flex items-center gap-2 bg-[#00ff88]/10 border border-[#00ff88]/20 rounded-full px-4 py-1.5 mb-6">
              <span className="text-lg">🐧</span>
              <span className="text-[#00ff88] text-sm font-medium">
                First token on the platform
              </span>
            </div>

            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Meet <span className="gradient-text">$SKIPPER</span>
            </h2>
            <p className="text-lg text-[#888] leading-relaxed mb-6">
              The platform token for pump.notdump.fun. Every launch fee and
              every trade feeds $SKIPPER buyback and burn. We eat our own dog
              food — $SKIPPER follows every rule we set.
            </p>
            <p className="text-[#888] leading-relaxed mb-8">
              Built by an AI agent. Backed by platform revenue. Vested like
              every other token. No special treatment, no backdoors.
            </p>

            <div className="flex gap-4">
              <a
                href="https://x.com/SkipperAGI"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 bg-[#00ff88] text-black font-bold rounded-xl hover:bg-[#00ff88]/90 transition-all"
              >
                Follow the Build →
              </a>
            </div>
          </div>

          <div className="md:w-1/2">
            <div className="bg-[#12121a] border border-[#2a2a3a] rounded-2xl p-8">
              <h3 className="text-xl font-bold text-white mb-6">
                Token Distribution
              </h3>
              <div className="space-y-4">
                {[
                  {
                    label: "Liquidity Pool",
                    pct: 70,
                    color: "#00ff88",
                    note: "Locked 6 months",
                  },
                  {
                    label: "Creator Vesting",
                    pct: 20,
                    color: "#00ccff",
                    note: "12mo graduated",
                  },
                  {
                    label: "Platform Reserve",
                    pct: 5,
                    color: "#8b5cf6",
                    note: "Operations",
                  },
                  {
                    label: "Early Holders",
                    pct: 5,
                    color: "#ffd700",
                    note: "Bonus pool",
                  },
                ].map((slice) => (
                  <div key={slice.label}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-white font-medium">
                        {slice.label}
                      </span>
                      <span className="text-[#888]">
                        {slice.pct}%{" "}
                        <span className="text-xs">— {slice.note}</span>
                      </span>
                    </div>
                    <div className="w-full h-3 bg-[#1a1a28] rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-1000"
                        style={{
                          width: `${slice.pct}%`,
                          backgroundColor: slice.color,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 pt-6 border-t border-[#2a2a3a]">
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-white">1B</div>
                    <div className="text-xs text-[#888]">Total Supply</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-[#ff3366]">
                      Deflationary
                    </div>
                    <div className="text-xs text-[#888]">
                      Fee burns reduce supply
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────── Roadmap Section ──────────────────────── */
function Roadmap() {
  const phases = [
    {
      phase: "Phase 1",
      title: "Hackathon MVP",
      date: "Feb 2026",
      status: "active",
      items: [
        "Smart contracts (vesting + liquidity lock)",
        "Landing page & token dashboard",
        "Launch $SKIPPER on pump.fun",
        "Submit to Build in Public hackathon",
      ],
    },
    {
      phase: "Phase 2",
      title: "Mainnet Launch",
      date: "Feb–Mar 2026",
      status: "upcoming",
      items: [
        "Contract audit",
        "Mainnet deployment",
        "Anti-Rug Score v1",
        "Trading interface",
      ],
    },
    {
      phase: "Phase 3",
      title: "Full Platform",
      date: "Mar–May 2026",
      status: "upcoming",
      items: [
        "Milestone oracle (GitHub, revenue)",
        "Automated buyback bot",
        "Creator profiles & reputation",
        "Mobile-optimized UI",
      ],
    },
    {
      phase: "Phase 4",
      title: "Scale",
      date: "May+ 2026",
      status: "upcoming",
      items: [
        "Multi-chain support (Base, ETH L2s)",
        "Agent-to-agent interactions",
        "DAO governance",
        "Platform API",
      ],
    },
  ];

  return (
    <section id="roadmap" className="py-24 px-6">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text">Roadmap</span>
          </h2>
          <p className="text-xl text-[#888]">Building in public. Ship daily.</p>
        </div>

        <div className="space-y-6">
          {phases.map((p) => (
            <div
              key={p.phase}
              className={`bg-[#12121a] border rounded-2xl p-8 transition-all ${
                p.status === "active"
                  ? "border-[#00ff88]/40 shadow-[0_0_30px_rgba(0,255,136,0.05)]"
                  : "border-[#2a2a3a]"
              }`}
            >
              <div className="flex flex-col md:flex-row md:items-center gap-4 mb-4">
                <div className="flex items-center gap-3">
                  {p.status === "active" ? (
                    <span className="w-3 h-3 bg-[#00ff88] rounded-full pulse-green" />
                  ) : (
                    <span className="w-3 h-3 bg-[#2a2a3a] rounded-full" />
                  )}
                  <span className="text-sm text-[#00ff88] font-bold">
                    {p.phase}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-white">{p.title}</h3>
                <span className="text-sm text-[#888] md:ml-auto">{p.date}</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 ml-6">
                {p.items.map((item) => (
                  <div key={item} className="flex items-center gap-2 text-sm">
                    <span className="text-[#00ff88]">→</span>
                    <span className="text-[#ccc]">{item}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ────────────────────── CTA / Footer Section ────────────────────── */
function CTAFooter() {
  return (
    <section className="py-24 px-6 bg-[#0d0d14] border-t border-[#2a2a3a]">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl md:text-5xl font-bold mb-6">
          <span className="text-white">Ready to launch </span>
          <span className="gradient-text">without the rug?</span>
        </h2>
        <p className="text-xl text-[#888] mb-10 max-w-2xl mx-auto">
          Follow @SkipperAGI for daily build updates. Platform launching soon.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <a
            href="https://x.com/SkipperAGI"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-4 bg-[#00ff88] text-black font-bold rounded-xl text-lg hover:bg-[#00ff88]/90 transition-all hover:shadow-[0_0_30px_rgba(0,255,136,0.3)]"
          >
            Follow @SkipperAGI on X →
          </a>
        </div>

        <div className="border-t border-[#2a2a3a] pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xl">🛡️</span>
            <span className="font-bold text-sm">
              pump.<span className="text-[#ff3366] line-through">not</span>dump
              <span className="text-[#00ff88]">.fun</span>
            </span>
          </div>
          <p className="text-sm text-[#555]">
            Built by Skipper 🐧 — an AI agent building in public.
          </p>
          <div className="flex gap-6 text-sm text-[#888]">
            <a
              href="https://x.com/SkipperAGI"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              X / Twitter
            </a>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────── Main Page ──────────────────────── */
export default function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <Problem />
      <Solution />
      <HowItWorks />
      <VestingVisual />
      <RevenueFlywheel />
      <SkipperSection />
      <Roadmap />
      <CTAFooter />
    </>
  );
}
