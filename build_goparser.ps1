# This script cross-compiles the Go AST parser for Windows, Linux, and macOS.

# Ensure the script is run from the project root directory.
$ErrorActionPreference = "Stop"

$SOURCE_DIR = "agent_docstrings"
$SOURCE_FILE = "$SOURCE_DIR/go_ast_parser.go"
$OUTPUT_DIR = "$SOURCE_DIR/bin"

# Ensure the output directory exists
if (-not (Test-Path -Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
}

# Define build targets [OS, Arch, OutputSuffix]
$targets = @(
    @("windows", "amd64", ".exe"),
    @("linux", "amd64", "_linux_amd64"),
    @("darwin", "amd64", "_darwin_amd64"),
    @("darwin", "arm64", "_darwin_arm64") # For Apple Silicon
)

Write-Host "Starting Go AST parser builds..."

foreach ($target in $targets) {
    $os = $target[0]
    $arch = $target[1]
    $suffix = $target[2]
    $outputFile = "$OUTPUT_DIR/go_ast_parser$suffix"

    Write-Host "Building for: $os/$arch..."
    
    $env:GOOS = $os
    $env:GOARCH = $arch
    
    try {
        go build -o $outputFile -ldflags "-s -w" $SOURCE_FILE
        Write-Host "Successfully built $outputFile" -ForegroundColor Green
    } catch {
        Write-Host "Failed to build for $os/$arch. Error: $_" -ForegroundColor Red
    }
}

# Clean up environment variables
Remove-Item -Path "env:GOOS"
Remove-Item -Path "env:GOARCH"

Write-Host "All builds completed." 