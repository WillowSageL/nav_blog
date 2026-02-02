-- Core schema (run in SQL Editor with role: service_role or default editor role)

-- Enable required extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Tables
CREATE TABLE IF NOT EXISTS public.categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  icon VARCHAR(50),
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (user_id, name)
);

CREATE TABLE IF NOT EXISTS public.bookmarks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  url TEXT NOT NULL,
  description TEXT,
  favicon_url TEXT,
  category_id UUID REFERENCES public.categories(id) ON DELETE SET NULL,
  sort_order INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.user_settings (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  theme VARCHAR(20) DEFAULT 'light',
  layout VARCHAR(20) DEFAULT 'grid',
  show_descriptions BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE,
  display_name TEXT,
  bio TEXT,
  avatar_url TEXT,
  website TEXT,
  location TEXT,
  theme VARCHAR(20) DEFAULT 'system',
  language VARCHAR(10) DEFAULT 'zh-CN',
  timezone TEXT DEFAULT 'Asia/Shanghai',
  notifications_enabled BOOLEAN DEFAULT true,
  layout_preference VARCHAR(20) DEFAULT 'grid',
  show_descriptions BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_categories_user_id ON public.categories(user_id);
CREATE INDEX IF NOT EXISTS idx_categories_sort_order ON public.categories(sort_order);
CREATE INDEX IF NOT EXISTS idx_bookmarks_user_id ON public.bookmarks(user_id);
CREATE INDEX IF NOT EXISTS idx_bookmarks_category_id ON public.bookmarks(category_id);
CREATE INDEX IF NOT EXISTS idx_bookmarks_is_active ON public.bookmarks(is_active);
CREATE INDEX IF NOT EXISTS idx_bookmarks_sort_order ON public.bookmarks(sort_order);
CREATE INDEX IF NOT EXISTS idx_profiles_username ON public.profiles(username);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tr_categories_updated_at ON public.categories;
CREATE TRIGGER tr_categories_updated_at
  BEFORE UPDATE ON public.categories
  FOR EACH ROW EXECUTE PROCEDURE public.set_updated_at();

DROP TRIGGER IF EXISTS tr_bookmarks_updated_at ON public.bookmarks;
CREATE TRIGGER tr_bookmarks_updated_at
  BEFORE UPDATE ON public.bookmarks
  FOR EACH ROW EXECUTE PROCEDURE public.set_updated_at();

DROP TRIGGER IF EXISTS tr_profiles_updated_at ON public.profiles;
CREATE TRIGGER tr_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE PROCEDURE public.set_updated_at();

DROP TRIGGER IF EXISTS tr_user_settings_updated_at ON public.user_settings;
CREATE TRIGGER tr_user_settings_updated_at
  BEFORE UPDATE ON public.user_settings
  FOR EACH ROW EXECUTE PROCEDURE public.set_updated_at();

-- Auto create profile and settings on new user
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (
    id,
    display_name,
    theme,
    language,
    timezone,
    notifications_enabled,
    layout_preference,
    show_descriptions,
    created_at,
    updated_at
  )
  VALUES (
    NEW.id,
    COALESCE(NEW.email, 'User'),
    'system',
    'zh-CN',
    'Asia/Shanghai',
    true,
    'grid',
    true,
    NOW(),
    NOW()
  )
  ON CONFLICT (id) DO NOTHING;

  INSERT INTO public.user_settings (
    user_id,
    theme,
    layout,
    show_descriptions,
    created_at,
    updated_at
  )
  VALUES (
    NEW.id,
    'light',
    'grid',
    true,
    NOW(),
    NOW()
  )
  ON CONFLICT (user_id) DO NOTHING;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER
SET search_path = public, auth;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookmarks ENABLE ROW LEVEL SECURITY;

-- Policies: profiles
DROP POLICY IF EXISTS "Profiles: read own" ON public.profiles;
CREATE POLICY "Profiles: read own" ON public.profiles
  FOR SELECT USING (auth.uid() = id);

DROP POLICY IF EXISTS "Profiles: insert own" ON public.profiles;
CREATE POLICY "Profiles: insert own" ON public.profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Profiles: update own" ON public.profiles;
CREATE POLICY "Profiles: update own" ON public.profiles
  FOR UPDATE USING (auth.uid() = id);

-- Policies: user_settings
DROP POLICY IF EXISTS "UserSettings: read own" ON public.user_settings;
CREATE POLICY "UserSettings: read own" ON public.user_settings
  FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "UserSettings: insert own" ON public.user_settings;
CREATE POLICY "UserSettings: insert own" ON public.user_settings
  FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "UserSettings: update own" ON public.user_settings;
CREATE POLICY "UserSettings: update own" ON public.user_settings
  FOR UPDATE USING (auth.uid() = user_id);

-- Policies: categories (private)
DROP POLICY IF EXISTS "Categories: read own" ON public.categories;
CREATE POLICY "Categories: read own" ON public.categories
  FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Categories: insert own" ON public.categories;
CREATE POLICY "Categories: insert own" ON public.categories
  FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Categories: update own" ON public.categories;
CREATE POLICY "Categories: update own" ON public.categories
  FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Categories: delete own" ON public.categories;
CREATE POLICY "Categories: delete own" ON public.categories
  FOR DELETE USING (auth.uid() = user_id);

-- Policies: bookmarks (private)
DROP POLICY IF EXISTS "Bookmarks: read own" ON public.bookmarks;
CREATE POLICY "Bookmarks: read own" ON public.bookmarks
  FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Bookmarks: insert own" ON public.bookmarks;
CREATE POLICY "Bookmarks: insert own" ON public.bookmarks
  FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Bookmarks: update own" ON public.bookmarks;
CREATE POLICY "Bookmarks: update own" ON public.bookmarks
  FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Bookmarks: delete own" ON public.bookmarks;
CREATE POLICY "Bookmarks: delete own" ON public.bookmarks
  FOR DELETE USING (auth.uid() = user_id);

-- Seed data (per-user)
DO $$
DECLARE
  dev_category_id UUID;
  design_category_id UUID;
  learn_category_id UUID;
  entertainment_category_id UUID;
  current_user_id UUID;
BEGIN
  current_user_id := auth.uid();
  IF current_user_id IS NULL THEN
    RETURN;
  END IF;

  INSERT INTO public.categories (user_id, name, icon, sort_order) VALUES
    (current_user_id, '开发工具', '🛠️', 1),
    (current_user_id, '设计资源', '🎨', 2),
    (current_user_id, '学习资料', '📚', 3),
    (current_user_id, '娱乐', '🎮', 4)
  ON CONFLICT (user_id, name) DO NOTHING;

  SELECT id INTO dev_category_id FROM public.categories
    WHERE user_id = current_user_id AND name = '开发工具' LIMIT 1;
  SELECT id INTO design_category_id FROM public.categories
    WHERE user_id = current_user_id AND name = '设计资源' LIMIT 1;
  SELECT id INTO learn_category_id FROM public.categories
    WHERE user_id = current_user_id AND name = '学习资料' LIMIT 1;
  SELECT id INTO entertainment_category_id FROM public.categories
    WHERE user_id = current_user_id AND name = '娱乐' LIMIT 1;

  INSERT INTO public.bookmarks (user_id, title, url, description, category_id, sort_order) VALUES
    (current_user_id, 'GitHub', 'https://github.com', '全球最大的代码托管平台', dev_category_id, 1),
    (current_user_id, 'VS Code', 'https://code.visualstudio.com', '微软开发的免费代码编辑器', dev_category_id, 2),
    (current_user_id, 'Stack Overflow', 'https://stackoverflow.com', '程序员问答社区', dev_category_id, 3),
    (current_user_id, 'Figma', 'https://figma.com', '协作式界面设计工具', design_category_id, 1),
    (current_user_id, 'Dribbble', 'https://dribbble.com', '设计师作品展示平台', design_category_id, 2),
    (current_user_id, 'MDN Web Docs', 'https://developer.mozilla.org', 'Web技术权威文档', learn_category_id, 1),
    (current_user_id, 'freeCodeCamp', 'https://freecodecamp.org', '免费编程学习平台', learn_category_id, 2),
    (current_user_id, 'YouTube', 'https://youtube.com', '视频分享平台', entertainment_category_id, 1),
    (current_user_id, 'Netflix', 'https://netflix.com', '在线视频流媒体服务', entertainment_category_id, 2)
  ON CONFLICT DO NOTHING;
END $$;
