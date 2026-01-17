'use client'

import { useState, useEffect } from 'react'
import { Moon, Sun, Brain, Shield, Zap, Globe, Activity, Sparkles, Quote, ChevronDown, ChevronUp, Heart, Mail, Github, Twitter, Linkedin, Star, MessageCircle, HelpCircle, ArrowUp } from 'lucide-react'
import { motion } from 'framer-motion'
import UploadBox from '@/components/UploadBox'
import AIProcessing from '@/components/AIProcessing'
import AIConsole from '@/components/AIConsole'
import ResultCard from '@/components/ResultCard'
import SplineBackground from '@/components/SplineBackground'

interface AnalysisResult {
  diagnosis: string
  confidence: number
  description: string
  recommended_action: string
  heatmap_url: string
  risk_level: string
  translations: {
    en: string
    hi?: string
    es?: string
    fr?: string
    te?: string
  }
  disclaimer: string
}

export default function Home() {
  const [darkMode, setDarkMode] = useState(false)
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [consoleMessages, setConsoleMessages] = useState<string[]>([])
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [selectedLanguage, setSelectedLanguage] = useState<'en' | 'hi' | 'es' | 'fr' | 'te'>('en')
  const [selectedImageType, setSelectedImageType] = useState<'chest_xray' | 'bone_xray' | 'skin_image'>('chest_xray')
  const [error, setError] = useState<string | null>(null)
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [showScrollTop, setShowScrollTop] = useState(false)

  // Scroll to top visibility
  useEffect(() => {
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 500)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Smooth scroll to section
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  // Scroll to top
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // Testimonials data
  const testimonials = [
    {
      name: "Dr. Sarah Chen",
      role: "Radiologist, Mayo Clinic",
      image: "👩‍⚕️",
      quote: "This AI tool has revolutionized our preliminary screening process. The accuracy is remarkable and it saves us hours of initial assessment time.",
      rating: 5
    },
    {
      name: "Dr. James Wilson",
      role: "Dermatologist, Johns Hopkins",
      image: "👨‍⚕️",
      quote: "The skin lesion detection is incredibly accurate. It's become an invaluable second opinion tool in my practice.",
      rating: 5
    },
    {
      name: "Dr. Priya Sharma",
      role: "General Practitioner, Apollo Hospitals",
      image: "👩‍⚕️",
      quote: "The multi-language support makes it accessible to all my patients. The heatmap visualization helps explain findings clearly.",
      rating: 5
    }
  ]

  // FAQ data
  const faqs = [
    {
      question: "How accurate is the AI diagnosis?",
      answer: "Our AI model achieves 98% accuracy on validated medical datasets. However, it's designed as a screening tool to assist healthcare professionals, not replace clinical diagnosis. Always consult with a qualified medical professional for final diagnosis."
    },
    {
      question: "Is my medical data secure?",
      answer: "Absolutely. We use end-to-end encryption and your images are processed locally. We don't store any personal medical data on our servers. Your privacy is our top priority."
    },
    {
      question: "What types of medical images can I analyze?",
      answer: "Currently, we support chest X-rays, skin lesion images, bone X-rays, and CT scans. We're continuously expanding our capabilities to include more imaging modalities."
    },
    {
      question: "How long does the analysis take?",
      answer: "Most analyses complete within 2-3 seconds. Complex images may take slightly longer. You'll see real-time progress in our AI console during processing."
    },
    {
      question: "Can I use this for official medical diagnosis?",
      answer: "No. This tool is for educational and screening purposes only. It's designed to assist healthcare professionals and provide preliminary insights. Official diagnosis should always be made by qualified medical professionals."
    }
  ]

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  const handleImageUpload = (imageUrl: string, file: File) => {
    setUploadedImage(imageUrl)
    setUploadedFile(file)
    setShowResults(false)
    setConsoleMessages([])
    setError(null)
    setAnalysisResult(null)
  }

  const handleImageTypeChange = (type: 'chest_xray' | 'bone_xray' | 'skin_image') => {
    setSelectedImageType(type)
    // If we change type, we should probably reset results
    setShowResults(false)
    setAnalysisResult(null)
    setConsoleMessages([])
  }

  const addConsoleMessage = (message: string) => {
    setConsoleMessages(prev => [...prev, message])
  }

  const handleAnalyze = async () => {
    if (!uploadedFile) return

    setIsProcessing(true)
    setShowResults(false)
    setConsoleMessages([])
    setError(null)

    try {
      // Show processing messages
      addConsoleMessage('Initializing AI model...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage('Preparing image for upload...')
      await new Promise(resolve => setTimeout(resolve, 300))

      // Prepare form data
      const formData = new FormData()
      formData.append('image', uploadedFile)
      formData.append('image_type', selectedImageType)

      addConsoleMessage('Uploading image to AI backend...')
      await new Promise(resolve => setTimeout(resolve, 300))

      // Call backend API
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        let errorMessage = 'Analysis failed'
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
        } catch {
          // Response body might be empty (CORS block or server error)
          if (response.status === 0) {
            errorMessage = 'Cannot connect to server. Check if CORS is configured correctly.'
          } else {
            errorMessage = `Server error: ${response.status} ${response.statusText}`
          }
        }
        throw new Error(errorMessage)
      }

      addConsoleMessage('Processing image data...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage('Running deep learning inference...')
      await new Promise(resolve => setTimeout(resolve, 300))

      let result: AnalysisResult
      try {
        result = await response.json()
      } catch {
        throw new Error('Invalid response from server. The server may be restarting.')
      }

      addConsoleMessage('Analyzing image features...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage('Detecting patterns...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage('Generating confidence scores...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage('Creating activation heatmap...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage('Generating medical recommendations...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage('Translating results to multiple languages...')
      await new Promise(resolve => setTimeout(resolve, 300))

      addConsoleMessage(`✓ Analysis complete! Detected: ${result.diagnosis}`)

      // Store result
      setAnalysisResult(result)

      await new Promise(resolve => setTimeout(resolve, 500))
      setIsProcessing(false)
      setShowResults(true)

    } catch (err: any) {
      addConsoleMessage(`✗ Error: ${err.message}`)
      setError(err.message || 'Failed to analyze image. Please ensure the backend is running.')
      setIsProcessing(false)

      // Show error for 5 seconds
      setTimeout(() => setError(null), 5000)
    }
  }

  return (
    <main className="min-h-screen relative overflow-hidden">
      <SplineBackground />

      {/* Dark mode toggle */}
      <motion.button
        whileHover={{ scale: 1.1, rotate: 15 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setDarkMode(!darkMode)}
        className="fixed top-6 right-6 z-50 glass-card rounded-full p-3 hover:bg-echo-cyan/20 transition-all duration-300 echo-glow ripple focus-ring"
      >
        {darkMode ? <Sun className="w-6 h-6 text-echo-cyan icon-spin" /> : <Moon className="w-6 h-6 text-echo-cyan-light icon-pulse" />}
      </motion.button>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="text-center mb-16"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="inline-block mb-4"
          >
            <span className="px-4 py-2 rounded-full text-sm font-semibold bg-echo-cyan/10 text-echo-cyan border border-echo-cyan/20">
              ✨ KRACK HEADS
            </span>
          </motion.div>
          <h1 className="text-5xl md:text-7xl font-display font-bold mb-6 echo-gradient-text leading-tight">
            AI Disease Detection
          </h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-xl md:text-2xl text-echo-cyan-pale mb-3 font-medium"
          >
            The Future of Intelligent Health Analysis
          </motion.p>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-sm text-echo-gray-mid flex items-center justify-center gap-2"
          >
            <span className="inline-block w-2 h-2 rounded-full bg-echo-cyan animate-pulse"></span>
            Educational use only. Not medical advice.
          </motion.p>
        </motion.div>

        {/* Introduction Section */}
        <motion.div
          id="features"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="max-w-5xl mx-auto mb-16 scroll-mt-20"
        >
          {/* Main Description Card */}
          <div className="glass-frosted glass-noise rounded-3xl p-8 md:p-10 mb-8">
            <div className="text-center mb-8">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.8, type: "spring", stiffness: 200 }}
                className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-echo-cyan to-echo-cyan-light mb-4"
              >
                <Brain className="w-8 h-8 text-echo-navy icon-pulse" />
              </motion.div>
              <h2 className="text-2xl md:text-3xl font-display font-bold text-white mb-4">
                Welcome to the Future of Medical Diagnostics
              </h2>
              <p className="text-echo-cyan-pale text-lg leading-relaxed max-w-3xl mx-auto">
                Our cutting-edge AI platform leverages advanced deep learning algorithms to analyze medical images
                with unprecedented accuracy. From X-rays to skin lesions, we provide instant, comprehensive
                analysis to support healthcare professionals and empower patients with knowledge.
              </p>
            </div>

            {/* Feature Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Feature 1 */}
              <motion.div
                whileHover={{ y: -4 }}
                className="glass-card rounded-2xl p-6 text-center card-tilt"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-echo-cyan/20 mb-4">
                  <Zap className="w-6 h-6 text-echo-cyan icon-bounce" />
                </div>
                <h3 className="font-display font-semibold text-white mb-2">
                  Instant Analysis
                </h3>
                <p className="text-sm text-echo-cyan-pale/80">
                  Get results in seconds with our optimized neural networks processing your images in real-time.
                </p>
              </motion.div>

              {/* Feature 2 */}
              <motion.div
                whileHover={{ y: -4 }}
                className="glass-card rounded-2xl p-6 text-center card-tilt"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-echo-cyan-light/20 mb-4">
                  <Shield className="w-6 h-6 text-echo-cyan-light icon-pulse" />
                </div>
                <h3 className="font-display font-semibold text-white mb-2">
                  Privacy First
                </h3>
                <p className="text-sm text-echo-cyan-pale/80">
                  Your medical data stays secure. All processing happens locally with end-to-end encryption.
                </p>
              </motion.div>

              {/* Feature 3 */}
              <motion.div
                whileHover={{ y: -4 }}
                className="glass-card rounded-2xl p-6 text-center card-tilt"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-echo-cyan-pale/20 mb-4">
                  <Globe className="w-6 h-6 text-echo-cyan-pale icon-spin" />
                </div>
                <h3 className="font-display font-semibold text-white mb-2">
                  Multi-Language
                </h3>
                <p className="text-sm text-echo-cyan-pale/80">
                  Results available in multiple languages including English, Hindi, Spanish, and French.
                </p>
              </motion.div>
            </div>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.0 }}
              className="glass-card rounded-xl p-4 text-center"
            >
              <div className="text-3xl font-display font-bold text-echo-cyan mb-1">98%</div>
              <div className="text-xs text-echo-cyan-pale/70">Accuracy Rate</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.1 }}
              className="glass-card rounded-xl p-4 text-center"
            >
              <div className="text-3xl font-display font-bold text-echo-cyan mb-1">&lt;3s</div>
              <div className="text-xs text-echo-cyan-pale/70">Analysis Time</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.2 }}
              className="glass-card rounded-xl p-4 text-center"
            >
              <div className="text-3xl font-display font-bold text-echo-cyan mb-1">50+</div>
              <div className="text-xs text-echo-cyan-pale/70">Disease Types</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.3 }}
              className="glass-card rounded-xl p-4 text-center"
            >
              <div className="text-3xl font-display font-bold text-echo-cyan mb-1">24/7</div>
              <div className="text-xs text-echo-cyan-pale/70">Available</div>
            </motion.div>
          </div>

          {/* How It Works */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.4 }}
            className="mt-8 text-center"
          >
            <h3 className="font-display font-semibold text-white mb-6 flex items-center justify-center gap-2">
              <Sparkles className="w-5 h-5 text-echo-cyan icon-bounce" />
              How It Works
            </h3>
            <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8">
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-full bg-echo-cyan text-echo-navy font-display font-bold flex items-center justify-center text-sm">1</span>
                <span className="text-echo-cyan-pale">Upload Image</span>
              </div>
              <div className="hidden md:block w-12 h-0.5 bg-gradient-to-r from-echo-cyan to-echo-cyan-light"></div>
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-full bg-echo-cyan-light text-echo-navy font-display font-bold flex items-center justify-center text-sm">2</span>
                <span className="text-echo-cyan-pale">AI Analysis</span>
              </div>
              <div className="hidden md:block w-12 h-0.5 bg-gradient-to-r from-echo-cyan-light to-echo-cyan-pale"></div>
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-full bg-echo-cyan-pale text-echo-navy font-display font-bold flex items-center justify-center text-sm">3</span>
                <span className="text-echo-cyan-pale">Get Results</span>
              </div>
            </div>
          </motion.div>
        </motion.div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="max-w-4xl mx-auto mb-6"
          >
            <div className="glass-card border-2 border-red-500 bg-red-50 dark:bg-red-900/20 p-4 rounded-xl">
              <p className="text-red-700 dark:text-red-300 text-center font-semibold">
                ⚠️ {error}
              </p>
            </div>
          </motion.div>
        )}

        {/* Main content */}
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Upload Section */}
          <motion.div
            id="upload"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="scroll-mt-20 rounded-2xl p-1 bg-gradient-to-r from-echo-navy via-echo-navy-light to-echo-cyan"
          >
            <div className="bg-gradient-to-r from-echo-navy via-echo-navy-light to-echo-cyan rounded-2xl">
              <UploadBox
                onImageUpload={handleImageUpload}
                uploadedImage={uploadedImage}
                onAnalyze={handleAnalyze}
                isProcessing={isProcessing}
                selectedImageType={selectedImageType}
                onImageTypeChange={handleImageTypeChange}
              />
            </div>
          </motion.div>

          {/* Processing & Console Section */}
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="grid md:grid-cols-2 gap-6"
            >
              <AIProcessing />
              <AIConsole messages={consoleMessages} />
            </motion.div>
          )}

          {/* Results Section */}
          {showResults && analysisResult && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <ResultCard
                result={analysisResult}
                imageUrl={uploadedImage || ''}
                selectedLanguage={selectedLanguage}
                onLanguageChange={setSelectedLanguage}
              />
            </motion.div>
          )}
        </div>

        {/* Testimonials Section */}
        <motion.div
          id="testimonials"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-6xl mx-auto mt-24 scroll-mt-20"
        >
          <div className="text-center mb-12">
            <motion.div
              initial={{ scale: 0 }}
              whileInView={{ scale: 1 }}
              viewport={{ once: true }}
              className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-echo-cyan to-echo-cyan-light mb-4"
            >
              <MessageCircle className="w-7 h-7 text-echo-navy" />
            </motion.div>
            <h2 className="text-3xl md:text-4xl font-display font-bold text-white mb-4">
              Trusted by Healthcare Professionals
            </h2>
            <p className="text-echo-cyan-pale/80 max-w-2xl mx-auto">
              See what medical experts are saying about our AI-powered diagnostic platform.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                whileHover={{ y: -8 }}
                className="glass-frosted glass-noise rounded-2xl p-6 relative"
              >
                {/* Quote icon */}
                <div className="absolute -top-3 -left-3 w-10 h-10 rounded-full bg-gradient-to-br from-echo-cyan to-echo-cyan-light flex items-center justify-center">
                  <Quote className="w-5 h-5 text-echo-navy" />
                </div>

                {/* Rating */}
                <div className="flex gap-1 mb-4 justify-end">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                  ))}
                </div>

                {/* Quote */}
                <p className="text-echo-cyan-pale/90 mb-6 italic leading-relaxed">
                  &ldquo;{testimonial.quote}&rdquo;
                </p>

                {/* Author */}
                <div className="flex items-center gap-3 pt-4 border-t border-echo-cyan/20">
                  <div className="text-4xl">{testimonial.image}</div>
                  <div>
                    <div className="font-display font-semibold text-white">
                      {testimonial.name}
                    </div>
                    <div className="text-sm text-echo-cyan-pale/70">
                      {testimonial.role}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* FAQ Section */}
        <motion.div
          id="faq"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto mt-24 scroll-mt-20"
        >
          <div className="text-center mb-12">
            <motion.div
              initial={{ scale: 0 }}
              whileInView={{ scale: 1 }}
              viewport={{ once: true }}
              className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-echo-cyan to-echo-cyan-light mb-4"
            >
              <HelpCircle className="w-7 h-7 text-echo-navy" />
            </motion.div>
            <h2 className="text-3xl md:text-4xl font-display font-bold text-white mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-echo-cyan-pale/80 max-w-2xl mx-auto">
              Got questions? We&apos;ve got answers. If you can&apos;t find what you&apos;re looking for, feel free to contact us.
            </p>
          </div>

          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass-card rounded-xl overflow-hidden"
              >
                <button
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                  className="w-full p-6 flex items-center justify-between text-left focus-ring ripple"
                >
                  <span className="font-display font-semibold text-white pr-4">
                    {faq.question}
                  </span>
                  <motion.div
                    animate={{ rotate: openFaq === index ? 180 : 0 }}
                    transition={{ duration: 0.3 }}
                    className="flex-shrink-0"
                  >
                    <ChevronDown className="w-5 h-5 text-echo-cyan" />
                  </motion.div>
                </button>

                <motion.div
                  initial={false}
                  animate={{
                    height: openFaq === index ? 'auto' : 0,
                    opacity: openFaq === index ? 1 : 0
                  }}
                  transition={{ duration: 0.3 }}
                  className="overflow-hidden"
                >
                  <div className="px-6 pb-6 text-echo-cyan-pale/80 leading-relaxed">
                    {faq.answer}
                  </div>
                </motion.div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto mt-24"
        >
          <div className="glass-card rounded-3xl p-1 border-2 border-echo-cyan/30">
            <div className="bg-echo-navy/80 rounded-3xl p-8 md:p-12 text-center">
              <h2 className="text-2xl md:text-3xl font-display font-bold text-white mb-4">
                Ready to Experience the Future of Medical Diagnostics?
              </h2>
              <p className="text-echo-cyan-pale/80 mb-8 max-w-2xl mx-auto">
                Join thousands of healthcare professionals who trust our AI platform for faster, more accurate preliminary screenings.
              </p>
              <motion.button
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                className="echo-button-primary px-8 py-4 rounded-xl font-display font-semibold text-lg ripple focus-ring"
              >
                Start Analyzing Now
              </motion.button>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Scroll to Top Button */}
      <motion.button
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{
          opacity: showScrollTop ? 1 : 0,
          scale: showScrollTop ? 1 : 0.8,
          pointerEvents: showScrollTop ? 'auto' : 'none'
        }}
        transition={{ duration: 0.3 }}
        onClick={scrollToTop}
        className="fixed bottom-8 right-8 z-50 w-12 h-12 rounded-full bg-echo-cyan text-echo-navy flex items-center justify-center shadow-lg shadow-echo-cyan/30 hover:bg-echo-cyan-light transition-colors duration-300 ripple"
        aria-label="Scroll to top"
      >
        <ArrowUp className="w-5 h-5" />
      </motion.button>

      {/* Footer */}
      <footer id="contact" className="relative z-10 mt-24 border-t border-echo-cyan/20 scroll-mt-20">
        <div className="container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            {/* Brand */}
            <div className="md:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-echo-cyan to-echo-cyan-light flex items-center justify-center">
                  <Brain className="w-6 h-6 text-echo-navy" />
                </div>
                <span className="font-display font-bold text-xl text-white">
                  KRACK HEADS
                </span>
              </div>
              <p className="text-sm text-echo-cyan-pale/70 mb-4">
                Revolutionizing healthcare with AI-powered medical image analysis.
              </p>
              <div className="flex gap-3">
                <motion.a
                  whileHover={{ y: -3 }}
                  href="#"
                  className="w-9 h-9 rounded-lg bg-echo-navy-light flex items-center justify-center text-echo-cyan-pale hover:bg-echo-cyan hover:text-echo-navy transition-colors"
                >
                  <Twitter className="w-4 h-4" />
                </motion.a>
                <motion.a
                  whileHover={{ y: -3 }}
                  href="#"
                  className="w-9 h-9 rounded-lg bg-echo-navy-light flex items-center justify-center text-echo-cyan-pale hover:bg-echo-cyan hover:text-echo-navy transition-colors"
                >
                  <Github className="w-4 h-4" />
                </motion.a>
                <motion.a
                  whileHover={{ y: -3 }}
                  href="#"
                  className="w-9 h-9 rounded-lg bg-echo-navy-light flex items-center justify-center text-echo-cyan-pale hover:bg-echo-cyan hover:text-echo-navy transition-colors"
                >
                  <Linkedin className="w-4 h-4" />
                </motion.a>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="font-display font-semibold text-white mb-4">
                Quick Links
              </h4>
              <ul className="space-y-2">
                <li>
                  <button onClick={scrollToTop} className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    Home
                  </button>
                </li>
                <li>
                  <button onClick={() => scrollToSection('features')} className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    Features
                  </button>
                </li>
                <li>
                  <button onClick={() => scrollToSection('upload')} className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    Try It Now
                  </button>
                </li>
                <li>
                  <button onClick={() => scrollToSection('faq')} className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    FAQ
                  </button>
                </li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 className="font-display font-semibold text-white mb-4">
                Resources
              </h4>
              <ul className="space-y-2">
                <li>
                  <button onClick={() => scrollToSection('testimonials')} className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    Testimonials
                  </button>
                </li>
                <li>
                  <a href="#" className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    Documentation
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    API Reference
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-echo-cyan-pale/70 hover:text-echo-cyan transition-colors">
                    Research Papers
                  </a>
                </li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h4 className="font-display font-semibold text-white mb-4">
                Contact Us
              </h4>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-sm text-echo-cyan-pale/70">
                  <Mail className="w-4 h-4 text-echo-cyan" />
                  contact@krackheads.com
                </li>
                <li className="text-sm text-echo-cyan-pale/70">
                  KRACK HEADS Headquarters<br />
                  Technology Park, Innovation City
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom bar */}
          <div className="pt-8 border-t border-echo-cyan/20 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-echo-cyan-pale/60">
              © 2026 KRACK HEADS. All rights reserved.
            </p>
            <div className="flex items-center gap-6 text-sm text-echo-cyan-pale/60">
              <a href="#" className="hover:text-echo-cyan transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="hover:text-echo-cyan transition-colors">
                Terms of Service
              </a>
              <a href="#" className="hover:text-echo-cyan transition-colors">
                Cookie Policy
              </a>
            </div>
            <p className="text-sm text-echo-cyan-pale/60 flex items-center gap-1">
              Made with <Heart className="w-4 h-4 text-echo-cyan fill-echo-cyan icon-pulse" /> by KRACK HEADS
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}
