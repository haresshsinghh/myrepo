import subprocess

def get_commit_history():
    # Git log command to fetch commit history for the current branch (develop)
    result = subprocess.run(['git', 'log', '--oneline'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').split('\n')

def get_current_branch():
    # Git command to get the current branch
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

def calculate_version_for_fix_and_feature(commit_history):
    major, minor, patch = 1, 9, 5  # Starting version: 1.9.5 for develop branch
    fix_commits = 0
    feature_commits = 0
    major_change_commits = 0
    
    # Iterate through commit history and count fix, feature, and major change commits
    for commit in commit_history:
        if 'fix' in commit.lower():  # Identifying fix commits
            fix_commits += 1
        elif 'feature' in commit.lower() or 'feat' in commit.lower():  # Identifying feature commits
            feature_commits += 1
        elif 'breaking' in commit.lower() or 'major' in commit.lower():  # Identifying major breaking change commits
            major_change_commits += 1
    
    # Handle major breaking change commits
    if major_change_commits > 0:
        major += major_change_commits  # Major version increases on breaking changes
        minor = 0  # Reset minor version after a major change
        patch = 0  # Reset patch version after a major change
    else:
        # Increment minor version for each feature commit and reset patch version
        if feature_commits > 0:
            minor += feature_commits
            patch = 0  # Reset patch version after a feature commit
        
        # Increment patch version for each fix commit
        patch += fix_commits

    # Format version for the develop branch (fix, feature, and major commits)
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

    # Calculate the new version based on fix, feature, and major commits
    version = calculate_version_for_fix_and_feature(commit_history)

    # Output the new version
    print(f"New version for develop branch (fix, feature, and major commits): {version}")

if __name__ == '__main__':
    main()

