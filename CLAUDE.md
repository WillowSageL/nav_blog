# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A modern personal navigation/bookmark manager built with Next.js 15 and Supabase. Features include user authentication, bookmark management with categories, theme switching, and responsive design.

**Tech Stack:**
- Frontend: Next.js 15 (App Router), TypeScript, Tailwind CSS
- UI Components: Shadcn/ui (Radix UI primitives)
- Backend: Supabase (PostgreSQL + Auth + Storage)
- Deployment: Vercel

## Common Commands

```bash
# Development
npm run dev              # Start dev server with Turbopack (http://localhost:3000)

# Build & Production
npm run build            # Build for production
npm start                # Start production server

# Code Quality
npm run lint             # Run ESLint
```

## Database Setup

**Initial Setup:**
1. Create a Supabase project at https://supabase.com
2. Copy `.env.example` to `.env.local` and fill in Supabase credentials:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
3. Run SQL scripts in Supabase SQL Editor (in order):
   - `database.sql` - Creates tables, triggers, RLS policies, seed data
   - `storage.sql` - Sets up avatar storage bucket and policies

**Database Schema:**
- `profiles` - User profile data (username, display_name, bio, avatar_url, preferences)
- `categories` - Bookmark categories (name, icon, sort_order)
- `bookmarks` - Bookmark entries (title, url, description, favicon_url, category_id)
- `user_settings` - User preferences (theme, layout, show_descriptions)

**Key Features:**
- Row Level Security (RLS) enabled on all tables - users can only access their own data
- Auto-creation of profile and settings on user signup via trigger
- Cascading deletes when user is deleted
- Auto-updated `updated_at` timestamps via triggers

## Architecture

### Directory Structure

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Home page (bookmark display)
│   └── admin/
│       └── page.tsx       # Admin page (bookmark/category management)
├── components/            # React components (mostly client components)
│   ├── ui/               # Shadcn/ui components (Button, Input, Card, etc.)
│   ├── EnhancedAuthProvider.tsx    # Auth context with password encryption
│   ├── EnhancedAuthDialog.tsx      # Login/signup modal
│   ├── BookmarkManager.tsx         # Bookmark CRUD
│   ├── CategoryManager.tsx         # Category CRUD
│   ├── UserProfileEditor.tsx       # Profile editing
│   └── ...
└── lib/                   # Utilities and types
    ├── supabase.ts       # Supabase client initialization
    ├── types.ts          # TypeScript interfaces (Bookmark, Category, etc.)
    ├── crypto.ts         # Password encryption utilities
    ├── profile.ts        # Profile service functions
    └── database.types.ts # Auto-generated Supabase types
```

### Key Patterns

**1. Client vs Server Components:**
- Most components use `'use client'` directive (12+ client components)
- Root layout is server component, wraps app with providers
- Client components needed for: auth state, interactive UI, Supabase realtime

**2. Authentication Flow:**
- `EnhancedAuthProvider` wraps entire app in `layout.tsx`
- Provides auth context: `user`, `session`, `loading`, `signIn`, `signUp`, `signOut`
- Uses Supabase Auth with localStorage persistence
- Password encryption available but disabled by default (Supabase compatibility)
- Access via `useAuth()` hook in any component

**3. Data Fetching:**
- Direct Supabase client calls in components (no API routes)
- Parallel fetching with `Promise.all()` for initial page load
- Example from `page.tsx:30-34`:
  ```typescript
  const [profileData, categoriesData, bookmarksData] = await Promise.all([
    profileService.getProfile(user),
    supabase.from('categories').select('*').order('sort_order'),
    supabase.from('bookmarks').select('*, category:categories(*)').eq('is_active', true)
  ])
  ```

**4. State Management:**
- React Context for auth state (EnhancedAuthProvider)
- Local component state with useState
- No external state management library (Redux, Zustand, etc.)

**5. Styling:**
- Tailwind CSS utility classes
- CSS variables in `globals.css` for theming
- Shadcn/ui components with `cn()` utility for class merging
- Responsive design with Tailwind breakpoints

**6. Type Safety:**
- TypeScript strict mode enabled
- Path alias `@/*` maps to `./src/*`
- Supabase types in `lib/database.types.ts`
- Custom interfaces in `lib/types.ts`

## Important Implementation Details

### Password Security System

The codebase includes a comprehensive password encryption system (`lib/crypto.ts`) with multiple encryption schemes:
- Simple SHA256 hashing
- PBKDF2 with salt
- AES symmetric encryption
- Password strength validation

**IMPORTANT:** Client-side encryption is **disabled by default** to maintain Supabase Auth compatibility. The `useEncryption` parameter in `signIn`/`signUp` defaults to `false`. Only enable if implementing custom auth backend.

### Image Handling

`next.config.js` allows remote images from any domain for favicon fetching:
```javascript
remotePatterns: [
  { protocol: 'https', hostname: '**' },
  { protocol: 'http', hostname: '**' }
]
```

### Admin Page Protection

`/admin` page uses client-side redirect if user not authenticated:
```typescript
useEffect(() => {
  if (!loading && !user && !hasRedirected.current) {
    hasRedirected.current = true
    redirect('/')
  }
}, [loading, user])
```

### Profile Auto-Creation

Database trigger automatically creates profile and user_settings when new user signs up (see `database.sql:98-153`). No manual profile creation needed in application code.

### Storage Bucket

Avatar uploads use Supabase Storage bucket `avatars`:
- Public read access
- Users can only upload/update/delete their own avatars
- File path pattern: `{user_id}/avatar.{ext}`
- See `profileService.uploadAvatar()` in `lib/profile.ts`

## Development Workflow

1. **Adding New Features:**
   - Create components in `src/components/`
   - Use `'use client'` if component needs interactivity or hooks
   - Import types from `@/lib/types`
   - Use Supabase client from `@/lib/supabase`

2. **Database Changes:**
   - Modify `database.sql` with new schema
   - Run updated SQL in Supabase SQL Editor
   - Regenerate types: `npx supabase gen types typescript --project-id <project-id> > src/lib/database.types.ts`

3. **Adding UI Components:**
   - Use existing Shadcn/ui components from `components/ui/`
   - Add new Shadcn components: `npx shadcn-ui@latest add <component-name>`
   - Follow existing patterns for styling and composition

4. **Authentication:**
   - Always check `loading` state before checking `user`
   - Use `useAuth()` hook to access auth state
   - Protected pages should redirect if `!user`

## Common Pitfalls

1. **Race Conditions:** Check `authLoading` before accessing `user` to avoid race conditions
2. **RLS Policies:** All database operations are subject to RLS - ensure user is authenticated
3. **Client Components:** Don't forget `'use client'` directive when using hooks or browser APIs
4. **Password Encryption:** Don't enable client-side encryption without understanding Supabase Auth implications
5. **Image Domains:** Add new domains to `next.config.js` if restricting remote image patterns

## Environment Variables

Required in `.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

Optional (for password encryption, if enabled):
```env
NEXT_PUBLIC_ENCRYPTION_KEY=your_encryption_key
NEXT_PUBLIC_ENCRYPTION_MODE=none|hash|encrypt
```
