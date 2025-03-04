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
def generate_version(commit_count, branch_name, commit_type):
    major = 1
    minor = 0
    patch = commit_count  # Increment patch version with each commit

    if commit_type == "feat":
        # Reset patch version to 0 and increment the minor version for feature commits
        minor += 1
        patch = 0
    elif commit_type == "fix":
        # Increment the patch version for fix commits
        patch = commit_count

    new_version = f"{major}.{minor}.{patch}-{branch_name}"
    return new_version

# Function to get the commit type ('fix' or 'feat') from the commit message
def get_commit_type(commit_message):
    if "feat:" in commit_message:
        return "feat"
    elif "fix:" in commit_message:
        return "fix"
    return None

# Check the current branch
current_branch = get_current_branch()

# Only allow 'develop' or 'dev' branches to run the script
if current_branch not in ['develop', 'dev']:
    print(f"This script only runs on the 'develop' or 'dev' branch! Current branch: {current_branch}")
    sys.exit(1)

# Get the latest commit message to determine the type
commit_message = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).strip().decode()

# Get the commit type ('fix' or 'feat')
commit_type = get_commit_type(commit_message)

if commit_type is None:
    print("Error: Invalid commit type. Please use 'fix:' or 'feat:' in the commit message.")
    sys.exit(1)

# Get the number of commits on the current branch
commit_count = get_commit_count(current_branch)

# Generate the new version based on the commit count and commit type
new_version = generate_version(commit_count, current_branch, commit_type)

# Display the version that will be used
print(f"Version generated for commit: {new_version}")

# End of script

