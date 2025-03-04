import subprocess
import sys

# Function to get the current branch name
def get_current_branch():
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode()
        return branch
    except subprocess.CalledProcessError:
        print("Error: Not a git repository.")
        sys.exit(1)

# Function to get the number of commits on the current branch
def get_commit_count(branch_name):
    try:
        # Count the number of commits in the current branch
        commit_count = subprocess.check_output(['git', 'rev-list', '--count', branch_name]).strip().decode()
        return int(commit_count)
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve commit count.")
        sys.exit(1)

# Function to generate the version string based on the commit count
def generate_version(commit_count, branch_name):
    # Version starts from 1.0.0, and increment the patch version with each commit
    major = 1
    minor = 0
    patch = commit_count  # Increment patch version with each commit
    new_version = f"{major}.{minor}.{patch}-{branch_name}"
    return new_version

# Check the current branch
current_branch = get_current_branch()

# Only allow 'develop' or 'dev' branches to run the script
if current_branch not in ['develop', 'dev']:
    print(f"This script only runs on the 'develop' or 'dev' branch! Current branch: {current_branch}")
    sys.exit(1)

# Get the number of commits on the current branch
commit_count = get_commit_count(current_branch)

# Generate the new version based on the commit count and branch name
new_version = generate_version(commit_count, current_branch)

# Display the version that will be used
print(f"Current version based on commits: {new_version}")

# End of script

