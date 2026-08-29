$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedBranch = 'feat/pre-wp7-protocol-v1.1-ui-rebuild'
$Repository = 'MariosGiannakaras/resilient-ai-agents-thesis'
$PullRequest = 92
$Amendment = 'configs/protocols/protocol-v2-t526-recovery-phase-b-v0.1.json'
$RecoveryOutput = 'results/pilots/protocol-v2-feasibility-v0.1-recovery'
$PhaseBOutput = 'results/pilots/protocol-v2-feasibility-phase-b-v0.1'
# GitHub exposes job/check names in statusCheckRollup. These map to the
# Repository checks and Protocol-v2 pilot checks workflows respectively.
$RequiredChecks = @('sanity', 'focused-conformance')

if (-not $IsWindows) {
    throw 'T-526A must run in native Windows PowerShell on the validated thesis machine.'
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

$Branch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Branch -ne $ExpectedBranch) {
    throw "Expected branch '$ExpectedBranch'; current branch is '$Branch'."
}

$Dirty = git status --porcelain --untracked-files=all
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect native-Windows Git state.' }
if ($Dirty) {
    throw "Working tree must be clean before T-526A physical execution. Current changes:`n$Dirty"
}

git fetch origin $ExpectedBranch
if ($LASTEXITCODE -ne 0) { throw 'Unable to fetch the active reviewed branch.' }
$LocalHead = (git rev-parse HEAD).Trim()
$RemoteHead = (git rev-parse "origin/$ExpectedBranch").Trim()
if ($LASTEXITCODE -ne 0 -or $LocalHead -ne $RemoteHead) {
    throw "Local HEAD '$LocalHead' does not equal current remote branch HEAD '$RemoteHead'."
}

$PrJson = gh pr view $PullRequest --repo $Repository --json headRefName,headRefOid,isDraft,state,statusCheckRollup
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect draft PR #92.' }
$Pr = $PrJson | ConvertFrom-Json
if ($Pr.state -ne 'OPEN' -or -not $Pr.isDraft) {
    throw 'PR #92 must remain open and draft for T-526A.'
}
if ($Pr.headRefName -ne $ExpectedBranch -or $Pr.headRefOid -ne $LocalHead) {
    throw 'PR #92 does not point to the clean local/current remote HEAD.'
}
foreach ($CheckName in $RequiredChecks) {
    $Matches = @($Pr.statusCheckRollup | Where-Object { $_.name -eq $CheckName })
    if ($Matches.Count -ne 1 -or $Matches[0].status -ne 'COMPLETED' -or $Matches[0].conclusion -ne 'SUCCESS') {
        throw "Required reviewed-head check '$CheckName' is not green."
    }
}

foreach ($Output in @($RecoveryOutput, $PhaseBOutput)) {
    if (Test-Path $Output) {
        $Existing = Get-ChildItem -Force $Output -ErrorAction SilentlyContinue
        if ($Existing) { throw "Retained output already exists at '$Output'; do not overwrite it." }
    }
}

Write-Host 'T-526A preflight: locked CPU pilot environment'
uv sync --locked --group protocol-v2-pilot --no-progress
if ($LASTEXITCODE -ne 0) { throw 'uv sync failed.' }

Write-Host 'T-526A preflight: Python/SB3/PyTorch CPU contract'
uv run --locked --group protocol-v2-pilot python -c "import sys, torch, stable_baselines3 as sb3; assert sys.version_info[:2] == (3,12); assert sb3.__version__ == '2.9.0'; assert torch.__version__.startswith('2.9.0'); assert torch.version.cuda is None; assert not torch.cuda.is_available(); print(sys.version); print('SB3', sb3.__version__); print('Torch', torch.__version__, 'CUDA', torch.version.cuda)"
if ($LASTEXITCODE -ne 0) { throw 'CPU scientific dependency preflight failed.' }

Write-Host 'T-526A preflight: recovery and affected protocol-v2 conformance tests'
uv run --locked --group protocol-v2-pilot python -m unittest `
    tests.test_protocol_v2_t526_recovery `
    tests.test_protocol_v2_feasibility `
    tests.test_protocol_v2_executor `
    tests.test_protocol_v2_prefix `
    tests.test_protocol_v2_sb3_phase_b `
    tests.test_protocol_v2_tabular_phase_b -q
if ($LASTEXITCODE -ne 0) { throw 'T-526A focused conformance tests failed.' }

Write-Host 'T-526A physical deterministic checkpoint materialization and Phase-B calibration'
uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t526_recovery --repo-root . --amendment $Amendment
if ($LASTEXITCODE -ne 0) { throw 'T-526A recovery/Phase-B runner failed; retain all diagnostic output.' }

Write-Host 'T-526A independent generated-evidence validation'
uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t526_recovery --repo-root . --amendment $Amendment --validate-only
if ($LASTEXITCODE -ne 0) { throw 'T-526A generated-evidence validation failed.' }

Write-Host ''
Write-Host 'T-526A / T-526 physical gate completed. Retained outputs:'
Get-ChildItem -File -Recurse $RecoveryOutput, $PhaseBOutput |
    Measure-Object -Property Length -Sum |
    Select-Object Count, Sum
Write-Host 'Do not rerun, delete, replace or hand-edit either evidence directory.'
