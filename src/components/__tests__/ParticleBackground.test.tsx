import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, cleanup } from '@testing-library/react'
import { ParticleBackground } from '../ParticleBackground'

const mockCtx = {
  clearRect: vi.fn(),
  scale: vi.fn(),
  fillRect: vi.fn(),
  beginPath: vi.fn(),
  arc: vi.fn(),
  fill: vi.fn(),
  stroke: vi.fn()
}

describe('ParticleBackground', () => {
  let rafCallback: FrameRequestCallback | null = null
  let rafId = 1

  beforeEach(() => {
    rafCallback = null
    rafId = 1

    vi.spyOn(window, 'requestAnimationFrame').mockImplementation((cb) => {
      rafCallback = cb
      return rafId++
    })

    vi.spyOn(window, 'cancelAnimationFrame').mockImplementation(() => {})

    HTMLCanvasElement.prototype.getContext = vi.fn().mockReturnValue(mockCtx)

    Object.defineProperty(window, 'innerWidth', { value: 1920, writable: true, configurable: true })
    Object.defineProperty(window, 'innerHeight', { value: 1080, writable: true, configurable: true })
    Object.defineProperty(window, 'devicePixelRatio', { value: 2, writable: true, configurable: true })
  })

  afterEach(() => {
    cleanup()
    vi.restoreAllMocks()
  })

  it('renders canvas element', () => {
    const onFrame = vi.fn()
    const { getByTestId } = render(<ParticleBackground onFrame={onFrame} />)

    expect(getByTestId('particle-background')).toBeInTheDocument()
    expect(getByTestId('particle-background').tagName).toBe('CANVAS')
  })

  it('applies fullscreen fixed positioning', () => {
    const onFrame = vi.fn()
    const { getByTestId } = render(<ParticleBackground onFrame={onFrame} />)
    const canvas = getByTestId('particle-background')

    expect(canvas).toHaveStyle({
      position: 'fixed',
      width: '100vw',
      height: '100vh',
      pointerEvents: 'none'
    })
  })

  it('starts RAF loop when enabled (default)', () => {
    const onFrame = vi.fn()
    render(<ParticleBackground onFrame={onFrame} />)

    expect(window.requestAnimationFrame).toHaveBeenCalled()
  })

  it('calls onFrame with correct meta', () => {
    const onFrame = vi.fn()
    render(<ParticleBackground onFrame={onFrame} />)

    if (rafCallback) {
      rafCallback(1000)
    }

    expect(onFrame).toHaveBeenCalledWith(
      mockCtx,
      expect.objectContaining({
        width: 1920,
        height: 1080,
        dpr: 2,
        time: 1000
      })
    )
  })

  it('does not start RAF when enabled=false', () => {
    const onFrame = vi.fn()
    render(<ParticleBackground onFrame={onFrame} enabled={false} />)

    if (rafCallback) {
      rafCallback(1000)
    }

    expect(onFrame).not.toHaveBeenCalled()
  })

  it('cancels RAF on unmount', () => {
    const onFrame = vi.fn()
    const { unmount } = render(<ParticleBackground onFrame={onFrame} />)

    unmount()

    expect(window.cancelAnimationFrame).toHaveBeenCalled()
  })

  it('calls onResize on mount', () => {
    const onFrame = vi.fn()
    const onResize = vi.fn()
    render(<ParticleBackground onFrame={onFrame} onResize={onResize} />)

    expect(onResize).toHaveBeenCalledWith(
      expect.objectContaining({
        width: 1920,
        height: 1080,
        dpr: 2
      })
    )
  })

  it('handles resize events', () => {
    const onFrame = vi.fn()
    const onResize = vi.fn()
    render(<ParticleBackground onFrame={onFrame} onResize={onResize} />)

    onResize.mockClear()

    Object.defineProperty(window, 'innerWidth', { value: 1280, writable: true, configurable: true })
    Object.defineProperty(window, 'innerHeight', { value: 720, writable: true, configurable: true })

    window.dispatchEvent(new Event('resize'))

    expect(onResize).toHaveBeenCalledWith(
      expect.objectContaining({
        width: 1280,
        height: 720
      })
    )
  })

  it('removes resize listener on unmount', () => {
    const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener')
    const onFrame = vi.fn()
    const { unmount } = render(<ParticleBackground onFrame={onFrame} />)

    unmount()

    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function))
  })

  it('applies custom className', () => {
    const onFrame = vi.fn()
    const { getByTestId } = render(
      <ParticleBackground onFrame={onFrame} className="custom-class" />
    )

    expect(getByTestId('particle-background')).toHaveClass('custom-class')
  })

  it('applies custom style', () => {
    const onFrame = vi.fn()
    const { getByTestId } = render(
      <ParticleBackground onFrame={onFrame} style={{ zIndex: 100 }} />
    )

    expect(getByTestId('particle-background')).toHaveStyle({ zIndex: 100 })
  })

  it('calculates delta time between frames', () => {
    const onFrame = vi.fn()
    render(<ParticleBackground onFrame={onFrame} />)

    if (rafCallback) {
      rafCallback(1000)
      rafCallback(1016)
    }

    const secondCall = onFrame.mock.calls[1]
    if (secondCall) {
      expect(secondCall[1].delta).toBe(16)
    }
  })
})
