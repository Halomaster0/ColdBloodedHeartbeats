# WEB_DEV.md - Web Development Directive

> This file serves as a specialized instruction layer for all web development tasks. It aligns the agent's orchestration with the USER's specific aesthetic and architectural preferences.

## 🎨 Core Design Principles (The "Halom" Standard)

Follow these principles for every new website or refinement task to ensure a "WOW" factor by default:

1. **Advanced Glassmorphism**: Use translucent backgrounds (`rgba(255, 255, 255, 0.4)`), heavy blurs (`16px+`), and subtle borders to create depth and a premium feel.
2. **Generous Whitespace**: Avoid "crowded" layouts. Prioritize large margins and padding. If in doubt, add more breathing room.
3. **Micro-Animations**: Implement subtle hover scales (e.g., `transform: scale(1.03)`), smooth transitions (`cubic-bezier`), and entrance "reveals" on scroll.
4. **Vibrant & Harmonious Palettes**: Avoid default browser colors. Use curated HSL palettes (Deep Espresso, Warm Latte, Muted Sage) that feel sophisticated and cohesive.
5. **Modern Typography**: Default to high-quality Google Fonts (e.g., Outfit, Playfair Display, Inter). Use clear hierarchy through weight and size.

## 🏗️ Technical Architecture

### Layer 1: Structure (HTML)
- Use strict Semantic HTML5 (`<main>`, `<section>`, `<header>`).
- Ensure every interactive element has a unique ID for easier browser verification.

### Layer 2: Styling (CSS)
- **Vanilla First**: Prioritize Vanilla CSS with CSS Variables (`:root`) unless Tailwind is explicitly requested.
- **Design Tokens**: Centralize tokens for radius, spacing, and shadows to ensure consistency across the whole app.

### Layer 3: Logic (JS)
- **Unified Initialization**: Consolidate all DOM events into a single entry point.
- **Robustness**: Implement strict validation for inputs and flows (e.g., multi-step booking validation).

## 🔄 The Collaborative Workflow

1. **Directive-First**: Check `directives/` for any existing SOPs (e.g., mock data generation) before manual work.
2. **Proactive Verification**: Always use the `browser_subagent` to verify UI changes and functional flows. Capturing recordings is mandatory for successful proof-of-work.
3. **Execution Mode**: When moving to EXECUTION, prioritize clean, commented code over quick hacks. Consolidate edits into `multi_replace_file_content` to minimize noise.
4. **Self-Annealing**: If a layout element breaks on mobile or CORS blocks a local fetch, troubleshoot and fix it immediately before reporting progress.

## 🚀 Mindset: High-End Artisan

Approach every website as a high-end studio project, not a minimum viable product. Think like an artisan:
- Is the spacing comfortable?
- Does the button feel "clickable"?
- Is the data structure clean and reusable?
- Would this design "WOW" a premium client?

---
*Follow this directive to minimize prompting and maximize visual excellence.*
