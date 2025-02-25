import git

# Function to get the current version from a version file or set initial version
def get_current_version():
    # Yeh function version.txt se current version padhega
    try:
        with open('version.txt', 'r') as version_file:
            version = version_file.read().strip()
        return version
    except FileNotFoundError:
        return "1.0.0"  # Agar version.txt nahi milta toh initial version 1.0.0 set karenge

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

# Function to parse commit type
def get_commit_type(commit_message):
    if "BREAKING CHANGE" in commit_message or "feat!" in commit_message:
        return "major"  # Major version increment for breaking changes
    elif "feat:" in commit_message:
        return "minor"  # Minor version increment for new features
    elif "fix:" in commit_message or "perf:" in commit_message:
        return "patch"  # Patch version increment for fixes and performance changes
    else:
        return None  # Agar commit message mein yeh sab nahi hai toh versioning nahi hoga

# Function to update version in version.txt
def update_version_file(new_version):
    with open('version.txt', 'w') as version_file:
        version_file.write(new_version)

# Initialize Git Repo
repo = git.Repo('/home/haressh/ver/myrepo')  # Yahan apni repo ka path dena hoga

# Get the current version
current_version = get_current_version()

# Iterate over the commits
for commit in repo.iter_commits():
    commit_type = get_commit_type(commit.message)
    
    if commit_type:
        # Agar commit type major, minor ya patch hai, toh new version calculate karo
        new_version = calculate_new_version(current_version, commit_type)
        
        # Version.txt file ko new version ke saath update karo
        update_version_file(new_version)
        
        # Version ko git mein commit karen
        repo.git.add('version.txt')
        repo.git.commit(m=f"Update version to {new_version}")
        repo.git.push()
        
        # Current version ko update karen taaki next commit ke liye sahi version ho
        current_version = new_version

