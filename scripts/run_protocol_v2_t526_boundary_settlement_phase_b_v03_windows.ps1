$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedBranch = 'feat/pre-wp7-protocol-v1.1-ui-rebuild'
$Repository = 'MariosGiannakaras/resilient-ai-agents-thesis'
$PullRequest = 92
$Config = 'configs/protocols/protocol-v2-t526-boundary-settlement-phase-b-v0.3.json'
$SettlementOutput = 'results/pilots/protocol-v2-feasibility-boundary-settlement-v0.1'
$PhaseBOutput = 'results/pilots/protocol-v2-feasibility-phase-b-v0.3'
$RequiredInputs = @(
    'results/pilots/protocol-v2-feasibility-v0.1',
    'results/pilots/protocol-v2-feasibility-v0.1-recovery',
    'results/pilots/protocol-v2-feasibility-v0.1-recovery-v0.2',
    'results/pilots/protocol-v2-feasibility-phase-b-v0.2'
)
$RequiredChecks = @('sanity', 'focused-conformance')
$Git = 'C:\Program Files\Git\cmd\git.exe'
$Gh = 'C:\Program Files\GitHub CLI\gh.exe'
$Uv = Join-Path $env:USERPROFILE '.local\bin\uv.exe'

if ($env:OS -ne 'Windows_NT') {
    throw 'DEC-054 T-526A must run in native Windows PowerShell on the validated thesis machine.'
}
foreach ($Tool in @($Git, $Gh, $Uv)) {
    if (-not (Test-Path $Tool -PathType Leaf)) {
        throw "Required native tool not found: '$Tool'."
    }
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

$Branch = (& $Git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Branch -ne $ExpectedBranch) {
    throw "Expected branch '$ExpectedBranch'; current branch is '$Branch'."
}
$Dirty = & $Git status --porcelain --untracked-files=all
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect native-Windows Git state.' }
if ($Dirty) {
    throw "Working tree must be clean before DEC-054 physical execution. Current changes:`n$Dirty"
}

& $Git fetch origin $ExpectedBranch
if ($LASTEXITCODE -ne 0) { throw 'Unable to fetch the active reviewed branch.' }
$LocalHead = (& $Git rev-parse HEAD).Trim()
$RemoteHead = (& $Git rev-parse "origin/$ExpectedBranch").Trim()
if ($LASTEXITCODE -ne 0 -or $LocalHead -ne $RemoteHead) {
    throw "Local HEAD '$LocalHead' does not equal current remote branch HEAD '$RemoteHead'."
}

$PrJson = & $Gh pr view $PullRequest --repo $Repository --json headRefName,headRefOid,isDraft,state,statusCheckRollup
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect draft PR #92.' }
$Pr = $PrJson | ConvertFrom-Json
if ($Pr.state -ne 'OPEN' -or -not $Pr.isDraft) {
    throw 'PR #92 must remain open and draft for DEC-054 T-526A.'
}
if ($Pr.headRefName -ne $ExpectedBranch -or $Pr.headRefOid -ne $LocalHead) {
    throw 'PR #92 does not point to the clean local/current remote reviewed HEAD.'
}
foreach ($CheckName in $RequiredChecks) {
    $Matches = @($Pr.statusCheckRollup | Where-Object { $_.name -eq $CheckName })
    if ($Matches.Count -ne 1 -or $Matches[0].status -ne 'COMPLETED' -or $Matches[0].conclusion -ne 'SUCCESS') {
        throw "Required reviewed-head check '$CheckName' is not green."
    }
}

foreach ($InputDirectory in $RequiredInputs) {
    if (-not (Test-Path $InputDirectory -PathType Container)) {
        throw "Required immutable input evidence is missing: '$InputDirectory'."
    }
}
foreach ($Output in @($SettlementOutput, $PhaseBOutput)) {
    if (Test-Path $Output) {
        $Existing = Get-ChildItem -Force $Output -ErrorAction SilentlyContinue
        if ($Existing) { throw "Retained output already exists at '$Output'; do not overwrite it." }
    }
}

Write-Host 'DEC-054 T-526A preflight: locked CPU pilot environment'
& $Uv sync --locked --group protocol-v2-pilot --no-progress
if ($LASTEXITCODE -ne 0) { throw 'uv sync failed.' }

Write-Host 'DEC-054 T-526A preflight: Python/SB3/PyTorch CPU contract'
& $Uv run --locked --group protocol-v2-pilot python -c "import sys, torch, stable_baselines3 as sb3; assert sys.version_info[:2] == (3,12); assert sb3.__version__ == '2.9.0'; assert torch.__version__.startswith('2.9.0'); assert torch.version.cuda is None; assert not torch.cuda.is_available(); print(sys.version); print('SB3', sb3.__version__); print('Torch', torch.__version__, 'CUDA', torch.version.cuda)"
if ($LASTEXITCODE -ne 0) { throw 'CPU scientific dependency preflight failed.' }

Write-Host 'DEC-054 T-526A preflight: immutable input validation'
& $Uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t526_boundary_phase_b_v03 --repo-root . --config $Config --validate-inputs-only
if ($LASTEXITCODE -ne 0) { throw 'DEC-054 immutable input validation failed.' }

Write-Host 'DEC-054 T-526A preflight: boundary and affected conformance tests'
& $Uv run --locked --group protocol-v2-pilot python -m unittest `
    tests.test_protocol_v2_boundary_settlement `
    tests.test_protocol_v2_t526_recovery_v02 `
    tests.test_protocol_v2_prefix `
    tests.test_protocol_v2_executor `
    tests.test_protocol_v2_sb3_phase_b `
    tests.test_protocol_v2_tabular_driver `
    tests.test_protocol_v2_tabular_phase_b -q
if ($LASTEXITCODE -ne 0) { throw 'DEC-054 focused conformance tests failed.' }

Write-Host 'DEC-054 T-526A zero-interaction settlement and fresh Phase-B v0.3'
& $Uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t526_boundary_phase_b_v03 --repo-root . --config $Config
if ($LASTEXITCODE -ne 0) { throw 'DEC-054 settlement/Phase-B runner failed; retain all output.' }

Write-Host 'DEC-054 T-526A independent generated-evidence validation'
& $Uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t526_boundary_phase_b_v03 --repo-root . --config $Config --validate-attempt-only
if ($LASTEXITCODE -ne 0) { throw 'DEC-054 generated-evidence validation failed.' }

Write-Host ''
Write-Host 'DEC-054 T-526A / T-526 physical gate completed. Retained outputs:'
Get-ChildItem -File -Recurse $SettlementOutput, $PhaseBOutput |
    Measure-Object -Property Length -Sum |
    Select-Object Count, Sum
Write-Host 'Do not rerun, delete, replace or hand-edit either evidence directory.'
