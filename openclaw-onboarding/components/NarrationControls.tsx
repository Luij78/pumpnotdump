'use client';

import { useEffect, useRef, useState } from 'react';
import { Play, Pause, Volume2, VolumeX } from 'lucide-react';

interface NarrationControlsProps {
  narrationText: string;
  isNarrating: boolean;
  setIsNarrating: (value: boolean) => void;
  isMuted: boolean;
  setIsMuted: (value: boolean) => void;
  skipNarration: boolean;
  setSkipNarration: (value: boolean) => void;
  onNarrationEnd: () => void;
}

export function NarrationControls({
  narrationText,
  isNarrating,
  setIsNarrating,
  isMuted,
  setIsMuted,
  skipNarration,
  setSkipNarration,
  onNarrationEnd,
}: NarrationControlsProps) {
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [selectedVoice, setSelectedVoice] = useState<SpeechSynthesisVoice | null>(null);

  // Load available voices
  useEffect(() => {
    const loadVoices = () => {
      const availableVoices = window.speechSynthesis.getVoices();
      setVoices(availableVoices);

      // Try to find the best female voice
      const preferredVoices = [
        'Samantha', // macOS
        'Victoria', // macOS
        'Fiona', // macOS
        'Karen', // macOS
        'Google US English Female', // Chrome
        'Microsoft Zira', // Windows
        'female', // Generic fallback
      ];

      let bestVoice = availableVoices.find(voice =>
        preferredVoices.some(preferred => voice.name.toLowerCase().includes(preferred.toLowerCase()))
      );

      // Fallback to any female voice
      if (!bestVoice) {
        bestVoice = availableVoices.find(voice =>
          voice.name.toLowerCase().includes('female')
        );
      }

      // Final fallback to first English voice
      if (!bestVoice) {
        bestVoice = availableVoices.find(voice => voice.lang.startsWith('en'));
      }

      if (bestVoice) {
        setSelectedVoice(bestVoice);
      }
    };

    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;

    return () => {
      window.speechSynthesis.onvoiceschanged = null;
    };
  }, []);

  // Auto-play narration when slide changes (unless skipped or muted)
  useEffect(() => {
    if (!skipNarration && !isMuted && selectedVoice) {
      // Small delay to let slide animation start
      const timer = setTimeout(() => {
        playNarration();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [narrationText, selectedVoice]);

  const playNarration = () => {
    if (isMuted) return;

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(narrationText);
    
    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }
    
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onstart = () => {
      setIsNarrating(true);
    };

    utterance.onend = () => {
      setIsNarrating(false);
      onNarrationEnd();
    };

    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setIsNarrating(false);
    };

    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  };

  const pauseNarration = () => {
    window.speechSynthesis.cancel();
    setIsNarrating(false);
  };

  const toggleMute = () => {
    if (!isMuted) {
      window.speechSynthesis.cancel();
      setIsNarrating(false);
    }
    setIsMuted(!isMuted);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      window.speechSynthesis.cancel();
    };
  }, []);

  return (
    <div className="flex items-center justify-center gap-4 mb-4 px-4">
      {/* Play/Pause button */}
      <button
        onClick={isNarrating ? pauseNarration : playNarration}
        disabled={isMuted}
        className="p-3 rounded-full bg-purple-600 hover:bg-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        aria-label={isNarrating ? 'Pause narration' : 'Play narration'}
      >
        {isNarrating ? (
          <Pause className="w-5 h-5" />
        ) : (
          <Play className="w-5 h-5" />
        )}
      </button>

      {/* Mute toggle */}
      <button
        onClick={toggleMute}
        className="p-3 rounded-full bg-white/10 hover:bg-white/20 transition-all"
        aria-label={isMuted ? 'Unmute' : 'Mute'}
      >
        {isMuted ? (
          <VolumeX className="w-5 h-5" />
        ) : (
          <Volume2 className="w-5 h-5" />
        )}
      </button>

      {/* Skip narration toggle */}
      <label className="flex items-center gap-2 cursor-pointer text-sm text-gray-400 hover:text-gray-300 transition-colors">
        <input
          type="checkbox"
          checked={skipNarration}
          onChange={(e) => setSkipNarration(e.target.checked)}
          className="w-4 h-4 rounded border-gray-600 bg-white/10"
        />
        Skip auto-advance
      </label>
    </div>
  );
}
