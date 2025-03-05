#!/bin/bash

# Step 1: Define Base Version
BASE_MAJOR=1
BASE_MINOR=0
BASE_PATCH=0

# Step 2: Fetch commit messages in reverse (oldest to newest)
COMMITS=$(git log --pretty=%s | tac)

# Initialize version
MAJOR=$BASE_MAJOR
MINOR=$BASE_MINOR
PATCH=$BASE_PATCH

# Step 3: Analyze commit messages
for COMMIT in $COMMITS; do
    if [[ $COMMIT == feat\!* || $COMMIT == *"BREAKING CHANGE"* ]]; then
        # Major version bump for 'feat!' or 'BREAKING CHANGE'
        MAJOR=$((MAJOR + 1))
        MINOR=0      # Minor reset
        PATCH=0      # Patch reset
    elif [[ $COMMIT == feat:* ]]; then
        # Minor version bump for 'feat:' (new feature)
        MINOR=$((MINOR + 1))
        PATCH=0      # Patch reset
    elif [[ $COMMIT == fix:* || $COMMIT == perf:* || $COMMIT == refactor:* || $COMMIT == test:* ]]; then
        # Patch version bump for 'fix:', 'perf:', 'refactor:', 'test:'
        PATCH=$((PATCH + 1))
    fi
done

# Step 4: Construct new version
NEW_VERSION="version-$MAJOR.$MINOR.$PATCH-dev"

# Step 5: Print version to terminal only (NO FILE SAVING)
echo "Updated Version: $NEW_VERSION"

