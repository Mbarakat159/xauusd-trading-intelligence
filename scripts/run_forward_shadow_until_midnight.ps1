# Run the real MT5 forward-shadow session until local midnight.
# Observation-only: no order API is called by the runner.
# Each completed hour is committed and pushed to GitHub.

$ErrorActionPreference = "Stop"

# Resolve the repository root from this script location, not the caller's
# current directory. This makes the launcher safe to run from anywhere.
$repoRoot = Split-Path -Parent $PSScriptRoot
$outputDir = Join-Path $repoRoot "runtime\forward_shadow"
$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw "Project virtualenv Python not found: $pythonExe"
}

Set-Location -LiteralPath $repoRoot
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

# Make the src-layout package importable without requiring installation.
$env:PYTHONPATH = Join-Path $repoRoot "src"

Write-Host "=== XAUUSD MT5 forward-shadow session ===" -ForegroundColor Cyan
Write-Host "Repository: $repoRoot"
Write-Host "Python: $pythonExe"
Write-Host "PYTHONPATH: $env:PYTHONPATH"
Write-Host "Mode: READ-ONLY / NO TRADING"

# Verify MT5 and the expected Equiti symbol before starting.
$check = @'
import MetaTrader5 as mt5
symbol = "XAUUSD.sd"
ok = mt5.initialize()
print("MT5 initialize:", ok)
if not ok:
    print("MT5 last_error:", mt5.last_error())
    raise SystemExit(2)
info = mt5.symbol_info(symbol)
print("Symbol:", symbol)
print("Symbol available:", info is not None)
if info is None:
    print("MT5 last_error:", mt5.last_error())
    mt5.shutdown()
    raise SystemExit(3)
tick = mt5.symbol_info_tick(symbol)
print("Tick available:", tick is not None)
if tick is None:
    print("MT5 last_error:", mt5.last_error())
    mt5.shutdown()
    raise SystemExit(4)
print("Bid:", tick.bid, "Ask:", tick.ask)
print("Server:", mt5.account_info().server if mt5.account_info() else "unknown")
mt5.shutdown()
'@
$check | & $pythonExe -
if ($LASTEXITCODE -ne 0) {
    throw "MT5/XAUUSD startup validation failed."
}

function Write-CheckpointStatus([datetime]$CheckpointTime) {
    $statusPath = Join-Path $outputDir "LATEST_STATUS.md"
    $files = @(Get-ChildItem -Path $outputDir -Filter "observations_*.jsonl" -File | Sort-Object Name)
    $totalObservations = 0
    $totalErrors = 0
    $lastCapture = "n/a"
    $lastAsOf = "n/a"

    foreach ($file in $files) {
        $lines = @(Get-Content -LiteralPath $file.FullName)
        foreach ($line in $lines) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            try {
                $record = $line | ConvertFrom-Json
                if ($record.record_type -eq "shadow_observation") {
                    $totalObservations++
                    $lastCapture = $record.captured_at
                    $lastAsOf = $record.observation.as_of
                }
                elseif ($record.record_type -eq "source_error") {
                    $totalErrors++
                }
            }
            catch {
                $totalErrors++
            }
        }
    }

    $latestName = if ($files.Count -gt 0) { $files[-1].Name } else { "n/a" }
    $status = @"
# Live Forward-Shadow Status

- Mode: **read-only observation**
- Symbol: **XAUUSD.sd**
- Venue: **EquitiBrokerageSC-Demo**
- Runner: **mt5-forward-runner-v1.0.0**
- Checkpoint time (local): **$($CheckpointTime.ToString("yyyy-MM-dd HH:mm:ss zzz"))**
- Latest hour file: **$latestName**
- Total observations: **$totalObservations**
- Source errors recorded: **$totalErrors**
- Last capture: **$lastCapture**
- Last market timestamp (as_of): **$lastAsOf**

The observations are causal forward captures. They contain versioned observation IDs/digests rather than future outcomes. No orders are submitted by this session.

## Hourly files

$($files | ForEach-Object { "- [$($_.Name)](./$($_.Name))" } | Out-String)
"@
    Set-Content -LiteralPath $statusPath -Value $status -Encoding UTF8
    return $statusPath
}

function Publish-Checkpoint([string]$OutputPath) {
    Write-CheckpointStatus -CheckpointTime (Get-Date) | Out-Null
    $statusPath = Join-Path $outputDir "LATEST_STATUS.md"

    git add -- $OutputPath $statusPath
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "No new checkpoint data to commit."
        return
    }

    $hourName = [IO.Path]::GetFileNameWithoutExtension($OutputPath)
    git commit -m "data: forward shadow checkpoint $hourName"
    if ($LASTEXITCODE -ne 0) {
        throw "Git commit failed."
    }

    git push origin main
    if ($LASTEXITCODE -ne 0) {
        throw "Git push failed. Monitoring stopped so the hourly GitHub guarantee is not silently broken."
    }

    Write-Host "GitHub checkpoint published: $hourName" -ForegroundColor Green
}

while ($true) {
    $now = Get-Date
    $midnight = $now.Date.AddDays(1)
    $remaining = [int][Math]::Floor(($midnight - $now).TotalSeconds)

    if ($remaining -le 0) {
        break
    }

    $segmentSeconds = [Math]::Min(3600, $remaining)
    $hourFile = "observations_{0}.jsonl" -f $now.ToString("yyyy-MM-dd_HH")
    $outputPath = Join-Path $outputDir $hourFile

    Write-Host ""
    Write-Host "Starting hour: $hourFile | duration=$segmentSeconds seconds" -ForegroundColor Yellow

    & $pythonExe -m xauusd_intelligence.mt5_forward_runner --symbol XAUUSD.sd --venue EquitiBrokerageSC-Demo --source MetaTrader5 --output $outputPath --interval 30 --bars 100 --duration $segmentSeconds

    if ($LASTEXITCODE -ne 0) {
        throw "Forward-shadow runner exited with code $LASTEXITCODE."
    }

    Publish-Checkpoint -OutputPath $outputPath
}

Write-CheckpointStatus -CheckpointTime (Get-Date) | Out-Null
Write-Host ""
Write-Host "=== Session reached local midnight. Final checkpoint written. ===" -ForegroundColor Cyan
