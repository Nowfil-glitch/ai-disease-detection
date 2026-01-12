import { ReactNode } from 'react'
import { motion } from 'framer-motion'

interface GlassCardProps {
  children: ReactNode
  className?: string
  hoverable?: boolean
  variant?: 'default' | 'frosted' | 'gradient-border' | 'gradient-pulse'
}

export default function GlassCard({ 
  children, 
  className = '', 
  hoverable = true,
  variant = 'default'
}: GlassCardProps) {
  const getVariantClasses = () => {
    switch (variant) {
      case 'frosted':
        return 'glass-frosted glass-noise'
      case 'gradient-border':
        return 'gradient-border'
      case 'gradient-pulse':
        return 'gradient-border-pulse'
      default:
        return 'glass-card'
    }
  }

  return (
    <motion.div
      whileHover={hoverable ? { scale: 1.01, y: -4 } : {}}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`${getVariantClasses()} rounded-2xl p-6 md:p-8 card-tilt ${className}`}
    >
      {children}
    </motion.div>
  )
}
