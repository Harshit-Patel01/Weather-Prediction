# PowerShell script to generate 50 commits and then clean up

# Function to run git commands
function Run-GitCommand {
    param (
        [string]$command
    )
    
    try {
        Invoke-Expression $command
        return $true
    }
    catch {
        Write-Host "Error: $_"
        return $false
    }
}

# Function to make a temporary change and commit it
function Make-Commit {
    param (
        [int]$commitNumber
    )
    
    # Create a temporary file with unique content
    $tempFile = "temp_file_$commitNumber.txt"
    $content = "This is a temporary file for commit #$commitNumber`r`n"
    $content += "Created at: $(Get-Date)`r`n"
    Set-Content -Path $tempFile -Value $content
    
    # Add and commit the file
    Run-GitCommand "git add $tempFile"
    $commitMessage = "Commit #$commitNumber`: Added temporary file"
    Run-GitCommand "git commit -m `"$commitMessage`""
    Write-Host "Created commit #$commitNumber"
    Start-Sleep -Milliseconds 100  # Small delay to ensure unique timestamps
}

# Function to remove all temporary files
function Remove-AllTempFiles {
    $files = Get-ChildItem -Path . -Filter "temp_file_*.txt"
    foreach ($file in $files) {
        Remove-Item -Path $file.FullName
        Write-Host "Removed $($file.Name)"
    }
}

# Main function
function Main {
    # Check if git repo exists
    if (-not (Test-Path ".git")) {
        Write-Host "Not a git repository. Please run this script from the root of your git repository."
        return
    }
    
    # Save current branch name
    $currentBranch = git branch --show-current
    Write-Host "Current branch: $currentBranch"
    
    # Generate 50 commits
    Write-Host "Generating 50 commits..."
    for ($i = 1; $i -le 50; $i++) {
        Make-Commit -commitNumber $i
    }
    
    # Create a final commit that removes all temporary files
    Write-Host "Creating final cleanup commit..."
    Remove-AllTempFiles
    Run-GitCommand "git add ."
    Run-GitCommand "git commit -m `"Final commit: Cleaned up all temporary files`""
    
    Write-Host "`nCompleted successfully!"
    Write-Host "50 commit history has been created and all temporary files have been removed."
    Write-Host "The repository is now back to a clean state with the commit history intact."
}

# Run the main function
Main 