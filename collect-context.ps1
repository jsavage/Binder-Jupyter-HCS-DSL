$rootPath = "C:\Users\consu\OneDrive\Documents\HCS_from_pi\jupyter-DSL"
$outputFile = Join-Path $rootPath "full-context.txt"

$filesToCollect = @(
    "jupyter-lite.json",
    "jupyter-config.json",
    "example-HCS.txt",
    "content\startup\00-hcs-processor.py"
)

# Create or clear the output file
"" | Set-Content $outputFile

foreach ($file in $filesToCollect) {
    $fullPath = Join-Path $rootPath $file
    if (Test-Path $fullPath) {
        "=== BEGIN $file ===" | Add-Content $outputFile
        Get-Content $fullPath | Add-Content $outputFile
        "=== END $file ===" | Add-Content $outputFile
        "`n`n" | Add-Content $outputFile
    }
}
