import subprocess

def get_commit_history():
    # Git log command to fetch commit history for the current branch (develop)
    result = subprocess.run(['git', 'log', '--oneline'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').split('\n')

def get_current_branch():
    # Git command to get the current branch
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

def calculate_version_for_fix_feature_major(commit_history):
    major, minor, patch = 1, 0, 0  # Starting version: 1.0.0 for develop branch
    fix_commits = 0
    feature_commits = 0
    major_change_commits = 0
    feature_incremented = False  # To ensure minor increments only once

    # Iterate through commit history and classify commits
    for commit in commit_history:
        print(f"Processing commit: {commit}")  # Debugging line
        if 'fix' in commit.lower():  # Identifying fix commits
            fix_commits += 1
        elif 'feature' in commit.lower() or 'feat' in commit.lower():  # Identifying feature commits
            feature_commits += 1
        elif 'major' in commit.lower() or 'breaking' in commit.lower():  # Identifying major breaking change commits
            major_change_commits += 1

    # Debugging the commit counts
    print(f"Fix commits: {fix_commits}, Feature commits: {feature_commits}, Major commits: {major_change_commits}")

    # Update patch version based on fix commits
    patch += fix_commits

    # Update minor version based on feature commits (only increment minor once)
    if feature_commits > 0 and not feature_incremented:
        minor += 1  # Increment minor version only once after the first feature commit
        feature_incremented = True

    # Update major version if there are major breaking change commits
    major += major_change_commits

    # If major breaking change occurs, reset patch and minor
    if major_change_commits > 0:
        minor = 0
        patch = 0

    version = f"{major}.{minor}.{patch}-develop"
    return version

def main():
    # Ensure the script runs only for the develop branch
    current_branch = get_current_branch()
    if current_branch != 'develop':
        print("This script only runs on the develop branch!")
        return

    # Get the commit history for the develop branch
    commit_history = get_commit_history()

    # Calculate the new version based on fix, feature, and major breaking change commits
    version = calculate_version_for_fix_feature_major(commit_history)

    # Output the new version
    print(f"New version for develop branch (fix, feature, and major commits): {version}")

if __name__ == '__main__':
    main()
