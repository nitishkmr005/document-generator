import Link from "next/link";
import { Button } from "@/components/ui/button";

function RefractionIllustration() {
  return (
    <div className="relative w-full max-w-3xl mx-auto">
      {/* Ambient glow background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-cyan-500/20 via-violet-500/20 to-fuchsia-500/20 rounded-full blur-3xl animate-pulse" />
      </div>
      
      <svg
        viewBox="0 0 600 240"
        className="w-full"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          {/* Enhanced prism gradient with 3D effect */}
          <linearGradient id="prism-main" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#0891b2', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#7c3aed', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#c026d3', stopOpacity: 1 }} />
          </linearGradient>
          
          {/* Prism highlight for 3D effect */}
          <linearGradient id="prism-highlight" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: 'white', stopOpacity: 0.4 }} />
            <stop offset="50%" style={{ stopColor: 'white', stopOpacity: 0.1 }} />
            <stop offset="100%" style={{ stopColor: 'white', stopOpacity: 0 }} />
          </linearGradient>
          
          {/* Prism shadow for depth */}
          <linearGradient id="prism-shadow" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style={{ stopColor: 'black', stopOpacity: 0 }} />
            <stop offset="100%" style={{ stopColor: 'black', stopOpacity: 0.3 }} />
          </linearGradient>
          
          {/* Rainbow ray gradients */}
          <linearGradient id="ray-red" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#ef4444', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#ef4444', stopOpacity: 0 }} />
          </linearGradient>
          <linearGradient id="ray-orange" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#f97316', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#f97316', stopOpacity: 0 }} />
          </linearGradient>
          <linearGradient id="ray-yellow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#eab308', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#eab308', stopOpacity: 0 }} />
          </linearGradient>
          <linearGradient id="ray-green" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#22c55e', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#22c55e', stopOpacity: 0 }} />
          </linearGradient>
          <linearGradient id="ray-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#06b6d4', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#06b6d4', stopOpacity: 0 }} />
          </linearGradient>
          <linearGradient id="ray-blue" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#3b82f6', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#3b82f6', stopOpacity: 0 }} />
          </linearGradient>
          <linearGradient id="ray-violet" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#8b5cf6', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#8b5cf6', stopOpacity: 0 }} />
          </linearGradient>
          
          {/* Input beam gradient */}
          <linearGradient id="input-beam" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: '#f8fafc', stopOpacity: 0.3 }} />
            <stop offset="100%" style={{ stopColor: '#f8fafc', stopOpacity: 0.9 }} />
          </linearGradient>
          
          {/* Glow filters */}
          <filter id="glow-strong">
            <feGaussianBlur stdDeviation="4" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          
          <filter id="glow-soft">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          
          <filter id="drop-shadow">
            <feDropShadow dx="0" dy="4" stdDeviation="4" floodColor="#7c3aed" floodOpacity="0.3" />
          </filter>
        </defs>

        {/* Input sources with modern card style */}
        <g>
          {/* PDF Source */}
          <g transform="translate(30, 40)">
            <rect x="0" y="0" width="50" height="40" rx="8" fill="white" className="dark:fill-slate-800" stroke="#e2e8f0" strokeWidth="1" />
            <rect x="0" y="0" width="50" height="40" rx="8" fill="url(#prism-highlight)" />
            <text x="25" y="25" textAnchor="middle" fontSize="12" fontWeight="600" fill="#dc2626">PDF</text>
          </g>
          
          {/* URL Source */}
          <g transform="translate(30, 100)">
            <rect x="0" y="0" width="50" height="40" rx="8" fill="white" className="dark:fill-slate-800" stroke="#e2e8f0" strokeWidth="1" />
            <rect x="0" y="0" width="50" height="40" rx="8" fill="url(#prism-highlight)" />
            <circle cx="25" cy="18" r="8" fill="none" stroke="#2563eb" strokeWidth="1.5" />
            <ellipse cx="25" cy="18" rx="3" ry="8" fill="none" stroke="#2563eb" strokeWidth="1" />
            <text x="25" y="35" textAnchor="middle" fontSize="9" fontWeight="500" fill="#2563eb">URL</text>
          </g>
          
          {/* Text Source */}
          <g transform="translate(30, 160)">
            <rect x="0" y="0" width="50" height="40" rx="8" fill="white" className="dark:fill-slate-800" stroke="#e2e8f0" strokeWidth="1" />
            <rect x="0" y="0" width="50" height="40" rx="8" fill="url(#prism-highlight)" />
            <text x="25" y="25" textAnchor="middle" fontSize="12" fontWeight="600" fill="#7c3aed">TXT</text>
          </g>
        </g>

        {/* Converging input beams with arrows */}
        <g>
          {/* Arrow marker definition */}
          <defs>
            <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
              <path d="M0,0 L0,6 L9,3 z" fill="#94a3b8" />
            </marker>
          </defs>
          
          {/* Input lines with arrows */}
          <line x1="85" y1="60" x2="210" y2="115" stroke="#94a3b8" strokeWidth="2.5" strokeLinecap="round" markerEnd="url(#arrow)">
            <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite" />
          </line>
          <line x1="85" y1="120" x2="210" y2="120" stroke="#94a3b8" strokeWidth="2.5" strokeLinecap="round" markerEnd="url(#arrow)">
            <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" begin="0.3s" />
          </line>
          <line x1="85" y1="180" x2="210" y2="125" stroke="#94a3b8" strokeWidth="2.5" strokeLinecap="round" markerEnd="url(#arrow)">
            <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite" begin="0.6s" />
          </line>
        </g>

        {/* Central Prism with 3D effect and AI label */}
        <g transform="translate(220, 50)" filter="url(#drop-shadow)">
          {/* Main prism body */}
          <polygon points="80,0 160,140 0,140" fill="url(#prism-main)" />
          {/* Highlight face for 3D */}
          <polygon points="80,0 160,140 80,140" fill="url(#prism-shadow)" />
          {/* Top highlight edge */}
          <polygon points="80,0 110,70 50,70" fill="url(#prism-highlight)" />
          {/* Border */}
          <polygon points="80,0 160,140 0,140" fill="none" stroke="rgba(255,255,255,0.5)" strokeWidth="2" />
          
          {/* AI Label inside prism */}
          <text x="80" y="95" textAnchor="middle" fontSize="24" fontWeight="700" fill="white" opacity="0.9" style={{ fontFamily: 'system-ui' }}>
            AI
          </text>
          
          {/* Inner glow */}
          <circle cx="80" cy="90" r="30" fill="white" opacity="0.1">
            <animate attributeName="r" values="25;35;25" dur="3s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.08;0.15;0.08" dur="3s" repeatCount="indefinite" />
          </circle>
        </g>

        {/* Rainbow output rays with staggered animations */}
        <g transform="translate(380, 120)" filter="url(#glow-soft)">
          {/* Red */}
          <line x1="0" y1="0" x2="180" y2="-80" stroke="url(#ray-red)" strokeWidth="4" strokeLinecap="round">
            <animate attributeName="x2" values="170;190;170" dur="2s" repeatCount="indefinite" />
          </line>
          {/* Orange */}
          <line x1="0" y1="0" x2="190" y2="-55" stroke="url(#ray-orange)" strokeWidth="4" strokeLinecap="round">
            <animate attributeName="x2" values="180;200;180" dur="2s" repeatCount="indefinite" begin="0.1s" />
          </line>
          {/* Yellow */}
          <line x1="0" y1="0" x2="195" y2="-28" stroke="url(#ray-yellow)" strokeWidth="4" strokeLinecap="round">
            <animate attributeName="x2" values="185;205;185" dur="2s" repeatCount="indefinite" begin="0.2s" />
          </line>
          {/* Green */}
          <line x1="0" y1="0" x2="200" y2="0" stroke="url(#ray-green)" strokeWidth="4" strokeLinecap="round">
            <animate attributeName="x2" values="190;210;190" dur="2s" repeatCount="indefinite" begin="0.3s" />
          </line>
          {/* Cyan */}
          <line x1="0" y1="0" x2="195" y2="28" stroke="url(#ray-cyan)" strokeWidth="4" strokeLinecap="round">
            <animate attributeName="x2" values="185;205;185" dur="2s" repeatCount="indefinite" begin="0.4s" />
          </line>
          {/* Blue */}
          <line x1="0" y1="0" x2="190" y2="55" stroke="url(#ray-blue)" strokeWidth="4" strokeLinecap="round">
            <animate attributeName="x2" values="180;200;180" dur="2s" repeatCount="indefinite" begin="0.5s" />
          </line>
          {/* Violet */}
          <line x1="0" y1="0" x2="180" y2="80" stroke="url(#ray-violet)" strokeWidth="4" strokeLinecap="round">
            <animate attributeName="x2" values="170;190;170" dur="2s" repeatCount="indefinite" begin="0.6s" />
          </line>
        </g>

        {/* Output labels with modern styling */}
        <g style={{ fontFamily: 'system-ui' }}>
          <text x="560" y="45" textAnchor="end" fontSize="12" fontWeight="600" fill="#ef4444">PDF Report</text>
          <text x="570" y="70" textAnchor="end" fontSize="12" fontWeight="600" fill="#f97316">Slides</text>
          <text x="575" y="95" textAnchor="end" fontSize="12" fontWeight="600" fill="#eab308">Markdown</text>
          <text x="580" y="120" textAnchor="end" fontSize="12" fontWeight="600" fill="#22c55e">Blog Post</text>
          <text x="575" y="145" textAnchor="end" fontSize="12" fontWeight="600" fill="#06b6d4">Mind Map</text>
          <text x="570" y="170" textAnchor="end" fontSize="12" fontWeight="600" fill="#3b82f6">FAQ Cards</text>
          <text x="560" y="195" textAnchor="end" fontSize="12" fontWeight="600" fill="#8b5cf6">Podcast</text>
        </g>
      </svg>
    </div>
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
            <h3 className="text-lg font-semibold">AI</h3>
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
