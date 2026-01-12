'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Layers } from 'lucide-react'
import Image from 'next/image'

interface HeatmapViewerProps {
  imageUrl: string
}

export default function HeatmapViewer({ imageUrl }: HeatmapViewerProps) {
  const [opacity, setOpacity] = useState(0.6)

  // Generate a simple heatmap overlay using canvas gradient
  const generateHeatmap = () => {
    return (
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute inset-0"
          style={{
            background: `radial-gradient(circle at 60% 45%, rgba(255, 0, 0, ${opacity}) 0%, rgba(255, 165, 0, ${opacity * 0.7}) 25%, rgba(255, 255, 0, ${opacity * 0.5}) 40%, transparent 70%)`,
            mixBlendMode: 'multiply'
          }}
        />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-echo-crimson/10 dark:bg-echo-blue-dark/20">
          <Layers className="w-5 h-5 text-echo-crimson dark:text-echo-blue-pale icon-bounce" />
        </div>
        <h3 className="text-lg font-display font-bold text-echo-charcoal dark:text-white">
          Activation Heatmap
        </h3>
      </div>

      {/* Image with heatmap overlay */}
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative rounded-xl overflow-hidden bg-echo-gray-light dark:bg-echo-charcoal border border-echo-gray-mid/20 dark:border-echo-gray-dark"
      >
        <Image
          src={imageUrl}
          alt="Medical image with heatmap"
          width={800}
          height={600}
          className="w-full h-auto max-h-96 object-contain"
          unoptimized
        />
        {generateHeatmap()}
      </motion.div>

      {/* Opacity slider */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-echo-gray-dark dark:text-echo-gray-mid">
          <span className="font-medium">Heatmap Opacity</span>
          <span className="font-semibold">{Math.round(opacity * 100)}%</span>
        </div>
        <input
          type="range"
          min="0"
          max="100"
          value={opacity * 100}
          onChange={(e) => setOpacity(Number(e.target.value) / 100)}
          className="w-full h-2 bg-echo-gray-light dark:bg-echo-gray-darker rounded-lg appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, #c4343c 0%, #c4343c ${opacity * 100}%, #f2f2f2 ${opacity * 100}%, #f2f2f2 100%)`
          }}
        />
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-echo-crimson shadow-sm" />
          <span className="text-echo-gray-dark dark:text-echo-gray-mid">High Attention</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-yellow-500 shadow-sm" />
          <span className="text-echo-gray-dark dark:text-echo-gray-mid">Medium</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-transparent border-2 border-echo-gray-mid/30" />
          <span className="text-echo-gray-dark dark:text-echo-gray-mid">Low</span>
        </div>
      </div>
    </div>
  )
}
