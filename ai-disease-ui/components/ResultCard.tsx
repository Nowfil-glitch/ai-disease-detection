'use client'

import { motion } from 'framer-motion'
import { AlertCircle, CheckCircle, Info, Globe } from 'lucide-react'
import GlassCard from './GlassCard'
import ProbabilityRing from './ProbabilityRing'
import HeatmapViewer from './HeatmapViewer'

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

interface ResultCardProps {
  result: AnalysisResult
  imageUrl: string
  selectedLanguage: 'en' | 'hi' | 'es' | 'fr' | 'te'
  onLanguageChange: (lang: 'en' | 'hi' | 'es' | 'fr' | 'te') => void
}

export default function ResultCard({ result, imageUrl, selectedLanguage, onLanguageChange }: ResultCardProps) {
  const getRiskDisplay = () => {
    const riskLevel = result.risk_level.toLowerCase()
    if (riskLevel === 'high') {
      return {
        icon: <AlertCircle className="w-6 h-6 text-red-500" />,
        title: 'High Risk Detected',
        color: 'border-red-500 bg-red-50 dark:bg-red-900/20',
        textColor: 'text-red-700 dark:text-red-300'
      }
    }
    if (riskLevel === 'moderate') {
      return {
        icon: <Info className="w-6 h-6 text-orange-500" />,
        title: 'Moderate Risk',
        color: 'border-orange-500 bg-orange-50 dark:bg-orange-900/20',
        textColor: 'text-orange-700 dark:text-orange-300'
      }
    }
    return {
      icon: <CheckCircle className="w-6 h-6 text-green-500" />,
      title: 'Low Risk',
      color: 'border-green-500 bg-green-50 dark:bg-green-900/20',
      textColor: 'text-green-700 dark:text-green-300'
    }
  }

  const riskDisplay = getRiskDisplay()

  const languages = [
    { code: 'en' as const, name: 'English', flag: '🇬🇧' },
    { code: 'hi' as const, name: 'हिंदी', flag: '🇮🇳' },
    { code: 'te' as const, name: 'తెలుగు', flag: '🇮🇳' },
    { code: 'es' as const, name: 'Español', flag: '🇪🇸' },
    { code: 'fr' as const, name: 'Français', flag: '🇫🇷' }
  ]

  const availableLanguages = languages.filter(lang =>
    result.translations[lang.code]
  )

  return (
    <GlassCard>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="space-y-8"
      >
        {/* Header with Language Selector */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="text-center md:text-left">
            <motion.h2
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-3xl font-display font-bold text-echo-charcoal dark:text-white mb-2"
            >
              Analysis Results
            </motion.h2>
            <p className="text-echo-gray-mid dark:text-echo-gray-mid flex items-center gap-2 justify-center md:justify-start">
              <span className="inline-block w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              AI-powered detection complete
            </p>
          </div>

          {/* Language Selector */}
          {availableLanguages.length > 1 && (
            <div className="flex items-center gap-2 justify-center md:justify-end flex-wrap">
              <Globe className="w-5 h-5 text-echo-gray-mid" />
              {availableLanguages.map(lang => (
                <motion.button
                  key={lang.code}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => onLanguageChange(lang.code)}
                  className={`
                    px-4 py-2 rounded-lg font-display font-semibold transition-all duration-300 text-sm ripple focus-ring
                    ${selectedLanguage === lang.code
                      ? 'echo-button-secondary shadow-lg'
                      : 'bg-echo-gray-light dark:bg-echo-gray-darker text-echo-gray-dark dark:text-echo-gray-mid hover:bg-echo-gray-mid/20 dark:hover:bg-echo-gray-dark'
                    }
                  `}
                >
                  {lang.flag} {lang.name}
                </motion.button>
              ))}
            </div>
          )}
        </div>

        {/* Diagnosis Badge */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          className="text-center"
        >
          <div className="inline-flex items-center gap-3 px-8 py-4 echo-button-primary rounded-full font-display font-bold text-lg shadow-xl ripple">
            <svg className="w-6 h-6 icon-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Detected: {result.diagnosis}</span>
          </div>
        </motion.div>

        {/* Main content grid */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Left: Probability Ring */}
          <div className="flex items-center justify-center">
            <ProbabilityRing confidence={Math.round(result.confidence * 100)} />
          </div>

          {/* Right: Heatmap Viewer */}
          <div>
            <HeatmapViewer imageUrl={result.heatmap_url} />
          </div>
        </div>

        {/* Description Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-echo-charcoal rounded-xl p-6 border border-echo-gray-mid/20 dark:border-echo-gray-dark"
        >
          <h3 className="text-xl font-display font-bold text-echo-charcoal dark:text-white mb-3 flex items-center gap-3">
            <div className="p-2 rounded-lg bg-echo-blue-pale/20 dark:bg-echo-blue-dark/30">
              <Info className="w-5 h-5 text-echo-blue-dark dark:text-echo-blue-pale icon-pulse" />
            </div>
            Analysis Details
          </h3>
          <p className="text-echo-gray-dark dark:text-echo-gray-mid leading-relaxed">
            {result.description}
          </p>
        </motion.div>

        {/* Risk Level & Recommendation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className={`border-2 rounded-xl p-6 ${riskDisplay.color}`}
        >
          <div className="flex gap-4">
            <div className="flex-shrink-0">
              {riskDisplay.icon}
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-3">
                {riskDisplay.title}
              </h3>
              <div className="space-y-3">
                <div>
                  <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-1">
                    Recommended Action:
                  </h4>
                  <p className="text-gray-700 dark:text-gray-300">
                    {result.recommended_action}
                  </p>
                </div>
                {result.translations[selectedLanguage] && selectedLanguage !== 'en' && (
                  <div className="pt-3 border-t border-gray-300 dark:border-gray-600">
                    <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-1">
                      Translation:
                    </h4>
                    <p className="text-gray-700 dark:text-gray-300">
                      {result.translations[selectedLanguage]}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-center text-sm text-echo-gray-mid dark:text-echo-gray-mid border-t border-echo-gray-mid/20 dark:border-echo-gray-dark pt-6"
        >
          <p className="font-display font-semibold mb-2 flex items-center justify-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-echo-crimson animate-pulse"></span>
            Important Disclaimer
          </p>
          <p className="max-w-2xl mx-auto">{result.disclaimer}</p>
        </motion.div>
      </motion.div>
    </GlassCard>
  )
}
