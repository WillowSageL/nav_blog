'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/components/EnhancedAuthProvider'
import { Bookmark, Category } from '@/lib/types'
import { UserProfile, profileService } from '@/lib/profile'
import { CategorySection } from '@/components/CategorySection'
import { SearchBar } from '@/components/SearchBar'
import { ThemeToggle } from '@/components/ThemeToggle'
import { EnhancedAuthDialog } from '@/components/EnhancedAuthDialog'
import { UserInfo } from '@/components/UserInfo'
import { UserProfileEditor } from '@/components/UserProfileEditor'
import { Button } from '@/components/ui/button'
import { Plus, LogIn, LogOut, Settings } from 'lucide-react'

export default function Home() {
  const router = useRouter()
  const { user, loading: authLoading, signOut } = useAuth()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [showAuthDialog, setShowAuthDialog] = useState(false)
  const [showProfileEditor, setShowProfileEditor] = useState(false)

  useEffect(() => {
    if (!authLoading && user) {
      const fetchAllData = async () => {
        try {
          const [profileData, categoriesData, bookmarksData] = await Promise.all([
            profileService.getProfile(user),
            supabase.from('categories').select('*').order('sort_order'),
            supabase.from('bookmarks').select('*, category:categories(*)').eq('is_active', true).order('sort_order')
          ])
          setProfile(profileData)
          setCategories(categoriesData.data || [])
          setBookmarks(bookmarksData.data || [])
        } catch (error) {
          console.error('Error fetching page data:', error)
        }
      }
      fetchAllData()
    } else if (!authLoading && !user) {
      // Clear all data when user logs out
      setProfile(null)
      setCategories([])
      setBookmarks([])
    }
  }, [user, authLoading])

  const handleSignOut = async () => {
    await signOut()
  }

  const filteredBookmarks = bookmarks.filter(bookmark =>
    bookmark.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    bookmark.description?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="bg-card/50 rounded-2xl p-8 shadow-neon-purple border border-primary/30">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 border-4 border-muted border-t-accent rounded-full animate-spin"></div>
            <div className="text-accent text-lg font-medium">加载中...</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-primary/10 blur-[100px] rounded-full"></div>
        <div className="absolute top-20 right-20 w-72 h-72 bg-accent/5 blur-[80px] rounded-full"></div>
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-secondary/10 blur-[100px] rounded-full"></div>
      </div>

      <header className="relative z-10 bg-card/50 backdrop-blur-md border-b border-primary/20">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-card rounded-2xl flex items-center justify-center border border-primary/30 shadow-neon-purple/50">
                <span className="text-2xl icon-neon-pink">🚀</span>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-neon-purple">我的导航</h1>
                <p className="text-muted-foreground text-sm">发现赛博世界</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="bg-card/50 rounded-xl p-1 border border-primary/20">
                <ThemeToggle />
              </div>
              {user ? (
                <div className="flex items-center gap-3">
                  <div className="bg-card/50 rounded-xl p-2 border border-primary/20">
                    <UserInfo onEdit={() => setShowProfileEditor(true)} profile={profile} />
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="bg-card/50 text-foreground hover:bg-card border border-primary/20 rounded-xl transition-colors duration-200"
                    onClick={() => router.push('/admin')}
                  >
                    <Settings className="w-4 h-4 mr-2" />
                    管理
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="bg-card/50 text-foreground hover:bg-card border border-primary/20 rounded-xl transition-colors duration-200"
                    onClick={handleSignOut}
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    退出
                  </Button>
                </div>
              ) : (
                <Button
                  onClick={() => setShowAuthDialog(true)}
                  size="sm"
                  className="bg-primary/20 text-foreground hover:bg-primary/30 border border-primary/30 rounded-xl transition-colors duration-200 shadow-lg"
                >
                  <LogIn className="w-4 h-4 mr-2" />
                  登录
                </Button>
              )}
            </div>
          </div>
          <div className="bg-card/50 rounded-2xl p-1 border border-primary/20">
            <SearchBar value={searchTerm} onChange={setSearchTerm} />
          </div>
        </div>
      </header>

      <main className="relative z-10 container mx-auto px-4 py-8">
        {categories.length === 0 && !authLoading ? (
          <div className="text-center py-20">
            <div className="bg-card/50 rounded-3xl p-12 shadow-xl border border-primary/20 max-w-md mx-auto">
              <div className="w-20 h-20 bg-card rounded-full flex items-center justify-center mx-auto mb-6 border border-primary/30">
                <span className="text-4xl">📚</span>
              </div>
              <p className="text-foreground text-lg mb-6 font-medium">还没有任何分类</p>
              <p className="text-muted-foreground mb-8">开始添加你的第一个书签吧！</p>
              {user && (
                <Button
                  onClick={() => router.push('/admin')}
                  className="bg-gradient-to-r from-secondary to-primary hover:from-secondary/80 hover:to-primary/80 text-primary-foreground border-0 rounded-xl transition-colors duration-200 shadow-lg px-8 py-3"
                >
                  <Plus className="w-5 h-5 mr-2" />
                  添加书签
                </Button>
              )}
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            {categories.map((category) => {
              const categoryBookmarks = filteredBookmarks.filter(
                bookmark => bookmark.category_id === category.id
              )
              
              if (categoryBookmarks.length === 0 && searchTerm) return null

              return (
                <CategorySection
                  key={category.id}
                  category={category}
                  bookmarks={categoryBookmarks}
                />
              )
            })}
          </div>
        )}
      </main>

      {showAuthDialog && (
        <EnhancedAuthDialog onClose={() => setShowAuthDialog(false)} />
      )}

      {showProfileEditor && (
        <UserProfileEditor 
          onClose={() => setShowProfileEditor(false)} 
          onProfileUpdate={setProfile}
        />
      )}
    </div>
  )
}