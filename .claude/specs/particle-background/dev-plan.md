# Development Plan: ParticleBackground Component

## Issue Reference
- **Issue**: #27 [Epic 2-Task 1] Create Canvas-based particle system component
- **Priority**: P0 (Critical)
- **Labels**: feature, ui, animation, phase-1

## Requirements Summary
1. Fullscreen canvas component (position: fixed, 100vw x 100vh)
2. requestAnimationFrame-driven render loop
3. Window resize listener with canvas size updates
4. Enable/disable rendering via prop
5. External particle drawing (component provides canvas infrastructure only)
6. 90%+ test coverage

## API Design

```typescript
interface ParticleBackgroundProps {
  enabled?: boolean // default: true
  onFrame: (ctx: CanvasRenderingContext2D, meta: FrameMeta) => void
  onResize?: (meta: ResizeMeta) => void
  className?: string
  style?: React.CSSProperties
}

interface FrameMeta {
  width: number
  height: number
  dpr: number
  time: number
  delta: number
}

interface ResizeMeta {
  width: number
  height: number
  dpr: number
}
```

## Task Breakdown

### Task 1: Component API & Skeleton
- **ID**: task-1
- **Type**: default
- **Backend**: codex
- **Scope**: `src/components/ParticleBackground.tsx`
- **Dependencies**: none
- **Description**: Create component skeleton with props interface and basic structure
- **Test Command**: N/A (no tests yet)

### Task 2: RAF + Resize Lifecycle
- **ID**: task-2
- **Type**: default
- **Backend**: codex
- **Scope**: `src/components/ParticleBackground.tsx`
- **Dependencies**: task-1
- **Description**: Implement requestAnimationFrame loop, resize handling, cleanup
- **Test Command**: N/A (no tests yet)

### Task 3: Test Framework Setup
- **ID**: task-3
- **Type**: default
- **Backend**: codex
- **Scope**: `package.json`, `vitest.config.ts`, `src/test/setup.ts`
- **Dependencies**: none
- **Description**: Add Vitest + React Testing Library + jsdom + coverage config
- **Test Command**: `npm run test`

### Task 4: Component Tests (90%+ Coverage)
- **ID**: task-4
- **Type**: default
- **Backend**: codex
- **Scope**: `src/components/__tests__/ParticleBackground.test.tsx`
- **Dependencies**: task-2, task-3
- **Description**: Write comprehensive tests for RAF, resize, cleanup, onFrame
- **Test Command**: `npm run test -- --coverage`

## Dependency Graph

```
task-1 ──► task-2 ──┐
                    ├──► task-4
task-3 ─────────────┘
```

## Success Criteria
- [ ] Component renders fullscreen fixed canvas
- [ ] requestAnimationFrame drives render loop
- [ ] Window resize updates canvas dimensions
- [ ] enabled prop controls rendering on/off
- [ ] onFrame callback receives correct meta
- [ ] 90%+ test coverage achieved
