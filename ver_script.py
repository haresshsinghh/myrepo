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

# Function to get the latest commit message
def get_latest_commit_message():
    try:
        commit_message = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).strip().decode()
        return commit_message
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve latest commit message.")
        sys.exit(1)

# Function to get the number of commits on the current branch
def get_commit_count(branch_name):
    try:
        # Count the number of commits in the current branch
        commit_count = subprocess.check_output(['git', 'rev-list', '--count', branch_name]).strip().decode()
        return int(commit_count)
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve commit count. Please make sure the repository is initialized correctly.")
        sys.exit(1)

# Function to determine commit type based on commit message
def get_commit_type(commit_message):
    if "feat:" in commit_message:
        return "feat"
    elif "fix:" in commit_message:
        return "fix"
    return None

# Function to generate the version string based on the commit count
def generate_version(commit_count, branch_name, commit_type, last_feat_commit=None):
    major = 1
    minor = 0
    patch = commit_count  # Increment patch version with each commit

    if commit_type == "feat":
        # Reset patch version to 0 and increment the minor version for feature commits
        minor += 1
        patch = 0
    elif commit_type == "fix":
        # Increment the patch version for fix commits after a feat commit
        if last_feat_commit is not None:
            # Get the commit count from the last feat commit
            patch = commit_count - last_feat_commit  # Count fix commits after feat commit
        else:
            patch = commit_count

    new_version = f"{major}.{minor}.{patch}-{branch_name}"
    return new_version

# Main function to run the versioning process
def main():
    current_branch = get_current_branch()
    commit_message = get_latest_commit_message()

    # Determine the type of commit
    commit_type = get_commit_type(commit_message)

    if not commit_type:
        print(f"Skipping version update. No feat/fix commit detected in: {commit_message}")
        return

    # Get the total number of commits in the current branch
    commit_count = get_commit_count(current_branch)

    # Generate version
    version = generate_version(commit_count, current_branch, commit_type)
    print(f"Version generated for commit: {version}")

# Run the script
if __name__ == "__main__":
    main()

