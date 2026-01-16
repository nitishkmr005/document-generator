'use client'

import { useEffect, useState } from 'react'

// Helper function to get cookie value
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    const cookieValue = parts.pop()?.split(';').shift()
    return cookieValue ? decodeURIComponent(cookieValue) : null
  }
  return null
}

// Helper function to delete cookie
function deleteCookie(name: string) {
  document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`
}

export default function AuthRedirectPage() {
  const [redirectPath, setRedirectPath] = useState<string | null>(null)

  useEffect(() => {
    // Small delay to ensure page is fully mounted and cookies are accessible
    const timer = setTimeout(() => {
      // Get the stored redirect path from cookie
      const storedPath = getCookie('authRedirectPath')
      console.log('Auth redirect - stored path from cookie:', storedPath)
      
      // Clear the cookie
      deleteCookie('authRedirectPath')
      
      // Set the path (for display) and redirect
      const targetPath = storedPath || '/'
      setRedirectPath(targetPath)
      
      // Use window.location for redirect
      window.location.href = targetPath
    }, 100)

    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center space-y-4">
        <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto" />
        <p className="text-muted-foreground">Completing sign in...</p>
        {redirectPath && (
          <p className="text-xs text-muted-foreground">Redirecting to {redirectPath}</p>
        )}
      </div>
    </div>
  )
}


