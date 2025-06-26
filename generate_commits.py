#!/usr/bin/env python3
import os
import subprocess
import time
import datetime

# Function to run git commands
def run_git_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode().strip()}")
        return False
    return True

# Function to make a temporary change and commit it
def make_commit(commit_number):
    # Create a temporary file with unique content
    temp_file = f"temp_file_{commit_number}.txt"
    with open(temp_file, "w") as f:
        f.write(f"This is a temporary file for commit #{commit_number}\n")
        f.write(f"Created at: {datetime.datetime.now()}\n")
    
    # Add and commit the file
    run_git_command(f"git add {temp_file}")
    commit_message = f"Commit #{commit_number}: Added temporary file"
    run_git_command(f'git commit -m "{commit_message}"')
    print(f"Created commit #{commit_number}")
    time.sleep(0.1)  # Small delay to ensure unique timestamps

# Function to remove all temporary files
def remove_all_temp_files():
    files = [f for f in os.listdir('.') if f.startswith('temp_file_') and f.endswith('.txt')]
    for file in files:
        os.remove(file)
        print(f"Removed {file}")

# Main function
def main():
    # Check if git repo exists
    if not os.path.exists(".git"):
        print("Not a git repository. Please run this script from the root of your git repository.")
        return
    
    # Save current branch name
    process = subprocess.Popen("git branch --show-current", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    current_branch = stdout.decode().strip()
    
    print(f"Current branch: {current_branch}")
    
    # Generate 50 commits
    print("Generating 50 commits...")
    for i in range(1, 51):
        make_commit(i)
    
    # Create a final commit that removes all temporary files
    print("Creating final cleanup commit...")
    remove_all_temp_files()
    run_git_command('git add .')
    run_git_command('git commit -m "Final commit: Cleaned up all temporary files"')
    
    print("\nCompleted successfully!")
    print("50 commit history has been created and all temporary files have been removed.")
    print("The repository is now back to a clean state with the commit history intact.")

if __name__ == "__main__":
    main() 