import Link from "next/link";
import { Button } from "@/components/ui/button";

function RefractionIllustration() {
  return (
    <svg
      viewBox="0 0 550 200"
      className="w-full max-w-2xl mx-auto"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="prism-fill" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{ stopColor: '#0891b2', stopOpacity: 0.95 }} />
          <stop offset="50%" style={{ stopColor: '#7c3aed', stopOpacity: 0.95 }} />
          <stop offset="100%" style={{ stopColor: '#c026d3', stopOpacity: 0.95 }} />
        </linearGradient>
        <linearGradient id="ray-teal" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style={{ stopColor: '#06d6a0' }} />
          <stop offset="100%" style={{ stopColor: '#06d6a0', stopOpacity: 0.1 }} />
        </linearGradient>
        <linearGradient id="ray-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style={{ stopColor: '#0891b2' }} />
          <stop offset="100%" style={{ stopColor: '#0891b2', stopOpacity: 0.1 }} />
        </linearGradient>
        <linearGradient id="ray-violet" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style={{ stopColor: '#7c3aed' }} />
          <stop offset="100%" style={{ stopColor: '#7c3aed', stopOpacity: 0.1 }} />
        </linearGradient>
        <linearGradient id="ray-fuchsia" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style={{ stopColor: '#c026d3' }} />
          <stop offset="100%" style={{ stopColor: '#c026d3', stopOpacity: 0.1 }} />
        </linearGradient>
        <linearGradient id="ray-rose" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style={{ stopColor: '#e11d48' }} />
          <stop offset="100%" style={{ stopColor: '#e11d48', stopOpacity: 0.1 }} />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <filter id="icon-shadow">
          <feDropShadow dx="0" dy="2" stdDeviation="2" floodOpacity="0.15" />
        </filter>
      </defs>

      {/* Input Sources - Multiple icons */}
      {/* PDF Icon */}
      <g transform="translate(20, 35)" filter="url(#icon-shadow)">
        <rect x="0" y="0" width="36" height="44" rx="4" fill="#fee2e2" stroke="#fca5a5" strokeWidth="1.5" />
        <text x="18" y="28" textAnchor="middle" fontSize="10" fontWeight="600" fill="#dc2626">PDF</text>
      </g>

      {/* URL/Globe Icon */}
      <g transform="translate(20, 90)" filter="url(#icon-shadow)">
        <rect x="0" y="0" width="36" height="44" rx="4" fill="#dbeafe" stroke="#93c5fd" strokeWidth="1.5" />
        <circle cx="18" cy="20" r="10" fill="none" stroke="#2563eb" strokeWidth="1.5" />
        <ellipse cx="18" cy="20" rx="4" ry="10" fill="none" stroke="#2563eb" strokeWidth="1" />
        <line x1="8" y1="20" x2="28" y2="20" stroke="#2563eb" strokeWidth="1" />
      </g>

      {/* DOCX Icon */}
      <g transform="translate(20, 145)" filter="url(#icon-shadow)">
        <rect x="0" y="0" width="36" height="44" rx="4" fill="#ddd6fe" stroke="#a78bfa" strokeWidth="1.5" />
        <text x="18" y="28" textAnchor="middle" fontSize="9" fontWeight="600" fill="#7c3aed">DOCX</text>
      </g>

      {/* Input labels */}
      <g style={{ fontFamily: 'system-ui' }}>
        <text x="66" y="62" fill="#64748b" fontSize="11" fontWeight="500">PDF</text>
        <text x="66" y="117" fill="#64748b" fontSize="11" fontWeight="500">URL</text>
        <text x="66" y="172" fill="#64748b" fontSize="11" fontWeight="500">DOCX</text>
      </g>

      {/* Converging beams from inputs to prism */}
      <g>
        {/* From PDF */}
        <line x1="95" y1="57" x2="185" y2="100" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" />
        {/* From URL */}
        <line x1="95" y1="112" x2="185" y2="100" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" />
        {/* From DOCX */}
        <line x1="95" y1="167" x2="185" y2="100" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" />
        {/* Arrow heads */}
        <polygon points="185,100 175,95 175,105" fill="#94a3b8" />
      </g>

      {/* Prism */}
      <g transform="translate(185, 45)" filter="url(#glow)">
        <polygon points="55,0 110,110 0,110" fill="url(#prism-fill)" />
        <polygon points="55,0 110,110 0,110" fill="none" stroke="rgba(255,255,255,0.4)" strokeWidth="1.5" />
      </g>

      {/* Output rays */}
      <g transform="translate(295, 100)" filter="url(#glow)">
        <line x1="0" y1="0" x2="150" y2="-60" stroke="url(#ray-teal)" strokeWidth="3" strokeLinecap="round" />
        <line x1="0" y1="0" x2="160" y2="-28" stroke="url(#ray-cyan)" strokeWidth="3" strokeLinecap="round" />
        <line x1="0" y1="0" x2="165" y2="5" stroke="url(#ray-violet)" strokeWidth="3" strokeLinecap="round" />
        <line x1="0" y1="0" x2="160" y2="40" stroke="url(#ray-fuchsia)" strokeWidth="3" strokeLinecap="round" />
        <line x1="0" y1="0" x2="145" y2="70" stroke="url(#ray-rose)" strokeWidth="3" strokeLinecap="round" />
      </g>

      {/* Output labels */}
      <g style={{ fontFamily: 'system-ui' }}>
        <text x="450" y="45" fill="#06d6a0" fontSize="13" fontWeight="600">PDF</text>
        <text x="460" y="77" fill="#0891b2" fontSize="13" fontWeight="600">PPTX</text>
        <text x="465" y="110" fill="#7c3aed" fontSize="13" fontWeight="600">Markdown</text>
        <text x="460" y="143" fill="#c026d3" fontSize="13" fontWeight="600">Mind Map</text>
        <text x="445" y="173" fill="#e11d48" fontSize="13" fontWeight="600">Podcast</text>
      </g>
    </svg>
  );
}

export default function HomePage() {
  return (
    <div className="relative overflow-hidden">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-28">
        <div className="flex flex-col items-center text-center space-y-8 max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div className="inline-flex items-center rounded-full border px-4 py-1.5 text-sm font-medium bg-gradient-to-r from-cyan-50 to-fuchsia-50 dark:from-cyan-950/50 dark:to-fuchsia-950/50 border-violet-200 dark:border-violet-800">
            <span className="bg-gradient-to-r from-cyan-600 via-violet-600 to-fuchsia-600 bg-clip-text text-transparent">
              AI-Powered Document Generation
            </span>
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl max-w-4xl">
            Multiple Sources.{" "}
            <span className="bg-gradient-to-r from-cyan-500 via-violet-500 to-fuchsia-500 bg-clip-text text-transparent">
              Many Formats.
            </span>
          </h1>

          <p className="text-lg text-muted-foreground max-w-2xl md:text-xl leading-relaxed">
            Transform PDFs, URLs, and documents into professional reports,
            presentations, mind maps, and more. Bring your own LLM API key
            and watch your content refract into any format.
          </p>

          <div className="flex flex-col gap-4 sm:flex-row">
            <Button asChild size="lg" className="h-12 px-8 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700">
              <Link href="/generate">Start Generating</Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="h-12 px-8">
              <a href="https://github.com/nitishkmr005/document-generator" target="_blank" rel="noopener noreferrer">
                View on GitHub
              </a>
            </Button>
          </div>
        </div>

        {/* Refraction Illustration */}
        <div className="mt-16 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-300">
          <RefractionIllustration />
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-4 py-16 border-t">
        <h2 className="text-2xl font-bold text-center mb-4">
          How It Works
        </h2>
        <p className="text-center text-muted-foreground mb-12 max-w-2xl mx-auto">
          Like light through a prism, your content refracts into multiple professional formats
        </p>

        <div className="grid gap-6 md:grid-cols-3 max-w-5xl mx-auto">
          {/* Input Card */}
          <div className="group relative flex flex-col items-center text-center space-y-4 p-6 rounded-xl border bg-card transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/10 hover:-translate-y-1">
            <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-cyan-100 to-cyan-50 dark:from-cyan-900/50 dark:to-cyan-950/50 flex items-center justify-center">
              <svg className="h-7 w-7 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Any Source</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Upload PDFs, Word docs, images, or paste URLs and plain text. We parse and understand it all.
            </p>
            <div className="flex flex-wrap justify-center gap-2 pt-2">
              <span className="px-2 py-1 text-xs rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300">PDF</span>
              <span className="px-2 py-1 text-xs rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300">URL</span>
              <span className="px-2 py-1 text-xs rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300">DOCX</span>
              <span className="px-2 py-1 text-xs rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300">Images</span>
            </div>
            {/* Connector arrow (hidden on mobile) */}
            <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 text-muted-foreground/30">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>

          {/* Transform Card */}
          <div className="group relative flex flex-col items-center text-center space-y-4 p-6 rounded-xl border bg-card transition-all duration-300 hover:shadow-lg hover:shadow-violet-500/10 hover:-translate-y-1">
            <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-violet-100 to-violet-50 dark:from-violet-900/50 dark:to-violet-950/50 flex items-center justify-center">
              <svg className="h-7 w-7 text-violet-600" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polygon points="12,2 22,20 2,20" strokeWidth={2} strokeLinejoin="round" />
                <circle cx="12" cy="14" r="2" fill="currentColor" stroke="none" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold">AI Prism</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Your content passes through our AI-powered prism, transforming and restructuring intelligently.
            </p>
            <div className="flex flex-wrap justify-center gap-2 pt-2">
              <span className="px-2 py-1 text-xs rounded-full bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300">Claude</span>
              <span className="px-2 py-1 text-xs rounded-full bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300">Gemini</span>
              <span className="px-2 py-1 text-xs rounded-full bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300">OpenAI</span>
            </div>
            {/* Connector arrow (hidden on mobile) */}
            <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 text-muted-foreground/30">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>

          {/* Output Card */}
          <div className="group flex flex-col items-center text-center space-y-4 p-6 rounded-xl border bg-card transition-all duration-300 hover:shadow-lg hover:shadow-fuchsia-500/10 hover:-translate-y-1">
            <div className="h-14 w-14 rounded-xl bg-gradient-to-br from-fuchsia-100 to-fuchsia-50 dark:from-fuchsia-900/50 dark:to-fuchsia-950/50 flex items-center justify-center">
              <svg className="h-7 w-7 text-fuchsia-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Many Formats</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Download your content refracted into multiple professional formats, ready to share.
            </p>
            <div className="flex flex-wrap justify-center gap-2 pt-2">
              <span className="px-2 py-1 text-xs rounded-full bg-fuchsia-100 dark:bg-fuchsia-900/30 text-fuchsia-700 dark:text-fuchsia-300">PDF</span>
              <span className="px-2 py-1 text-xs rounded-full bg-fuchsia-100 dark:bg-fuchsia-900/30 text-fuchsia-700 dark:text-fuchsia-300">PPTX</span>
              <span className="px-2 py-1 text-xs rounded-full bg-fuchsia-100 dark:bg-fuchsia-900/30 text-fuchsia-700 dark:text-fuchsia-300">Mind Map</span>
              <span className="px-2 py-1 text-xs rounded-full bg-fuchsia-100 dark:bg-fuchsia-900/30 text-fuchsia-700 dark:text-fuchsia-300">Podcast</span>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center space-y-6 p-8 rounded-2xl bg-gradient-to-br from-violet-50 to-fuchsia-50 dark:from-violet-950/30 dark:to-fuchsia-950/30 border border-violet-100 dark:border-violet-900/50">
          <h2 className="text-2xl font-bold">Ready to transform your content?</h2>
          <p className="text-muted-foreground">
            Bring your own API key and start generating professional documents in seconds.
          </p>
          <Button asChild size="lg" className="h-12 px-8 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700">
            <Link href="/generate">Get Started Free</Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
