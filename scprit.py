import git

# Function to get the current version from version.txt or set initial version
def get_current_version_and_branch():
    try:
        with open('version.txt', 'r') as version_file:
            content = version_file.read().strip().split(' ')
            version = content[0]
            branch = content[1] if len(content) > 1 else 'unknown'
        return version, branch
    except FileNotFoundError:
        return "1.0.0", 'main'  # Default version and branch if version.txt doesn't exist

# Function to calculate the new version based on commit type
def calculate_new_version(current_version, commit_type):
    major, minor, patch = map(int, current_version.split('.'))
    
    if commit_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif commit_type == "minor":
        minor += 1
        patch = 0
    elif commit_type == "patch":
        patch += 1
    
    return f"{major}.{minor}.{patch}"

# Function to parse commit type from commit message
def get_commit_type(commit_message):
    print(f"Commit message: {commit_message}")  # Debugging: show commit message
    if "BREAKING CHANGE" in commit_message or "feat!" in commit_message:
        print("Detected as major version change")  # Debugging: major version
        return "major"
    elif "feat:" in commit_message:
        print("Detected as minor version change")  # Debugging: minor version
        return "minor"
    elif "fix:" in commit_message or "perf:" in commit_message:
        print("Detected as patch version change")  # Debugging: patch version
        return "patch"
    else:
        print("No versioning change detected")  # Debugging: no versioning
        return None

# Function to update version in version.txt with branch name
def update_version_file(new_version, branch_name):
    with open('version.txt', 'w') as version_file:
        version_file.write(f"{new_version} {branch_name}")  # Store version and branch name
    print(f"Updated version and branch: {new_version} {branch_name}")  # Debugging print statement

# Initialize Git Repo
repo = git.Repo('/home/haressh/ver/myrepo')  # Yahan apni repo ka path dena hoga

# Get the current version and branch name
current_version, current_branch = get_current_version_and_branch()

# Iterate over the commits
for commit in repo.iter_commits():
    commit_type = get_commit_type(commit.message)
    
    if commit_type:
        # Agar commit type major, minor ya patch hai, toh new version calculate karo
        new_version = calculate_new_version(current_version, commit_type)
        
        # Version.txt file ko new version aur branch ke saath update karo
        update_version_file(new_version, current_branch)
        
        # Version ko git mein commit karen
        repo.git.add('version.txt')
        repo.git.commit(m=f"Update version to {new_version} for branch {current_branch}")
        repo.git.push()
        
        # Current version ko update karen taaki next commit ke liye sahi version ho
        current_version = new_version

