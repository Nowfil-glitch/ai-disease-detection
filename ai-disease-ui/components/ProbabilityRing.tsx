'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

interface ProbabilityRingProps {
  confidence: number
}

export default function ProbabilityRing({ confidence }: ProbabilityRingProps) {
  const [displayConfidence, setDisplayConfidence] = useState(0)
  const radius = 80
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (displayConfidence / 100) * circumference

  useEffect(() => {
    const timer = setTimeout(() => {
      let current = 0
      const interval = setInterval(() => {
        current += 1
        setDisplayConfidence(current)
        if (current >= confidence) {
          clearInterval(interval)
        }
      }, 20)
      return () => clearInterval(interval)
    }, 300)
    
    return () => clearTimeout(timer)
  }, [confidence])

  const getColor = () => {
    if (displayConfidence >= 80) return '#c4343c' // echo crimson
    if (displayConfidence >= 60) return '#e10878' // echo pink
    return '#2562a0' // echo blue
  }

  const getStatus = () => {
    if (displayConfidence >= 80) return 'High Risk'
    if (displayConfidence >= 60) return 'Moderate Risk'
    return 'Low Risk'
  }

  return (
    <div className="flex flex-col items-center space-y-6">
      <div className="relative w-52 h-52">
        {/* Outer glow */}
        <div 
          className="absolute inset-0 rounded-full blur-xl opacity-30"
          style={{ backgroundColor: getColor() }}
        />
        
        <svg className="w-52 h-52 transform -rotate-90 relative">
          {/* Background circle */}
          <circle
            cx="104"
            cy="104"
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="10"
            className="text-echo-gray-light dark:text-echo-gray-darker"
          />
          
          {/* Progress circle */}
          <motion.circle
            cx="104"
            cy="104"
            r={radius}
            fill="none"
            stroke={getColor()}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.5, ease: 'easeOut' }}
            style={{
              filter: `drop-shadow(0 0 12px ${getColor()})`
            }}
          />
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.5, type: 'spring', stiffness: 200 }}
            className="text-center"
          >
            <div className="text-5xl font-display font-bold" style={{ color: getColor() }}>
              {displayConfidence}%
            </div>
            <div className="text-sm text-echo-gray-mid dark:text-echo-gray-mid text-center mt-2 font-medium">
              Confidence Score
            </div>
          </motion.div>
        </div>
      </div>

      {/* Status badge */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1, type: 'spring' }}
        className="px-8 py-3 rounded-full font-display font-semibold text-white shadow-lg"
        style={{ 
          backgroundColor: getColor(),
          boxShadow: `0 4px 20px ${getColor()}50`
        }}
      >
        {getStatus()}
      </motion.div>
    </div>
  )
}
