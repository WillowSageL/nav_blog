# Repository Guidelines

## 项目结构与模块组织
- `src/app/`：Next.js App Router 页面与布局入口。
- `src/components/`：可复用 UI 与业务组件；`src/components/ui/` 为基础组件（shadcn 风格）。
- `src/lib/`：Supabase 客户端、服务层与工具函数。
- `src/types/`：TypeScript 类型声明。
- `public/`：静态资源（图标、图片等）。
- `database.sql`：Supabase 初始化脚本；文档见 `QUICK_START.md` / `NEXTJS_SUPABASE_TUTORIAL.md`。

## 构建、测试与开发命令
- `npm install`：安装依赖。
- `npm run dev`：本地开发（Next.js + Turbopack）。
- `npm run build`：生产构建。
- `npm run start`：启动生产服务。
- `npm run lint`：运行 ESLint（Next.js 规则集）。

## 编码风格与命名规范
- 采用 TypeScript + React；缩进 2 空格、无分号、字符串优先单引号（与现有代码一致）。
- 组件与文件名用 PascalCase（如 `UserProfileEditor.tsx`），hooks 用 `useXxx` 命名。
- Tailwind CSS 为主，样式入口在 `src/app/globals.css`；避免全局样式污染。

## 测试指南
- 当前仓库未配置自动化测试框架；提交前至少通过 `npm run lint`。
- 若新增测试，请统一放在 `src/**/__tests__/` 或 `*.test.tsx`，并在 `package.json` 增加对应脚本与说明。

## 提交与 PR 指南
- 历史提交多为 `type: summary` 形式（如 `feat:` / `fix:` / `refactor:`，中英文均可），请保持一致与简洁。
- PR 需包含：变更摘要、关键设计说明；涉及 UI 的请附截图；涉及数据库变更需同步更新 `database.sql`。

## 安全与配置提示
- 环境变量放在 `.env.local`，包含 `NEXT_PUBLIC_SUPABASE_URL` 与 `NEXT_PUBLIC_SUPABASE_ANON_KEY`，严禁提交到仓库。
- 密码与认证细节参考 `PASSWORD_SECURITY_GUIDE.md`。
