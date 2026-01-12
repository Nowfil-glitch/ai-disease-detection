'use client'

import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Terminal } from 'lucide-react'
import GlassCard from './GlassCard'

interface AIConsoleProps {
  messages: string[]
}

// Typing animation component
function TypewriterText({ text, onComplete }: { text: string; onComplete?: () => void }) {
  const [displayedText, setDisplayedText] = useState('')
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    setDisplayedText('')
    setIsComplete(false)

    let currentIndex = 0
    const typingSpeed = 25 // ms per character

    const typeInterval = setInterval(() => {
      if (currentIndex < text.length) {
        setDisplayedText(text.slice(0, currentIndex + 1))
        currentIndex++
      } else {
        clearInterval(typeInterval)
        setIsComplete(true)
        onComplete?.()
      }
    }, typingSpeed)

    return () => clearInterval(typeInterval)
  }, [text, onComplete])

  return (
    <span className="console-text">
      {displayedText}
      {!isComplete && (
        <span className="inline-block w-2 h-4 bg-echo-crimson dark:bg-echo-blue-pale ml-0.5 animate-pulse" />
      )}
    </span>
  )
}

export default function AIConsole({ messages }: AIConsoleProps) {
  const consoleEndRef = useRef<HTMLDivElement>(null)
  const [completedMessages, setCompletedMessages] = useState<Set<number>>(new Set())

  useEffect(() => {
    consoleEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Reset completed messages when messages array changes significantly
  useEffect(() => {
    if (messages.length === 0) {
      setCompletedMessages(new Set())
    }
  }, [messages.length])

  const handleMessageComplete = (index: number) => {
    setCompletedMessages(prev => new Set([...prev, index]))
  }

  return (
    <GlassCard className="min-h-[300px]">
      <div className="space-y-4">
        <div className="flex items-center gap-3 border-b border-echo-gray-mid/20 dark:border-echo-gray-dark pb-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-echo-crimson/10 to-echo-pink/10 dark:from-echo-blue-dark/20 dark:to-echo-blue-pale/20">
            <Terminal className="w-5 h-5 text-echo-crimson dark:text-echo-blue-pale icon-pulse" />
          </div>
          <div>
            <h3 className="text-lg font-display font-bold text-echo-charcoal dark:text-white">
              AI Console
            </h3>
            <p className="text-xs text-echo-gray-mid">Real-time analysis log</p>
          </div>
          <div className="ml-auto flex items-center gap-1.5">
            <motion.span
              animate={{ scale: messages.length > 0 ? [1, 1.2, 1] : 1 }}
              transition={{ duration: 1, repeat: messages.length > 0 ? Infinity : 0 }}
              className="w-3 h-3 rounded-full bg-echo-crimson/80 dark:bg-echo-crimson"
            />
            <span className="w-3 h-3 rounded-full bg-yellow-500/80"></span>
            <motion.span
              animate={{ opacity: completedMessages.size === messages.length && messages.length > 0 ? 1 : 0.5 }}
              className="w-3 h-3 rounded-full bg-green-500/80"
            />
          </div>
        </div>

        <div className="bg-echo-charcoal dark:bg-echo-black rounded-xl p-4 min-h-[220px] max-h-[400px] overflow-y-auto font-mono text-sm border border-echo-gray-darker/50 scrollbar-thin">
          {/* Initial boot sequence */}
          {messages.length > 0 && (
            <div className="mb-4 text-echo-gray-mid/60 text-xs">
              <div>KNAZ AI Tech v2.0.1</div>
              <div>Initializing neural network...</div>
              <div className="text-green-500/80">● System ready</div>
              <div className="border-b border-echo-gray-darker/50 my-2" />
            </div>
          )}

          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20, y: 10 }}
                animate={{ opacity: 1, x: 0, y: 0 }}
                transition={{ duration: 0.3, ease: "easeOut" }}
                className="mb-3 flex items-start gap-2"
              >
                <span className="text-echo-gray-mid select-none">{`>`}</span>
                {completedMessages.has(index) ? (
                  <span className="console-text">{message}</span>
                ) : (
                  <TypewriterText
                    text={message}
                    onComplete={() => handleMessageComplete(index)}
                  />
                )}
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={consoleEndRef} />

          {messages.length > 0 && completedMessages.size === messages.length && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: [1, 0.2, 1] }}
              transition={{ duration: 0.8, repeat: Infinity }}
              className="inline-block w-2.5 h-5 bg-echo-crimson dark:bg-echo-blue-pale ml-1 rounded-sm"
            />
          )}
        </div>

        {/* Progress indicator */}
        {messages.length > 0 && (
          <div className="flex items-center gap-2 text-xs text-echo-gray-mid">
            <div className="flex-1 h-1 bg-echo-gray-darker/50 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-echo-crimson to-echo-pink dark:from-echo-blue-dark dark:to-echo-blue-pale rounded-full"
                initial={{ width: '0%' }}
                animate={{ width: `${(completedMessages.size / messages.length) * 100}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
            <span>{completedMessages.size}/{messages.length} tasks</span>
          </div>
        )}
      </div>
    </GlassCard>
  )
}
