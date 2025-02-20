param (
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    [Parameter(Mandatory=$true)]
    [string]$Name,
    [boolean]$RunPerformance = $True
)

if (!$RunPerformance) {
    Write-Output "Skipping performance tests"
    exit 0
}

$perfSummary = New-Item -ItemType directory -Path $RepoName/test-results/performance-summary -Force

Push-Location $RepoName
try {
    Write-Output "Running Web performance tests"
    python fiftyone_devicedetection_examples/performance-tests/test_performance.py ../assets/51Degrees-LiteV4.1.hash ../assets/"20000 User Agents.csv" --output || $(throw "benchmark failed with code: $LASTEXITCODE")
    
    Write-Output "Running Console performance tests"
    python fiftyone_devicedetection_examples/fiftyone_devicedetection_examples/onpremise/performance.py --data_file ../assets/TAC-HashV41.hash --user_agents_file ../assets/"20000 User Agents.csv" --json_output $pwd/summary.json

    $Results = Get-Content $pwd/summary.json | ConvertFrom-Json
    @{
        HigherIsBetter = @{
            DetectionsPerSecond = $Results.DetectionsPerSecond
        };
        LowerIsBetter = @{
            AvgMillisecsPerDetection = $Results.AvgMillisecsPerDetection
        }
    } | ConvertTo-Json | Out-File $perfSummary/results_$Name.json
} finally {
    Pop-Location
}
