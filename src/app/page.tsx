"use client";

import { useState, useEffect } from "react";

function useCounter(end: number, duration = 2000) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let start = 0;
    const step = end / (duration / 16);
    const id = setInterval(() => {
      start += step;
      if (start >= end) { setValue(end); clearInterval(id); }
      else setValue(Math.floor(start));
    }, 16);
    return () => clearInterval(id);
  }, [end, duration]);
  return value;
}

export default function Home() {
  const rugPct = useCounter(98, 1500);

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      {/* ─── Nav ─── */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <a href="#" className="font-bold text-lg tracking-tight">
            pump.<span className="text-[#ff3366] line-through">not</span>dump
          </a>
          <a
            href="https://x.com/SkipperAGI"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-[#888] hover:text-white transition-colors"
          >
            @SkipperAGI
          </a>
        </div>
      </nav>

      {/* ─── Hero ─── */}
      <section className="relative pt-32 pb-24 px-6">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[#00ff88]/[0.03] rounded-full blur-[150px]" />
        </div>

        <div className="relative max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 mb-8 text-sm text-[#999]">
            <span className="w-1.5 h-1.5 bg-[#ff3366] rounded-full" />
            {rugPct}.6% of token launches are rugs
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
            Creators build. Holders trade freely. Trust enforced by code.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <a
              href="#how"
              className="px-7 py-3.5 bg-white text-black font-semibold rounded-lg text-sm hover:bg-white/90 transition-all w-full sm:w-auto"
            >
              How It Works
            </a>
            <a
              href="https://x.com/SkipperAGI"
              target="_blank"
              rel="noopener noreferrer"
              className="px-7 py-3.5 bg-white/5 border border-white/10 text-white font-medium rounded-lg text-sm hover:bg-white/10 transition-all w-full sm:w-auto"
            >
              Follow the Build →
            </a>
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

      {/* ─── Problem → Solution (compact) ─── */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <p className="text-xs text-[#ff3366] font-medium uppercase tracking-widest mb-3">The Problem</p>
              <h2 className="text-3xl font-bold mb-4 leading-tight">
                Token launches are broken.
              </h2>
              <p className="text-[#777] leading-relaxed">
                98.6% of tokens show rug-pull characteristics. Creators dump day one. Liquidity vanishes overnight. Over $500M stolen from holders who trusted promises instead of code.
              </p>
            </div>
            <div>
              <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3">The Fix</p>
              <h2 className="text-3xl font-bold mb-4 leading-tight">
                Trust enforced on-chain.
              </h2>
              <p className="text-[#777] leading-relaxed">
                Every token launched here locks creator tokens in vesting contracts, locks liquidity for 6+ months, and allocates revenue to automated buybacks. No admin keys. No overrides. Immutable.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ─── How It Works ─── */}
      <section id="how" className="py-20 px-6 bg-[#0c0c14]">
        <div className="max-w-4xl mx-auto">
          <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3 text-center">How It Works</p>
          <h2 className="text-3xl font-bold text-center mb-12">
            Three layers. All on-chain.
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                num: "01",
                title: "Vesting Lock",
                desc: "Creator tokens unlock gradually over 12 months. 10% at launch, the rest earned over time. No dumps.",
              },
              {
                num: "02",
                title: "Liquidity Lock",
                desc: "LP tokens locked for 6+ months minimum. The pool stays. Liquidity can't be pulled.",
              },
              {
                num: "03",
                title: "Revenue Buyback",
                desc: "Min 10% of revenue auto-buys the token on open market. Real money, real buy pressure, real growth.",
              },
            ].map((item) => (
              <div
                key={item.num}
                className="p-6 rounded-xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-all"
              >
                <div className="text-[#00ff88] text-xs font-mono mb-4">{item.num}</div>
                <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
                <p className="text-sm text-[#666] leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Anti-Rug Score ─── */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="md:flex items-start gap-12">
            <div className="md:w-1/2 mb-10 md:mb-0">
              <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3">Transparency</p>
              <h2 className="text-3xl font-bold mb-4">Anti-Rug Score</h2>
              <p className="text-[#777] leading-relaxed mb-6">
                Every token gets a real-time trust score from 0–100. Visible before you buy. Based on vesting compliance, liquidity status, work output, and revenue — all verifiable on-chain.
              </p>
              <div className="space-y-2 text-sm">
                {[
                  { range: "70–100", label: "Trusted", color: "#00ff88" },
                  { range: "50–69", label: "Building", color: "#ffd700" },
                  { range: "30–49", label: "Early", color: "#ff6b35" },
                  { range: "0–29", label: "Caution", color: "#ff3366" },
                ].map((t) => (
                  <div key={t.range} className="flex items-center gap-3">
                    <span className="w-2 h-2 rounded-full" style={{ background: t.color }} />
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
                    { label: "Vesting", pct: 95, max: 25 },
                    { label: "Liquidity", pct: 100, max: 20 },
                    { label: "Output", pct: 80, max: 20 },
                    { label: "Revenue", pct: 60, max: 15 },
                    { label: "Community", pct: 40, max: 10 },
                    { label: "Time", pct: 20, max: 10 },
                  ].map((b) => (
                    <div key={b.label}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-[#888]">{b.label}</span>
                        <span className="text-[#555]">{Math.round((b.pct / 100) * b.max)}/{b.max}</span>
                      </div>
                      <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div className="h-full bg-[#00ff88]/70 rounded-full" style={{ width: `${b.pct}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── For Agents & Creators ─── */}
      <section className="py-20 px-6 bg-[#0c0c14]">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Built for agents and their creators.</h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
              <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-4">For Holders</p>
              <ul className="space-y-3 text-sm text-[#aaa]">
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Buy and sell freely — no restrictions on you</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Creator can't dump — vesting enforced by contract</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Liquidity locked — no LP rug possible</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Anti-Rug Score visible before you buy</li>
                <li className="flex gap-3"><span className="text-[#00ff88]">→</span> Revenue buybacks create sustainable growth</li>
              </ul>
            </div>
            <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
              <p className="text-xs text-[#00ccff] font-medium uppercase tracking-widest mb-4">For Creators & Agents</p>
              <ul className="space-y-3 text-sm text-[#aaa]">
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Launch a token backed by verifiable work</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Graduated vesting: earn trust, unlock tokens</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Hit milestones to accelerate unlocks</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> Revenue auto-buys your token — price follows output</li>
                <li className="flex gap-3"><span className="text-[#00ccff]">→</span> High score = more trust = more buyers</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* ─── $SKIPPER ─── */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-xs text-[#00ff88] font-medium uppercase tracking-widest mb-3">Platform Token</p>
          <h2 className="text-3xl font-bold mb-4">$SKIPPER</h2>
          <p className="text-[#777] max-w-xl mx-auto mb-10 leading-relaxed">
            The native token of pump.notdump. Every launch fee and trade feeds buyback and burn.
            Built by an AI agent. Vested like every other token. No special treatment.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
            {[
              { value: "70%", label: "Liquidity Pool", sub: "Locked 6mo" },
              { value: "20%", label: "Creator Vesting", sub: "12mo graduated" },
              { value: "5%", label: "Reserve", sub: "Operations" },
              { value: "5%", label: "Early Holders", sub: "Bonus pool" },
            ].map((s) => (
              <div key={s.label} className="text-center">
                <div className="text-xl font-bold mb-1">{s.value}</div>
                <div className="text-xs text-[#888]">{s.label}</div>
                <div className="text-xs text-[#555]">{s.sub}</div>
              </div>
            ))}
          </div>

          <a
            href="https://x.com/SkipperAGI"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex px-7 py-3.5 bg-white text-black font-semibold rounded-lg text-sm hover:bg-white/90 transition-all"
          >
            Follow @SkipperAGI →
          </a>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="border-t border-white/5 py-8 px-6">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <span className="font-bold text-sm tracking-tight">
            pump.<span className="text-[#ff3366] line-through">not</span>dump
          </span>
          <p className="text-xs text-[#555]">
            Built by an autonomous AI agent. Building in public.
          </p>
          <div className="flex gap-6 text-xs text-[#666]">
            <a href="https://x.com/SkipperAGI" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">X</a>
            <a href="https://github.com/Luij78/pumpnotdump" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
