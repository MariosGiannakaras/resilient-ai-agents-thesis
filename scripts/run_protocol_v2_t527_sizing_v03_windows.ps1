$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedBranch = 'feat/pre-wp7-protocol-v1.1-ui-rebuild'
$Repository = 'MariosGiannakaras/resilient-ai-agents-thesis'
$PullRequest = 92
$Config = 'configs/protocols/protocol-v2-t527-sizing-completion-v0.3.json'
$TuningInput = 'results/pilots/protocol-v2-t527-tuning-v0.1'
$SizingV01Input = 'results/pilots/protocol-v2-t527-sizing-v0.1'
$SizingV02Input = 'results/pilots/protocol-v2-t527-sizing-v0.2'
$FreshOutput = 'results/pilots/protocol-v2-t527-sizing-v0.3'
$CombinedOutput = 'results/pilots/protocol-v2-t527-sizing-combined-v0.3'
$RequiredChecks = @('sanity', 'focused-conformance')
$Git = 'C:\Program Files\Git\cmd\git.exe'
$Gh = 'C:\Program Files\GitHub CLI\gh.exe'
$Uv = Join-Path $env:USERPROFILE '.local\bin\uv.exe'

function Invoke-NativeCaptured {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string]$ArgumentString
    )
    $StdoutPath = [IO.Path]::GetTempFileName()
    $StderrPath = [IO.Path]::GetTempFileName()
    try {
        $Process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentString `
            -WorkingDirectory $RepoRoot -RedirectStandardOutput $StdoutPath `
            -RedirectStandardError $StderrPath -Wait -PassThru
        $Stdout = Get-Content -Raw $StdoutPath -ErrorAction SilentlyContinue
        $Stderr = Get-Content -Raw $StderrPath -ErrorAction SilentlyContinue
        if ($Stdout) { Write-Host $Stdout.TrimEnd() }
        if ($Stderr) { Write-Host $Stderr.TrimEnd() }
        return [pscustomobject]@{
            ExitCode = $Process.ExitCode
            Stdout = if ($Stdout) { $Stdout } else { '' }
            Stderr = if ($Stderr) { $Stderr } else { '' }
        }
    }
    finally {
        Remove-Item -Force $StdoutPath, $StderrPath -ErrorAction SilentlyContinue
    }
}

if ($env:OS -ne 'Windows_NT') {
    throw 'DEC-057 T-527 sizing-v0.3 must run on the authoritative native Windows thesis host.'
}
foreach ($Tool in @($Git, $Gh, $Uv)) {
    if (-not (Test-Path $Tool -PathType Leaf)) { throw "Required native tool not found: '$Tool'." }
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot
$GitResult = Invoke-NativeCaptured $Git 'branch --show-current'
$Branch = $GitResult.Stdout.Trim()
if ($GitResult.ExitCode -ne 0 -or $Branch -ne $ExpectedBranch) {
    throw "Expected branch '$ExpectedBranch'; current branch is '$Branch'."
}
$GitResult = Invoke-NativeCaptured $Git 'status --porcelain --untracked-files=all'
$Dirty = $GitResult.Stdout.Trim()
if ($GitResult.ExitCode -ne 0) { throw 'Unable to inspect native-Windows Git state.' }
if ($Dirty) { throw "Working tree must be clean before DEC-057 physical execution. Current changes:`n$Dirty" }

$GitResult = Invoke-NativeCaptured $Git "fetch origin $ExpectedBranch"
if ($GitResult.ExitCode -ne 0) { throw 'Unable to fetch the active reviewed branch.' }
$GitResult = Invoke-NativeCaptured $Git 'rev-parse HEAD'
$LocalHead = $GitResult.Stdout.Trim()
if ($GitResult.ExitCode -ne 0) { throw 'Unable to resolve local HEAD.' }
$GitResult = Invoke-NativeCaptured $Git "rev-parse origin/$ExpectedBranch"
$RemoteHead = $GitResult.Stdout.Trim()
if ($GitResult.ExitCode -ne 0 -or $LocalHead -ne $RemoteHead) {
    throw "Local HEAD '$LocalHead' does not equal current remote branch HEAD '$RemoteHead'."
}

$GhResult = Invoke-NativeCaptured $Gh "pr view $PullRequest --repo $Repository --json headRefName,headRefOid,isDraft,state,statusCheckRollup"
if ($GhResult.ExitCode -ne 0) { throw 'Unable to inspect draft PR #92.' }
$Pr = $GhResult.Stdout | ConvertFrom-Json
if ($Pr.state -ne 'OPEN' -or -not $Pr.isDraft) { throw 'PR #92 must remain open and draft.' }
if ($Pr.headRefName -ne $ExpectedBranch -or $Pr.headRefOid -ne $LocalHead) {
    throw 'PR #92 does not point to the clean local/current remote reviewed HEAD.'
}
foreach ($CheckName in $RequiredChecks) {
    $Matches = @($Pr.statusCheckRollup | Where-Object { $_.name -eq $CheckName })
    if ($Matches.Count -ne 1 -or $Matches[0].status -ne 'COMPLETED' -or $Matches[0].conclusion -ne 'SUCCESS') {
        throw "Required reviewed-head check '$CheckName' is not green."
    }
}

foreach ($Input in @($TuningInput, $SizingV01Input, $SizingV02Input)) {
    if (-not (Test-Path $Input -PathType Container)) { throw "Retained T-527 input is missing: '$Input'." }
}
foreach ($Output in @($FreshOutput, $CombinedOutput)) {
    if (Test-Path $Output) {
        $Existing = Get-ChildItem -Force $Output -ErrorAction SilentlyContinue
        if ($Existing) { throw "Retained output already exists at '$Output'; do not overwrite or resume it." }
    }
}

Write-Host 'DEC-057 preflight: locked CPU pilot environment'
$UvResult = Invoke-NativeCaptured $Uv 'sync --locked --group protocol-v2-pilot --no-progress'
if ($UvResult.ExitCode -ne 0) { throw 'uv sync failed.' }

Write-Host 'DEC-057 preflight: Python/SB3/PyTorch CPU contract'
$UvResult = Invoke-NativeCaptured $Uv 'run --locked --group protocol-v2-pilot python -c "import sys, torch, stable_baselines3 as sb3; assert sys.version_info[:2] == (3,12); assert sb3.__version__ == ''2.9.0''; assert torch.__version__.startswith(''2.9.0''); assert torch.version.cuda is None; assert not torch.cuda.is_available(); print(sys.version); print(''SB3'', sb3.__version__); print(''Torch'', torch.__version__, ''CUDA'', torch.version.cuda)"'
if ($UvResult.ExitCode -ne 0) { throw 'CPU scientific dependency preflight failed.' }

Write-Host 'DEC-057 preflight: immutable histories and Q-Learning/SARSA structural reuse barrier'
$UvResult = Invoke-NativeCaptured $Uv "run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t527_sizing_v03 --repo-root . --config $Config --validate-inputs-only"
if ($UvResult.ExitCode -ne 0) { throw 'DEC-057 retained-input/reuse validation failed.' }

Write-Host 'DEC-057 preflight: focused direct-ingress/lifecycle/sizing tests'
$UvResult = Invoke-NativeCaptured $Uv 'run --locked --group protocol-v2-pilot python -m unittest tests.test_protocol_v2_prefix tests.test_protocol_v2_sb3_driver tests.test_protocol_v2_sb3_phase_b tests.test_protocol_v2_t527 tests.test_protocol_v2_gridworld tests.test_protocol_v2_tabular_phase_b tests.test_protocol_v2_feasibility tests.test_study_protocol_v2_executors tests.test_study_protocol_v2_phase_b_executor tests.test_evidence_v2_statistics -q'
if ($UvResult.ExitCode -ne 0) { throw 'DEC-057 focused tests failed.' }

Write-Host 'DEC-057: one fresh DQN/PPO/Dyna-Q+ sizing-v0.3 execution and derived five-method composition'
$UvResult = Invoke-NativeCaptured $Uv "run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t527_sizing_v03 --repo-root . --config $Config"
if ($UvResult.ExitCode -ne 0) { throw 'DEC-057 physical sizing/composition failed; retain all output and do not resume or rerun.' }

Write-Host 'DEC-057: independent fresh and combined evidence validation'
$UvResult = Invoke-NativeCaptured $Uv "run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t527_sizing_v03 --repo-root . --config $Config --validate-fresh-only"
if ($UvResult.ExitCode -ne 0) { throw 'DEC-057 fresh evidence validation failed.' }
$UvResult = Invoke-NativeCaptured $Uv "run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t527_sizing_v03 --repo-root . --config $Config --validate-combined-only"
if ($UvResult.ExitCode -ne 0) { throw 'DEC-057 combined evidence validation failed.' }

Write-Host ''
Write-Host 'DEC-057 T-527 sizing completion validated. Retained outputs:'
foreach ($Output in @($FreshOutput, $CombinedOutput)) {
    Write-Host $Output
    Get-ChildItem -File -Recurse $Output |
        Measure-Object -Property Length -Sum |
        Select-Object Count, Sum
}
Write-Host 'Do not rerun, resume, delete, replace or hand-edit either evidence directory.'
