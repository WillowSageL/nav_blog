'use client'

import type React from 'react'
import { useRef, useEffect, useCallback } from 'react'

export interface FrameMeta {
  width: number
  height: number
  dpr: number
  time: number
  delta: number
}

export interface ResizeMeta {
  width: number
  height: number
  dpr: number
}

export interface ParticleBackgroundProps {
  enabled?: boolean
  onFrame: (ctx: CanvasRenderingContext2D, meta: FrameMeta) => void
  onResize?: (meta: ResizeMeta) => void
  className?: string
  style?: React.CSSProperties
}

export function ParticleBackground(props: ParticleBackgroundProps) {
  const { enabled = true, onFrame, onResize, className, style } = props
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const rafIdRef = useRef<number>(0)
  const lastTimeRef = useRef<number>(0)

  const updateCanvasSize = useCallback(() => {
    const canvas = canvasRef.current
    if (!canvas) return null

    const dpr = window.devicePixelRatio || 1
    const width = window.innerWidth
    const height = window.innerHeight

    canvas.width = width * dpr
    canvas.height = height * dpr

    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.scale(dpr, dpr)
    }

    return { width, height, dpr }
  }, [])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const initialSize = updateCanvasSize()
    if (initialSize && onResize) {
      onResize(initialSize)
    }

    const handleResize = () => {
      const size = updateCanvasSize()
      if (size && onResize) {
        onResize(size)
      }
    }

    window.addEventListener('resize', handleResize)

    const render = (time: number) => {
      if (!enabled) return

      const delta = lastTimeRef.current ? time - lastTimeRef.current : 0
      lastTimeRef.current = time

      const dpr = window.devicePixelRatio || 1
      const width = window.innerWidth
      const height = window.innerHeight

      ctx.clearRect(0, 0, width, height)

      onFrame(ctx, { width, height, dpr, time, delta })

      rafIdRef.current = requestAnimationFrame(render)
    }

    if (enabled) {
      rafIdRef.current = requestAnimationFrame(render)
    }

    return () => {
      if (rafIdRef.current) {
        cancelAnimationFrame(rafIdRef.current)
      }
      window.removeEventListener('resize', handleResize)
    }
  }, [enabled, onFrame, onResize, updateCanvasSize])

  return (
    <canvas
      ref={canvasRef}
      className={className}
      data-testid="particle-background"
      style={{
        position: 'fixed',
        inset: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        ...style
      }}
    />
  )
}
