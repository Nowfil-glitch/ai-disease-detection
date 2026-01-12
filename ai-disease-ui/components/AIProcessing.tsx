'use client'

import { motion } from 'framer-motion'
import GlassCard from './GlassCard'

export default function AIProcessing() {
  return (
    <GlassCard className="flex items-center justify-center min-h-[300px]">
      <div className="text-center space-y-8">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          className="relative w-36 h-36 mx-auto"
        >
          {/* Outer glow ring */}
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-echo-crimson/20 to-echo-pink/20 dark:from-echo-blue-dark/20 dark:to-echo-blue-pale/20 blur-xl" />
          
          {/* Outer ring */}
          <div className="absolute inset-0 border-4 border-echo-crimson/20 dark:border-echo-blue-pale/20 rounded-full" />
          
          {/* Animated ring */}
          <svg className="absolute inset-0 w-36 h-36" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke="url(#echo-gradient)"
              strokeWidth="4"
              strokeLinecap="round"
              strokeDasharray="180 80"
            />
            <defs>
              <linearGradient id="echo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#c4343c" />
                <stop offset="50%" stopColor="#e10878" />
                <stop offset="100%" stopColor="#2562a0" />
              </linearGradient>
            </defs>
          </svg>
          
          {/* Inner pulse */}
          <motion.div
            animate={{ scale: [1, 1.15, 1], opacity: [0.4, 0.7, 0.4] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="absolute inset-6 bg-gradient-to-br from-echo-crimson/15 to-echo-blue-dark/15 dark:from-echo-blue-pale/15 dark:to-echo-pink/15 rounded-full"
          />
          
          {/* Center icon */}
          <motion.div
            animate={{ scale: [0.95, 1.05, 0.95] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-echo-crimson to-echo-pink dark:from-echo-blue-dark dark:to-echo-blue-pale flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
          </motion.div>
        </motion.div>

        <div className="space-y-2">
          <h3 className="text-xl font-display font-bold text-echo-charcoal dark:text-white">
            AI Processing
          </h3>
          <p className="text-echo-gray-mid dark:text-echo-gray-mid">
            Analyzing your medical image...
          </p>
        </div>

        {/* Animated dots */}
        <div className="flex justify-center gap-3">
          {[0, 1, 2, 3].map((i) => (
            <motion.div
              key={i}
              animate={{ 
                y: [0, -12, 0],
                opacity: [0.5, 1, 0.5]
              }}
              transition={{
                duration: 0.8,
                repeat: Infinity,
                delay: i * 0.15,
                ease: "easeInOut"
              }}
              className="w-2.5 h-2.5 bg-gradient-to-r from-echo-crimson to-echo-pink dark:from-echo-blue-dark dark:to-echo-blue-pale rounded-full"
            />
          ))}
        </div>
      </div>
    </GlassCard>
  )
}
