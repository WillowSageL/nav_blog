'use client'

import { Moon, Sun, Zap, Monitor } from 'lucide-react'
import { useTheme } from 'next-themes'
import { useEffect, useState } from 'react'

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <button className="p-2 rounded-lg border border-input">
        <Sun className="w-4 h-4" />
      </button>
    )
  }

  const cycleTheme = () => {
    if (theme === 'system') setTheme('light')
    else if (theme === 'light') setTheme('dark')
    else if (theme === 'dark') setTheme('cyberpunk')
    else setTheme('system')
  }

  const getIcon = () => {
    switch (theme) {
      case 'system': return <Monitor className="w-4 h-4" />
      case 'light': return <Sun className="w-4 h-4" />
      case 'dark': return <Moon className="w-4 h-4" />
      case 'cyberpunk': return <Zap className="w-4 h-4" />
      default: return <Monitor className="w-4 h-4" />
    }
  }

  return (
    <button
      onClick={cycleTheme}
      className="p-2 rounded-lg border border-input hover:bg-accent transition-colors"
    >
      {getIcon()}
    </button>
  )
}