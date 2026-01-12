'use client'

import { useRef, useState } from 'react'
import { Upload, Image as ImageIcon, Loader2 } from 'lucide-react'
import Image from 'next/image'
import { motion } from 'framer-motion'
import GlassCard from './GlassCard'

interface UploadBoxProps {
  onImageUpload: (imageUrl: string, file: File) => void
  uploadedImage: string | null
  onAnalyze: () => void
  isProcessing: boolean
  selectedImageType: 'chest_xray' | 'bone_xray' | 'skin_image'
  onImageTypeChange: (type: 'chest_xray' | 'bone_xray' | 'skin_image') => void
}

export default function UploadBox({
  onImageUpload,
  uploadedImage,
  onAnalyze,
  isProcessing,
  selectedImageType,
  onImageTypeChange
}: UploadBoxProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  const categories = [
    { id: 'chest_xray', label: 'Chest X-Ray', icon: '🫁' },
    { id: 'bone_xray', label: 'Bone X-Ray', icon: '🦴' },
    { id: 'skin_image', label: 'Skin Lesion', icon: '🔍' }
  ] as const

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
        {/* Category Selection */}
        <div className="space-y-3">
          <p className="text-sm font-medium text-echo-cyan-pale/70 px-1">Select Analysis Category</p>
          <div className="grid grid-cols-3 gap-3">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => onImageTypeChange(cat.id)}
                className={`
                  flex flex-col items-center gap-2 p-3 rounded-xl border transition-all duration-300
                  ${selectedImageType === cat.id
                    ? 'bg-echo-cyan/20 border-echo-cyan shadow-[0_0_15px_rgba(34,211,238,0.2)]'
                    : 'bg-echo-navy-light/50 border-echo-cyan/10 hover:border-echo-cyan/30'}
                `}
              >
                <span className="text-2xl">{cat.icon}</span>
                <span className={`text-xs font-semibold ${selectedImageType === cat.id ? 'text-echo-cyan' : 'text-echo-cyan-pale/60'}`}>
                  {cat.label}
                </span>
                {selectedImageType === cat.id && (
                  <motion.div
                    layoutId="active-cat"
                    className="absolute inset-0 border-2 border-echo-cyan rounded-xl pointer-events-none"
                    initial={false}
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  />
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Upload area */}
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer
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
            className="flex flex-col items-center space-y-4"
          >
            <motion.div
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              className="relative"
            >
              <div className="absolute inset-0 bg-echo-cyan/30 rounded-full blur-xl"></div>
              <div className="relative p-3 rounded-full bg-gradient-to-br from-echo-cyan/20 to-echo-cyan-light/20">
                <Upload className="w-10 h-10 text-echo-cyan icon-bounce" />
              </div>
            </motion.div>
            <div className="space-y-1">
              <p className="text-lg font-display font-semibold text-white">
                Upload {categories.find(c => c.id === selectedImageType)?.label}
              </p>
              <p className="text-xs text-echo-cyan-pale/70">
                Drop image here or click to browse
              </p>
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
              <Image
                src={uploadedImage}
                alt="Uploaded medical image"
                width={800}
                height={400}
                className="w-full h-auto max-h-80 object-contain"
                unoptimized
              />
              <div className="absolute top-3 left-3 px-3 py-1 rounded-full bg-echo-navy/80 border border-echo-cyan/30 text-[10px] font-bold text-echo-cyan uppercase tracking-wider backdrop-blur-sm">
                Category: {categories.find(c => c.id === selectedImageType)?.label}
              </div>
            </div>

            <div className="flex gap-3">
              <motion.button
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                onClick={onAnalyze}
                disabled={isProcessing}
                className={`
                  flex-1 py-3 px-6 rounded-xl font-display font-semibold text-white
                  echo-button-primary ripple focus-ring
                  disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
                  flex items-center justify-center gap-2
                `}
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <ImageIcon className="w-4 h-4" />
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
                className="py-3 px-5 rounded-xl text-sm font-display font-semibold text-white bg-echo-navy-light hover:bg-echo-navy transition-all duration-300 ripple focus-ring border border-echo-cyan/30"
              >
                Replace
              </motion.button>
            </div>
          </motion.div>
        )}
      </div>
    </GlassCard>
  )
}
