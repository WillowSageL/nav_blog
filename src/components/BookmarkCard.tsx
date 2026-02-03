'use client'

import { useState } from 'react'
import { Bookmark } from '@/lib/types'
import { ExternalLink } from 'lucide-react'

interface BookmarkCardProps {
  bookmark: Bookmark
}

export function BookmarkCard({ bookmark }: BookmarkCardProps) {
  const [imageError, setImageError] = useState(false)

  return (
    <a
      href={bookmark.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group block p-4 bg-card/50 border border-primary/20 rounded-2xl hover:bg-card/80 transition-colors duration-200 hover:shadow-lg glow-interactive"
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <div className="w-10 h-10 bg-card rounded-xl flex items-center justify-center border border-primary/30">
            {bookmark.favicon_url && !imageError ? (
              <img
                src={bookmark.favicon_url}
                alt=""
                width={20}
                height={20}
                className="w-5 h-5 rounded"
                onError={() => setImageError(true)}
              />
            ) : (
              <ExternalLink className="w-4 h-4 text-muted-foreground group-hover:icon-neon-cyan transition-all" />
            )}
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-foreground group-hover:text-neon-pink transition-colors text-sm leading-tight">
            {bookmark.title}
          </h3>
          {bookmark.description && (
            <p className="text-xs text-muted-foreground mt-1 line-clamp-2 leading-relaxed">
              {bookmark.description}
            </p>
          )}
          <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
            <p className="text-xs text-muted-foreground">
              {new URL(bookmark.url).hostname}
            </p>
          </div>
        </div>
      </div>
    </a>
  )
}