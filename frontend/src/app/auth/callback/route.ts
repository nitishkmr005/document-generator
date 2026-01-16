import { NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')
  const error = requestUrl.searchParams.get('error')
  const errorDescription = requestUrl.searchParams.get('error_description')
  const origin = requestUrl.origin

  // Handle OAuth errors
  if (error) {
    console.error('OAuth error:', error, errorDescription)
    return NextResponse.redirect(`${origin}/?error=${encodeURIComponent(errorDescription || error)}`)
  }

  if (code) {
    const supabase = await createClient()
    if (supabase) {
      const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code)
      if (exchangeError) {
        console.error('Session exchange error:', exchangeError.message)
        return NextResponse.redirect(`${origin}/?error=${encodeURIComponent(exchangeError.message)}`)
      }
    } else {
      console.error('Supabase client not initialized')
      return NextResponse.redirect(`${origin}/?error=supabase_not_configured`)
    }
  }

  // Redirect to the auth redirect page which handles cookie-based redirect
  return NextResponse.redirect(`${origin}/auth/redirect`)
}
