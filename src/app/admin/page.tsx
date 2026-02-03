'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/components/EnhancedAuthProvider'
import { CategoryManager } from '@/components/CategoryManager'
import { BookmarkManager } from '@/components/BookmarkManager'
import { Button } from '@/components/ui/button'
import { Category } from '@/lib/types'
import { ArrowLeft } from 'lucide-react'

export default function AdminPage() {
  const router = useRouter()
  const { user, loading } = useAuth()
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(null)
  const [categories, setCategories] = useState<Category[]>([])
  const hasRedirected = useRef(false)

  useEffect(() => {
    if (!loading && !user && !hasRedirected.current) {
      hasRedirected.current = true
      router.replace('/')
    }
  }, [loading, user, router])

  // 在loading时显示加载状态
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">加载中...</div>
      </div>
    )
  }

  // 在没有用户时不渲染任何内容
  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-primary/5 blur-[100px] rounded-full"></div>
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-secondary/5 blur-[100px] rounded-full"></div>
      </div>
      <header className="relative z-10 border-b border-primary/20 bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-neon-cyan">管理后台</h1>
              <p className="text-muted-foreground mt-1">
                管理你的导航书签和分类 - {user.email}
              </p>
            </div>
            <Button
              variant="outline"
              className="border-primary/30 hover:bg-primary/10 hover:text-neon-purple transition-all duration-300"
              onClick={() => router.push('/')}
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              返回首页
            </Button>
          </div>
        </div>
      </header>

      <main className="relative z-10 container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* 分类管理 */}
          <div>
            <CategoryManager 
              selectedCategoryId={selectedCategoryId}
              onCategorySelect={setSelectedCategoryId}
              onCategoriesChange={setCategories}
            />
          </div>

          {/* 书签管理 */}
          <div>
            <BookmarkManager 
              selectedCategoryId={selectedCategoryId}
              categories={categories}
            />
          </div>
        </div>
      </main>
    </div>
  )
}