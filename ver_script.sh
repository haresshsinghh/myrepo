#!/bin/bash

# Enable error handling
set -e  # Agar koi bhi command fail hoti hai toh script turant band ho jaayegi

# Error handling function
error_exit() {
    echo "$1" 1>&2  # Error message print karna
    exit 1  # Script ko exit karwana
}

# Step 1: Get the current version from dev branch
CURRENT_VERSION=$(git tag --list "v20.0.1-dev" | tail -n 1) || error_exit "Current version ko fetch karne mein error aayi."

# Extracting the version number
BASE_MAJOR=20
BASE_MINOR=0
BASE_PATCH=1

if [[ -n "$CURRENT_VERSION" ]]; then
    # Extracting major, minor, patch from the current version tag
    VERSION_NUMBER=$(echo "$CURRENT_VERSION" | sed 's/v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)-dev/\1 \2 \3/')
    read BASE_MAJOR BASE_MINOR BASE_PATCH <<< "$VERSION_NUMBER"
fi

# Step 2: Commit messages ko reverse mein fetch karna (oldest se newest)
COMMITS=$(git log --pretty=%s | tac) || error_exit "Git se commits fetch karne mein error aayi."

# Version ko initialize karna
MAJOR=$BASE_MAJOR
MINOR=$BASE_MINOR
PATCH=$BASE_PATCH

# Step 3: Commit messages ko line-by-line analyze karna
while IFS= read -r COMMIT; do
    # Leading/trailing spaces ko trim karna
    COMMIT=$(echo "$COMMIT" | xargs)

    # Agar commit mein kuch galat ho, toh error print karna
    if [[ $COMMIT == "" ]]; then
        continue  # Empty commit ko skip kar dena
    fi

    if [[ $COMMIT == feat\!* || "$COMMIT" =~ "BREAKING CHANGE" ]]; then
        # 'feat!' ya 'BREAKING CHANGE' ke liye major version bump
        MAJOR=$((MAJOR + 1))
        MINOR=0  # Minor version ko reset karna
        PATCH=0  # Patch version ko reset karna
    elif [[ $COMMIT == feat:* ]]; then
        # 'feat:' ke liye minor version bump
        MINOR=$((MINOR + 1))
        PATCH=0  # Patch version ko reset karna
    elif [[ $COMMIT == fix:* || $COMMIT == perf:* || $COMMIT == refactor:* || $COMMIT == test:* ]]; then
        # 'fix:', 'perf:', 'refactor:', 'test:' ke liye patch version bump
        PATCH=$((PATCH + 1))
    fi
done <<< "$COMMITS"

# Step 4: Naya version construct karna
NEW_VERSION="v$MAJOR.$MINOR.$PATCH-dev"

# Step 5: Version ko terminal par print karna (file mein save nahi karenge)
echo "Updated Version: $NEW_VERSION"

# Optional: Agar script ka koi part fail ho jaata hai toh error print karna
if [[ $? -ne 0 ]]; then
    error_exit "Script mein koi error aayi thi."
fi

