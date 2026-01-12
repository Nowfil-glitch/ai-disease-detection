'use client'

import { useEffect, useState, useRef } from 'react'

interface Particle {
  x: number
  y: number
  size: number
  speedX: number
  speedY: number
  opacity: number
  color: string
}

export default function SplineBackground() {
  const [mounted, setMounted] = useState(false)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const particlesRef = useRef<Particle[]>([])
  const animationRef = useRef<number>()
  const mouseRef = useRef({ x: 0, y: 0 })

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!mounted) return

    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Particle colors (Deep Navy to Cyan palette)
    const colors = [
      'rgba(40, 184, 213, 0.7)',   // cyan
      'rgba(95, 212, 235, 0.6)',   // cyan-light
      'rgba(160, 232, 245, 0.5)',  // cyan-pale
      'rgba(30, 144, 200, 0.6)',   // blue-accent
      'rgba(255, 255, 255, 0.4)',  // white
    ]

    // Initialize particles - optimized for performance
    const initParticles = () => {
      const particles: Particle[] = []
      // Reduced particle count for better performance (max 25 particles)
      const particleCount = Math.min(25, Math.floor((canvas.width * canvas.height) / 50000))

      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 2 + 1,
          speedX: (Math.random() - 0.5) * 0.3,
          speedY: (Math.random() - 0.5) * 0.3,
          opacity: Math.random() * 0.4 + 0.2,
          color: colors[Math.floor(Math.random() * colors.length)]
        })
      }
      particlesRef.current = particles
    }
    initParticles()

    // Mouse move handler
    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current = { x: e.clientX, y: e.clientY }
    }
    window.addEventListener('mousemove', handleMouseMove)

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      particlesRef.current.forEach((particle, index) => {
        // Update position
        particle.x += particle.speedX
        particle.y += particle.speedY

        // Mouse interaction - simplified for performance
        const dx = mouseRef.current.x - particle.x
        const dy = mouseRef.current.y - particle.y
        const distanceSquared = dx * dx + dy * dy
        if (distanceSquared < 22500) { // 150^2
          const force = 0.015
          particle.x -= dx * force
          particle.y -= dy * force
        }

        // Wrap around edges
        if (particle.x < 0) particle.x = canvas.width
        if (particle.x > canvas.width) particle.x = 0
        if (particle.y < 0) particle.y = canvas.height
        if (particle.y > canvas.height) particle.y = 0

        // Draw particle
        ctx.beginPath()
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
        ctx.fillStyle = particle.color
        ctx.fill()

        // Draw connections between nearby particles - optimized (only check every 3rd particle)
        if (index % 2 === 0) {
          particlesRef.current.slice(index + 1).forEach((otherParticle, otherIndex) => {
            if (otherIndex % 2 !== 0) return // Skip every other particle for connections
            const dx = particle.x - otherParticle.x
            const dy = particle.y - otherParticle.y
            const distanceSquared = dx * dx + dy * dy

            if (distanceSquared < 10000) { // 100^2, avoid sqrt for performance
              ctx.beginPath()
              ctx.strokeStyle = `rgba(40, 184, 213, ${0.1 * (1 - Math.sqrt(distanceSquared) / 100)})`
              ctx.lineWidth = 0.5
              ctx.moveTo(particle.x, particle.y)
              ctx.lineTo(otherParticle.x, otherParticle.y)
              ctx.stroke()
            }
          })
        }
      })

      animationRef.current = requestAnimationFrame(animate)
    }
    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      window.removeEventListener('mousemove', handleMouseMove)
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [mounted])

  if (!mounted) return null

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {/* Deep Navy to Cyan gradient background */}
      <div className="absolute inset-0 bg-gradient-to-r from-echo-navy via-echo-navy-light to-echo-cyan dark:from-echo-navy dark:via-echo-navy-light dark:to-echo-cyan" />

      {/* Animated gradient mesh overlay */}
      <div className="absolute inset-0 opacity-40">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-echo-cyan/10 via-transparent to-echo-navy/20" />
      </div>

      {/* Particle canvas */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 pointer-events-none"
        style={{ opacity: 0.8 }}
      />

      {/* Animated orbs with Cyan/Navy colors - reduced for performance */}
      <div className="absolute top-1/4 left-1/4 w-[400px] h-[400px] bg-echo-cyan rounded-full mix-blend-screen filter blur-[80px] opacity-25 animate-blob" />
      <div className="absolute bottom-1/3 right-1/4 w-[350px] h-[350px] bg-echo-cyan-light rounded-full mix-blend-screen filter blur-[80px] opacity-20 animate-blob animation-delay-4000" />

      {/* Subtle grid pattern overlay */}
      <div className="absolute inset-0 opacity-[0.05]"
        style={{
          backgroundImage: `linear-gradient(rgba(40, 184, 213, 0.3) 1px, transparent 1px),
                           linear-gradient(90deg, rgba(40, 184, 213, 0.3) 1px, transparent 1px)`,
          backgroundSize: '50px 50px'
        }}
      />

      {/* Radial gradient spotlight */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-echo-cyan/20 via-transparent to-transparent rounded-full" />

      {/* Floating particles (CSS) - reduced to 3 for performance */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(3)].map((_, i) => (
          <div
            key={i}
            className={`absolute w-2 h-2 rounded-full bg-echo-cyan/40 floating-particle floating-particle-${i + 1}`}
            style={{
              left: `${20 + i * 30}%`,
              top: `${25 + (i % 2) * 30}%`,
            }}
          />
        ))}
      </div>

      <style jsx>{`
        @keyframes blob {
          0%, 100% {
            transform: translate(0px, 0px) scale(1);
          }
          50% {
            transform: translate(20px, -20px) scale(1.02);
          }
        }
        .animate-blob {
          animation: blob 20s ease-in-out infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
        .animation-delay-6000 {
          animation-delay: 6s;
        }
        
        @keyframes float-up {
          0%, 100% {
            transform: translateY(0) translateX(0) scale(1);
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            transform: translateY(-100vh) translateX(50px) scale(0.5);
            opacity: 0;
          }
        }
        
        .floating-particle {
          animation: float-up linear infinite;
        }
        .floating-particle-1 { animation-duration: 20s; animation-delay: 0s; }
        .floating-particle-2 { animation-duration: 25s; animation-delay: 3s; }
        .floating-particle-3 { animation-duration: 22s; animation-delay: 6s; }
      `}</style>
    </div>
  )
}
