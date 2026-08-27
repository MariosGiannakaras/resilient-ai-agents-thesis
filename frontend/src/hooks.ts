import { useEffect, useState } from 'react'
import { api, type RunRecord } from './api'

export function useRuns() {
  const [runs, setRuns] = useState<RunRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError(null)
    api.runs(controller.signal)
      .then((payload) => setRuns(payload.runs))
      .catch((reason: unknown) => {
        if (!controller.signal.aborted) {
          setError(reason instanceof Error ? reason.message : 'Unknown API error')
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false)
      })
    return () => controller.abort()
  }, [reloadKey])

  return {
    runs,
    loading,
    error,
    reload: () => setReloadKey((key) => key + 1),
  }
}
