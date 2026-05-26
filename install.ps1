# PaperScholar Installer — Windows PowerShell
param([string]$Target = "all")

Write-Host "🎓 PaperScholar Installer" -ForegroundColor Cyan
Write-Host "Target: $Target"

pip install openai gradio --quiet

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CodexSkills = "$env:USERPROFILE\.codex\skills"
$ClaudeSkills = "$env:USERPROFILE\.claude\skills"
$ClaudeCommands = "$env:USERPROFILE\.claude\commands"

if ($Target -in @("all","codex")) {
    New-Item -ItemType Directory -Force -Path "$CodexSkills\paperscholar" | Out-Null
    Copy-Item "$ScriptDir\dist\codex\skills\paperscholar\*" "$CodexSkills\paperscholar\" -Recurse -Force
    Write-Host "✅ Installed to Codex: $CodexSkills\paperscholar" -ForegroundColor Green
}
if ($Target -in @("all","claude")) {
    New-Item -ItemType Directory -Force -Path $ClaudeSkills, $ClaudeCommands | Out-Null
    Get-ChildItem "$ScriptDir\dist\claude\skills" -Directory | ForEach-Object {
        $dest = Join-Path $ClaudeSkills $_.Name
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
        Copy-Item "$($_.FullName)\*" $dest -Recurse -Force
    }
    Copy-Item "$ScriptDir\dist\claude\commands\paperscholar.md" $ClaudeCommands -Force
    Write-Host "✅ Installed to Claude Code" -ForegroundColor Green
}
Write-Host "`n🎉 Done! Web UI: python src/web_ui.py → http://localhost:7860" -ForegroundColor Cyan
