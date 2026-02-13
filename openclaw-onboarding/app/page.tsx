'use client'

import { useState, useEffect, useCallback, useRef } from 'react'

interface Slide {
  title: string
  subtitle?: string
  bullets: string[]
  code?: string
  narration: string
  visual?: 'orb' | 'checklist' | 'terminal' | 'chat' | 'heartbeat' | 'brain' | 'agents' | 'cron' | 'soul' | 'finale'
}

const slides: Slide[] = [
  // SECTION 1: SETUP
  {
    title: 'Welcome to OpenClaw',
    subtitle: 'Your Personal AI Assistant',
    bullets: [
      'In the next few minutes, I\'ll walk you through setting everything up.',
      'By the end, you\'ll have your own AI running 24/7.',
      'Let\'s get started.'
    ],
    narration: 'Welcome to OpenClaw, your personal AI assistant. In the next few minutes, I\'ll walk you through setting everything up. By the end, you\'ll have your own AI running 24 7 on your computer. Let\'s get started.',
    visual: 'orb'
  },
  {
    title: 'What You\'ll Need',
    subtitle: 'Quick Checklist',
    bullets: [
      '✓ A Mac Mini or any Mac or Linux computer',
      '✓ An internet connection',
      '✓ A phone number for WhatsApp (recommended)',
      '✓ An Anthropic API key (I\'ll show you how)',
    ],
    narration: 'Here\'s what you\'ll need. A Mac Mini or any Mac or Linux computer. An internet connection. A phone number for WhatsApp, which is recommended but optional. And an Anthropic API key. Don\'t worry, I\'ll show you exactly how to get one.',
    visual: 'checklist'
  },
  {
    title: 'Installing OpenClaw',
    subtitle: 'One Command — That\'s It',
    bullets: [
      'Open Terminal on your Mac',
      'Copy and paste this command:',
      'It installs everything automatically',
      'Takes about 2 minutes'
    ],
    code: 'curl -fsSL https://openclaw.ai/install.sh | bash',
    narration: 'Open Terminal on your Mac. You can find it in Applications, then Utilities. Then copy and paste this one command. It installs everything automatically, including Node JS and all dependencies. The whole process takes about 2 minutes.',
    visual: 'terminal'
  },
  {
    title: 'Running the Setup Wizard',
    subtitle: 'Configure Your AI',
    bullets: [
      'The wizard asks you a few simple questions',
      'Choose Anthropic as your AI provider',
      'Get your API key at console.anthropic.com',
      'The gateway starts running — your AI\'s brain'
    ],
    code: 'openclaw onboard --install-daemon',
    narration: 'Next, run the onboarding wizard. It asks you a few simple questions. Choose Anthropic as your AI provider, that\'s Claude. Get your API key at console dot anthropic dot com. Sign up, create a key, and paste it in. The wizard then starts the gateway. That\'s your AI\'s brain, running 24 7 in the background.',
    visual: 'terminal'
  },
  {
    title: 'Connecting WhatsApp',
    subtitle: 'Chat With Your AI Anywhere',
    bullets: [
      'Run the login command to get a QR code',
      'On your phone: WhatsApp → Settings → Linked Devices',
      'Scan the QR code — done!',
      'Pro tip: Use a separate number for your AI'
    ],
    code: 'openclaw channels login',
    narration: 'Now let\'s connect WhatsApp so you can chat with your AI from anywhere. Run the login command and a QR code appears in your terminal. On your phone, open WhatsApp, go to Settings, then Linked Devices, and scan the QR code. That\'s it. Pro tip: use a separate phone number for your AI if possible. An old phone with a cheap sim card works great.',
    visual: 'chat'
  },
  {
    title: 'Your First Message',
    subtitle: 'Say Hello',
    bullets: [
      'Send a WhatsApp message to your AI\'s number',
      'It responds instantly',
      'Try: "What can you help me with?"',
      'Your AI is alive!'
    ],
    narration: 'Now for the exciting part. Send a WhatsApp message to the number you just linked. Your AI responds instantly. Try asking, What can you help me with? Congratulations. Your AI is alive and ready to work for you.',
    visual: 'chat'
  },
  {
    title: 'You\'re All Set!',
    subtitle: 'Your AI Runs 24/7',
    bullets: [
      'Your assistant is running on your Mac Mini',
      'It stays online as long as the computer is on',
      'Keep it connected to WiFi and power',
      'Next: Let\'s learn how your AI actually works...'
    ],
    narration: 'You\'re all set! Your AI assistant is now running 24 7 on your Mac Mini. It stays online as long as the computer is on and connected to WiFi. Just keep it plugged in and connected. Now let\'s learn how your AI actually works behind the scenes.',
    visual: 'orb'
  },
  // SECTION 2: HOW IT WORKS
  {
    title: 'The Heartbeat',
    subtitle: 'Your AI\'s Pulse',
    bullets: [
      'Every few hours, your AI wakes up automatically',
      'It checks on tasks, monitors your schedule',
      'Scans for things that need attention',
      'Works proactively — you don\'t have to ask'
    ],
    narration: 'Your AI has a heartbeat, just like you. Every few hours, it wakes up automatically and checks on things. It monitors your schedule, scans for tasks that need attention, and works proactively. You don\'t have to ask it to check. It just does.',
    visual: 'heartbeat'
  },
  {
    title: 'Memory',
    subtitle: 'It Remembers Everything',
    bullets: [
      'Conversations, preferences, decisions — all stored',
      'MEMORY.md stores long-term facts about you',
      'Daily logs track what happens each day',
      'This is what makes it YOUR assistant'
    ],
    narration: 'Your AI remembers everything. Conversations, preferences, decisions, all stored in memory files. Memory dot MD stores long-term facts about you. Daily logs track what happens each day. This is what makes it your assistant, not just any chatbot. The more you use it, the better it knows you.',
    visual: 'brain'
  },
  {
    title: 'Agents & Delegation',
    subtitle: 'Your AI Has a Team',
    bullets: [
      'Your AI can spawn sub-agents for complex tasks',
      'Like a CEO delegating work to specialists',
      'Research, coding, analysis — handled in parallel',
      'Your main AI stays focused on you'
    ],
    narration: 'Your AI can spawn sub-agents for complex tasks. Think of it like a CEO delegating work to specialists. Need research? A sub-agent handles it. Need code written? Another sub-agent. They work in parallel while your main AI stays focused on you.',
    visual: 'agents'
  },
  {
    title: 'Crons & Automation',
    subtitle: 'Set It and Forget It',
    bullets: [
      'Crons are scheduled tasks that run automatically',
      'Morning briefings, reminders, market scans',
      'Set them once — they run forever',
      'Your AI works even when you\'re not chatting'
    ],
    narration: 'Crons are scheduled tasks that run automatically. Morning briefings, appointment reminders, market scans. You set them once and they run forever. Your AI works 24 7 even when you\'re not chatting with it. It\'s always on, always working.',
    visual: 'cron'
  },
  {
    title: 'Personality',
    subtitle: 'Make It Yours',
    bullets: [
      'Your AI has a personality file called SOUL.md',
      'Edit it to change how your AI talks and thinks',
      'Make it formal, casual, funny — your choice',
      'Give it a name. Make it yours.'
    ],
    narration: 'Your AI has a personality file called Soul dot MD. Edit it to change how your AI talks, thinks, and behaves. Make it formal, casual, funny, whatever fits you. Give it a name. This is your assistant. Make it truly yours.',
    visual: 'soul'
  },
  {
    title: 'Welcome to the Future',
    subtitle: 'Your AI Journey Starts Now',
    bullets: [
      'You now have a personal AI running 24/7',
      'It remembers, it learns, it works while you sleep',
      'The more you use it, the better it gets',
      'Welcome to OpenClaw.'
    ],
    narration: 'You now have a personal AI assistant running 24 7. It remembers. It learns. It works while you sleep. The more you use it, the better it gets. Welcome to OpenClaw. Your AI journey starts now.',
    visual: 'finale'
  },
]

function OrbVisual() {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="w-32 h-32 rounded-full bg-gradient-to-br from-amber-500 to-orange-600 pulse-glow flex items-center justify-center">
        <div className="w-24 h-24 rounded-full bg-gradient-to-br from-amber-400 to-yellow-500 opacity-80" />
      </div>
    </div>
  )
}

function HeartbeatVisual() {
  return (
    <div className="flex items-center justify-center py-8">
      <svg viewBox="0 0 200 60" className="w-64 h-20">
        <polyline
          fill="none"
          stroke="#f59e0b"
          strokeWidth="2"
          points="0,30 40,30 50,10 60,50 70,30 80,30 100,30 110,10 120,50 130,30 140,30 160,30 170,10 180,50 190,30 200,30"
          className="animate-pulse"
        />
      </svg>
    </div>
  )
}

function TerminalVisual({ code }: { code?: string }) {
  return (
    <div className="mx-auto max-w-sm my-6">
      <div className="bg-[#1a1a2e] rounded-lg border border-[#333] overflow-hidden">
        <div className="flex items-center gap-1.5 px-3 py-2 bg-[#111128]">
          <div className="w-2.5 h-2.5 rounded-full bg-red-500/80" />
          <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/80" />
          <div className="w-2.5 h-2.5 rounded-full bg-green-500/80" />
          <span className="text-[10px] text-gray-500 ml-2">Terminal</span>
        </div>
        <div className="p-4">
          <p className="text-green-400 text-xs font-mono mb-1">$</p>
          <p className="text-amber-400 text-sm font-mono break-all typing-cursor">{code}</p>
        </div>
      </div>
    </div>
  )
}

function ChatVisual() {
  return (
    <div className="mx-auto max-w-xs my-6 space-y-3">
      <div className="flex justify-end">
        <div className="bg-green-700/40 border border-green-600/30 rounded-2xl rounded-br-sm px-4 py-2 max-w-[80%]">
          <p className="text-sm text-white">What can you help me with?</p>
        </div>
      </div>
      <div className="flex justify-start">
        <div className="bg-[#222] border border-[#333] rounded-2xl rounded-bl-sm px-4 py-2 max-w-[80%]">
          <p className="text-sm text-gray-200">I can help with scheduling, research, reminders, writing, and much more. What do you need?</p>
        </div>
      </div>
    </div>
  )
}

function AgentsVisual() {
  return (
    <div className="flex items-center justify-center py-6 gap-3">
      <div className="flex flex-col items-center gap-1">
        <div className="w-14 h-14 rounded-full bg-amber-500/20 border-2 border-amber-500/50 flex items-center justify-center text-lg">🧠</div>
        <span className="text-[10px] text-amber-400">Main AI</span>
      </div>
      <div className="text-gray-600 text-xs mt-[-16px]">→</div>
      <div className="flex flex-col gap-2">
        {['🔍 Research', '💻 Code', '📊 Analysis'].map((a, i) => (
          <div key={i} className="flex items-center gap-2 bg-[#1a1a1a] border border-[#333] rounded-lg px-3 py-1.5">
            <span className="text-xs">{a}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function SlideVisual({ visual, code }: { visual?: string; code?: string }) {
  switch (visual) {
    case 'orb': case 'finale': return <OrbVisual />
    case 'heartbeat': return <HeartbeatVisual />
    case 'terminal': return <TerminalVisual code={code} />
    case 'chat': return <ChatVisual />
    case 'agents': return <AgentsVisual />
    case 'brain': return (
      <div className="flex items-center justify-center py-8">
        <div className="w-28 h-28 rounded-full bg-purple-500/20 border-2 border-purple-500/40 flex items-center justify-center text-4xl pulse-glow">🧠</div>
      </div>
    )
    case 'cron': return (
      <div className="flex items-center justify-center py-8">
        <div className="w-28 h-28 rounded-full bg-blue-500/20 border-2 border-blue-500/40 flex items-center justify-center text-4xl pulse-glow">⏰</div>
      </div>
    )
    case 'soul': return (
      <div className="flex items-center justify-center py-8">
        <div className="w-28 h-28 rounded-full bg-pink-500/20 border-2 border-pink-500/40 flex items-center justify-center text-4xl pulse-glow">✨</div>
      </div>
    )
    case 'checklist': return null // bullets serve as checklist
    default: return null
  }
}

export default function OnboardingPage() {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [autoPlay, setAutoPlay] = useState(true)
  const [started, setStarted] = useState(false)
  const synthRef = useRef<SpeechSynthesis | null>(null)
  const utterRef = useRef<SpeechSynthesisUtterance | null>(null)

  useEffect(() => {
    if (typeof window !== 'undefined') {
      synthRef.current = window.speechSynthesis
    }
  }, [])

  const speak = useCallback((text: string) => {
    if (!synthRef.current || isMuted) return
    synthRef.current.cancel()
    const utter = new SpeechSynthesisUtterance(text)
    utter.rate = 0.95
    utter.pitch = 1.05
    // Find a good female voice
    const voices = synthRef.current.getVoices()
    const preferred = voices.find(v => v.name.includes('Samantha')) ||
      voices.find(v => v.name.includes('Karen')) ||
      voices.find(v => v.name.includes('Victoria')) ||
      voices.find(v => v.name.toLowerCase().includes('female')) ||
      voices.find(v => v.lang.startsWith('en') && v.name.includes('Google')) ||
      voices.find(v => v.lang.startsWith('en'))
    if (preferred) utter.voice = preferred
    utter.onstart = () => setIsSpeaking(true)
    utter.onend = () => {
      setIsSpeaking(false)
      if (autoPlay && currentSlide < slides.length - 1) {
        setTimeout(() => setCurrentSlide(prev => prev + 1), 1500)
      }
    }
    utterRef.current = utter
    synthRef.current.speak(utter)
  }, [isMuted, autoPlay, currentSlide])

  useEffect(() => {
    if (started && !isMuted) {
      // Small delay to let animations start
      const timer = setTimeout(() => speak(slides[currentSlide].narration), 800)
      return () => clearTimeout(timer)
    }
  }, [currentSlide, started])

  const goTo = (idx: number) => {
    synthRef.current?.cancel()
    setIsSpeaking(false)
    setCurrentSlide(idx)
  }

  const toggleMute = () => {
    if (!isMuted) {
      synthRef.current?.cancel()
      setIsSpeaking(false)
    }
    setIsMuted(!isMuted)
  }

  const slide = slides[currentSlide]
  const isSetupSection = currentSlide < 7
  const sectionLabel = isSetupSection ? 'Part 1: Setup' : 'Part 2: How It Works'

  if (!started) {
    return (
      <div className="h-dvh flex flex-col items-center justify-center px-6 text-center">
        <div className="w-24 h-24 rounded-full bg-gradient-to-br from-amber-500 to-orange-600 pulse-glow flex items-center justify-center mb-8">
          <div className="w-18 h-18 rounded-full bg-gradient-to-br from-amber-400 to-yellow-500 opacity-80 w-16 h-16" />
        </div>
        <h1 className="text-3xl font-bold text-white mb-3">OpenClaw</h1>
        <p className="text-gray-400 text-lg mb-2">Your Personal AI Assistant</p>
        <p className="text-gray-500 text-sm mb-10 max-w-xs">An interactive guide to setting up and understanding your AI</p>
        <button
          onClick={() => setStarted(true)}
          className="px-8 py-4 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-2xl text-lg transition-all active:scale-95"
        >
          Begin Setup Guide
        </button>
        <p className="text-gray-600 text-xs mt-4">~10 minutes • Includes voice narration</p>
      </div>
    )
  }

  return (
    <div className="h-dvh flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#222]">
        <span className="text-[11px] text-amber-500 font-medium">{sectionLabel}</span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setAutoPlay(!autoPlay)}
            className={`text-[10px] px-2 py-1 rounded ${autoPlay ? 'bg-amber-500/15 text-amber-400' : 'bg-white/5 text-gray-500'}`}
          >
            {autoPlay ? 'Auto ▶' : 'Manual'}
          </button>
          <button
            onClick={toggleMute}
            className={`text-[10px] px-2 py-1 rounded ${isMuted ? 'bg-red-500/15 text-red-400' : 'bg-white/5 text-gray-400'}`}
          >
            {isMuted ? '🔇 Muted' : '🔊 Sound'}
          </button>
        </div>
      </div>

      {/* Slide Content */}
      <div className="flex-1 overflow-y-auto px-6 py-6" key={currentSlide}>
        {/* Section divider */}
        {currentSlide === 7 && (
          <div className="text-center mb-6 animate-fade-in-up">
            <div className="inline-block px-4 py-1.5 bg-blue-500/10 border border-blue-500/20 rounded-full">
              <span className="text-blue-400 text-xs font-medium">Part 2: How Your AI Works</span>
            </div>
          </div>
        )}

        <div className="max-w-lg mx-auto">
          {/* Title */}
          <div className="animate-fade-in-up text-center mb-1">
            <h1 className="text-2xl font-bold text-white">{slide.title}</h1>
            {slide.subtitle && <p className="text-amber-400 text-sm mt-1">{slide.subtitle}</p>}
          </div>

          {/* Visual */}
          <div className="animate-fade-in-up-delay-1">
            <SlideVisual visual={slide.visual} code={slide.code} />
          </div>

          {/* Code block (if not terminal visual) */}
          {slide.code && slide.visual !== 'terminal' && (
            <div className="animate-fade-in-up-delay-2 my-4 bg-[#1a1a2e] rounded-lg p-3 border border-[#333]">
              <code className="text-amber-400 text-sm font-mono break-all">{slide.code}</code>
            </div>
          )}

          {/* Bullets */}
          <div className="space-y-3 mt-6">
            {slide.bullets.map((bullet, i) => (
              <div
                key={i}
                className={`animate-fade-in-up-delay-${Math.min(i + 2, 5)} flex items-start gap-3`}
              >
                <div className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-2 flex-shrink-0" />
                <p className="text-gray-300 text-[15px] leading-relaxed">{bullet}</p>
              </div>
            ))}
          </div>

          {/* Speaking indicator */}
          {isSpeaking && (
            <div className="flex items-center justify-center gap-1.5 mt-6">
              {[0,1,2,3,4].map(i => (
                <div key={i} className="w-1 bg-amber-500 rounded-full animate-pulse" style={{
                  height: `${12 + Math.random() * 16}px`,
                  animationDelay: `${i * 0.15}s`
                }} />
              ))}
            </div>
          )}

          {/* Final slide CTA */}
          {currentSlide === slides.length - 1 && (
            <div className="mt-8 flex flex-col items-center gap-3 animate-fade-in-up-delay-5">
              <a
                href="https://docs.openclaw.ai"
                target="_blank"
                className="px-6 py-3 bg-amber-500 text-black font-bold rounded-xl hover:bg-amber-400 transition-all"
              >
                Visit Documentation →
              </a>
              <button
                onClick={() => goTo(0)}
                className="text-gray-500 text-sm hover:text-white transition-colors"
              >
                Start Over
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Nav */}
      <div className="border-t border-[#222] px-4 py-3">
        {/* Progress bar */}
        <div className="flex gap-1 mb-3">
          {slides.map((_, i) => (
            <button
              key={i}
              onClick={() => goTo(i)}
              className={`h-1 rounded-full flex-1 transition-all ${
                i === currentSlide ? 'bg-amber-500' :
                i < currentSlide ? 'bg-amber-500/30' : 'bg-white/10'
              }`}
            />
          ))}
        </div>

        {/* Nav buttons */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => goTo(Math.max(0, currentSlide - 1))}
            disabled={currentSlide === 0}
            className="px-4 py-2 text-gray-400 hover:text-white disabled:opacity-20 transition-colors text-sm"
          >
            ← Back
          </button>
          <span className="text-gray-600 text-xs">{currentSlide + 1} / {slides.length}</span>
          <button
            onClick={() => goTo(Math.min(slides.length - 1, currentSlide + 1))}
            disabled={currentSlide === slides.length - 1}
            className="px-4 py-2 bg-amber-500/15 text-amber-400 hover:bg-amber-500/25 rounded-lg disabled:opacity-20 transition-colors text-sm font-medium"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  )
}
