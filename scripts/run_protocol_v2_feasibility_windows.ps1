$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedBranch = 'feat/pre-wp7-protocol-v1.1-ui-rebuild'
$Plan = 'configs/protocols/protocol-v2-feasibility-v0.1.json'
$Output = 'results/pilots/protocol-v2-feasibility-v0.1'

if (-not $IsWindows) {
    throw 'T-526 must run in native Windows PowerShell on the validated thesis machine.'
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

$Branch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Branch -ne $ExpectedBranch) {
    throw "Expected branch '$ExpectedBranch'; current branch is '$Branch'."
}

$Dirty = git status --porcelain --untracked-files=all
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to inspect Git working-tree state.'
}
if ($Dirty) {
    throw "Working tree must be clean before T-526. Current changes:`n$Dirty"
}

if (Test-Path $Output) {
    $Existing = Get-ChildItem -Force $Output -ErrorAction SilentlyContinue
    if ($Existing) {
        throw "Pilot output already exists at '$Output'. Do not overwrite retained evidence."
    }
}

Write-Host 'T-526 preflight: locked CPU pilot environment'
uv sync --locked --group protocol-v2-pilot --no-progress
if ($LASTEXITCODE -ne 0) { throw 'uv sync failed.' }

Write-Host 'T-526 preflight: Python/SB3/PyTorch CPU contract'
uv run --locked --group protocol-v2-pilot python -c "import sys, torch, stable_baselines3 as sb3; assert sys.version_info[:2] == (3,12); assert sb3.__version__ == '2.9.0'; assert torch.__version__.startswith('2.9.0'); assert torch.version.cuda is None; assert not torch.cuda.is_available(); print(sys.version); print('SB3', sb3.__version__); print('Torch', torch.__version__, 'CUDA', torch.version.cuda)"
if ($LASTEXITCODE -ne 0) { throw 'CPU scientific dependency preflight failed.' }

Write-Host 'T-526 preflight: complete protocol-v2 focused conformance suite'
uv run --locked --group protocol-v2-pilot python -m unittest discover -s tests -p 'test_protocol_v2*.py' -q
if ($LASTEXITCODE -ne 0) { throw 'Protocol-v2 conformance tests failed.' }

Write-Host 'T-526 physical Phase-A discrimination/method-feasibility gate'
uv run --locked --group protocol-v2-pilot python -m resilient_agents.protocol_v2_feasibility --repo-root . --plan $Plan
if ($LASTEXITCODE -ne 0) { throw 'T-526 feasibility runner failed.' }

Write-Host ''
Write-Host 'T-526 Phase-A gate completed. Retained outputs:'
Get-ChildItem -File $Output | Select-Object Name, Length, LastWriteTime
Write-Host ''
Write-Host 'Do not rerun or delete these outputs. Return/commit the generated results for review before Phase-B severity calibration.'
