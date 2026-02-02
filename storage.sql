-- Storage setup (run with role: postgres)

-- Create bucket if not exists
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true)
ON CONFLICT (id) DO NOTHING;

-- Storage policies
DROP POLICY IF EXISTS "Avatars: upload own" ON storage.objects;
CREATE POLICY "Avatars: upload own" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'avatars'
    AND name LIKE auth.uid()::text || '/%'
  );

DROP POLICY IF EXISTS "Avatars: update own" ON storage.objects;
CREATE POLICY "Avatars: update own" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'avatars'
    AND name LIKE auth.uid()::text || '/%'
  );

DROP POLICY IF EXISTS "Avatars: delete own" ON storage.objects;
CREATE POLICY "Avatars: delete own" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'avatars'
    AND name LIKE auth.uid()::text || '/%'
  );

DROP POLICY IF EXISTS "Avatars: public read" ON storage.objects;
CREATE POLICY "Avatars: public read" ON storage.objects
  FOR SELECT USING (bucket_id = 'avatars');
