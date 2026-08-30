$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedBranch = 'feat/pre-wp7-protocol-v1.1-ui-rebuild'
$Repository = 'MariosGiannakaras/resilient-ai-agents-thesis'
$PullRequest = 92
$Config = 'configs/protocols/protocol-v2-t527-sizing-retry-v0.2.json'
$TuningInput = 'results/pilots/protocol-v2-t527-tuning-v0.1'
$FailedSizingInput = 'results/pilots/protocol-v2-t527-sizing-v0.1'
$SizingOutput = 'results/pilots/protocol-v2-t527-sizing-v0.2'
$RequiredChecks = @('sanity', 'focused-conformance')
$Git = 'C:\Program Files\Git\cmd\git.exe'
$Gh = 'C:\Program Files\GitHub CLI\gh.exe'
$Uv = Join-Path $env:USERPROFILE '.local\bin\uv.exe'

if ($env:OS -ne 'Windows_NT') {
    throw 'DEC-056 T-527 sizing-v0.2 must run on the authoritative native Windows thesis host.'
}
foreach ($Tool in @($Git, $Gh, $Uv)) {
    if (-not (Test-Path $Tool -PathType Leaf)) { throw "Required native tool not found: '$Tool'." }
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot
$Branch = (& $Git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Branch -ne $ExpectedBranch) {
    throw "Expected branch '$ExpectedBranch'; current branch is '$Branch'."
}
$Dirty = & $Git status --porcelain --untracked-files=all
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect native-Windows Git state.' }
if ($Dirty) { throw "Working tree must be clean before DEC-056 physical execution. Current changes:`n$Dirty" }

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

foreach ($Input in @($TuningInput, $FailedSizingInput)) {
    if (-not (Test-Path $Input -PathType Container)) { throw "Retained DEC-055 input is missing: '$Input'." }
}
if (Test-Path $SizingOutput) {
    $Existing = Get-ChildItem -Force $SizingOutput -ErrorAction SilentlyContinue
    if ($Existing) { throw "Retained output already exists at '$SizingOutput'; do not overwrite or resume it." }
}

Write-Host 'DEC-056 preflight: locked CPU pilot environment'
& $Uv sync --locked --group protocol-v2-pilot --no-progress
if ($LASTEXITCODE -ne 0) { throw 'uv sync failed.' }

Write-Host 'DEC-056 preflight: Python/SB3/PyTorch CPU contract'
& $Uv run --locked --group protocol-v2-pilot python -c "import sys, torch, stable_baselines3 as sb3; assert sys.version_info[:2] == (3,12); assert sb3.__version__ == '2.9.0'; assert torch.__version__.startswith('2.9.0'); assert torch.version.cuda is None; assert not torch.cuda.is_available(); print(sys.version); print('SB3', sb3.__version__); print('Torch', torch.__version__, 'CUDA', torch.version.cuda)"
if ($LASTEXITCODE -ne 0) { throw 'CPU scientific dependency preflight failed.' }

Write-Host 'DEC-056 preflight: immutable T-526 and retained DEC-055 evidence validation'
& $Uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t527_sizing_v02 --repo-root . --config $Config --validate-inputs-only
if ($LASTEXITCODE -ne 0) { throw 'Retained input validation failed.' }

Write-Host 'DEC-056 preflight: focused representation/lifecycle/sizing tests'
& $Uv run --locked --group protocol-v2-pilot python -m unittest `
    tests.test_protocol_v2_t527 `
    tests.test_protocol_v2_gridworld `
    tests.test_protocol_v2_tabular_phase_b `
    tests.test_protocol_v2_sb3_phase_b `
    tests.test_protocol_v2_feasibility `
    tests.test_evidence_v2_statistics -q
if ($LASTEXITCODE -ne 0) { throw 'DEC-056 focused tests failed.' }

Write-Host 'DEC-056: one fresh non-final physical sizing-v0.2 execution (tuning is not executed)'
& $Uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t527_sizing_v02 --repo-root . --config $Config
if ($LASTEXITCODE -ne 0) { throw 'DEC-056 physical sizing failed; retain all output and do not resume or rerun.' }

Write-Host 'DEC-056: independent generated-evidence validation'
& $Uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_t527_sizing_v02 --repo-root . --config $Config --validate-attempt-only
if ($LASTEXITCODE -ne 0) { throw 'DEC-056 generated-evidence validation failed.' }

Write-Host ''
Write-Host 'DEC-056 T-527 sizing-v0.2 completed. Retained output:'
Get-ChildItem -File -Recurse $SizingOutput |
    Measure-Object -Property Length -Sum |
    Select-Object Count, Sum
Write-Host 'Do not rerun, resume, delete, replace or hand-edit the evidence directory.'
