export type HealthPayload = {
  api_schema_version: number
  status: string
  frontend_built: boolean
  active_runtime_service: string
}

export type RunRecord = {
  run_id: string
  status: string
  protocol_version: string
  stage: string
  recorded_at_utc: string
  source_git_commit: string | null
}

export type RunsPayload = {
  api_schema_version: number
  runs: RunRecord[]
}

export type SystemPayload = Record<string, unknown>

async function getJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(path, {
    method: 'GET',
    headers: { Accept: 'application/json' },
    signal,
  })
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`
    try {
      const body = (await response.json()) as { detail?: string }
      if (body.detail) detail = body.detail
    } catch {
      // Preserve the HTTP status when an error body is not JSON.
    }
    throw new Error(detail)
  }
  return (await response.json()) as T
}

export const api = {
  health: (signal?: AbortSignal) => getJson<HealthPayload>('/api/health', signal),
  runs: (signal?: AbortSignal) => getJson<RunsPayload>('/api/runs', signal),
  system: (signal?: AbortSignal) => getJson<SystemPayload>('/api/system', signal),
}
