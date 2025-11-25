$BlenderPath = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
$TestScript = "blender_addon/tests/test_addon.py"
$PythonExpr = "import bpy; bpy.ops.test.mcp_addon()"
$TempLogFile = Join-Path $env:TEMP "blender_test_output.log"

if (-not (Test-Path $BlenderPath)) {
    Write-Error "Blender executable not found at: $BlenderPath"
    exit 1
}

Write-Host "Running Blender Tests..."
Write-Host "Blender: $BlenderPath"
Write-Host "Test Script: $TestScript"
Write-Host "Output redirected to: $TempLogFile"

# Execute Blender and redirect all output to a temporary log file
& $BlenderPath -b --python $TestScript --python-expr $PythonExpr *>&1 | Out-File -FilePath $TempLogFile -Encoding UTF8

# Read the log file content
$LogContent = Get-Content $TempLogFile -Raw

# Output the log content to the console for visibility
Write-Host "\n--- Blender Output ---"
Write-Host $LogContent
Write-Host "--- End Blender Output ---\n"

# Check for failure string
if ($LogContent -like "*Blender Addon tests failed.*") {
    Write-Host "Tests Failed! Check log above for details." -ForegroundColor Red
    Remove-Item $TempLogFile -ErrorAction SilentlyContinue
    exit 1
} else {
    Write-Host "Tests Passed!" -ForegroundColor Green
    Remove-Item $TempLogFile -ErrorAction SilentlyContinue
    exit 0
}