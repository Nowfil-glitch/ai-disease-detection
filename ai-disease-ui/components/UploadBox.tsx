'use client'

import { useRef, useState } from 'react'
import { Upload, Image as ImageIcon, Loader2 } from 'lucide-react'
import { motion } from 'framer-motion'
import GlassCard from './GlassCard'

interface UploadBoxProps {
  onImageUpload: (imageUrl: string, file: File) => void
  uploadedImage: string | null
  onAnalyze: () => void
  isProcessing: boolean
}

export default function UploadBox({ onImageUpload, uploadedImage, onAnalyze, isProcessing }: UploadBoxProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onloadend = () => {
        onImageUpload(reader.result as string, file)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onloadend = () => {
        onImageUpload(reader.result as string, file)
      }
      reader.readAsDataURL(file)
    }
  }

  return (
    <GlassCard>
      <div className="space-y-6">
        {/* Upload area */}
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer
            transition-all duration-500 hover:border-echo-cyan
            bg-gradient-to-r from-echo-navy via-echo-navy-light to-echo-cyan/30
            ${isDragging ? 'border-echo-cyan scale-[1.02] shadow-lg shadow-echo-cyan/20' : 'border-echo-cyan/30'}
            ${uploadedImage ? 'hidden' : 'block'}
          `}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
          />
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="flex flex-col items-center space-y-6"
          >
            <motion.div
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              className="relative"
            >
              <div className="absolute inset-0 bg-echo-cyan/30 rounded-full blur-xl"></div>
              <div className="relative p-4 rounded-full bg-gradient-to-br from-echo-cyan/20 to-echo-cyan-light/20">
                <Upload className="w-12 h-12 text-echo-cyan icon-bounce" />
              </div>
            </motion.div>
            <div className="space-y-2">
              <p className="text-xl font-display font-semibold text-white">
                Drop your medical image here
              </p>
              <p className="text-sm text-echo-cyan-pale/70">
                or click to browse (X-ray, CT scan, skin images)
              </p>
              <div className="flex items-center justify-center gap-2 pt-2">
                <span className="px-3 py-1 text-xs rounded-full bg-echo-navy-light text-echo-cyan-pale">JPG</span>
                <span className="px-3 py-1 text-xs rounded-full bg-echo-navy-light text-echo-cyan-pale">PNG</span>
                <span className="px-3 py-1 text-xs rounded-full bg-echo-navy-light text-echo-cyan-pale">DICOM</span>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Image preview */}
        {uploadedImage && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-4"
          >
            <div className="relative rounded-xl overflow-hidden bg-echo-navy-light/50 border border-echo-cyan/20">
              <img
                src={uploadedImage}
                alt="Uploaded medical image"
                className="w-full h-auto max-h-96 object-contain"
              />
            </div>

            <div className="flex gap-4">
              <motion.button
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                onClick={onAnalyze}
                disabled={isProcessing}
                className={`
                  flex-1 py-4 px-8 rounded-xl font-display font-semibold text-white
                  echo-button-primary ripple focus-ring
                  disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
                  flex items-center justify-center gap-3
                `}
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <ImageIcon className="w-5 h-5" />
                    <span>Analyze Image</span>
                  </>
                )}
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  onImageUpload('', null as any)
                  if (fileInputRef.current) fileInputRef.current.value = ''
                }}
                className="py-4 px-6 rounded-xl font-display font-semibold text-white bg-echo-navy-light hover:bg-echo-navy transition-all duration-300 ripple focus-ring border border-echo-cyan/30"
              >
                Upload New
              </motion.button>
            </div>
          </motion.div>
        )}
      </div>
    </GlassCard>
  )
}
