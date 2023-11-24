#!/bin/bash

# Replace these variables with your GitHub credentials and repository information
GITHUB_USERNAME="$1"
GITHUB_TOKEN="$2"
REPO_NAME="$3"
REPO_DESCRIPTION="Repository created for terraform"
PRIVATE_REPO=true

# GitHub API endpoint
API_URL="https://api.github.com/user/repos"

# JSON data for the repository creation
JSON_DATA=$(cat <<EOF
{
  "name": "$REPO_NAME",
  "description": "$REPO_DESCRIPTION",
  "private": $PRIVATE_REPO
}
EOF
)

# Create the GitHub repository
create_repo() {
  curl -s -H "Authorization: token $GITHUB_TOKEN" -d "$JSON_DATA" $API_URL
}

# Main script
main() {
  # Check if 'curl' is installed
  if ! command -v curl &>/dev/null; then
    echo "Error: 'curl' is required but not installed. Aborting."
    exit 1
  fi

  # Check if GitHub token is provided
  if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GitHub personal access token not provided. Please set the GITHUB_TOKEN variable."
    exit 1
  fi

  # Check if GitHub username is provided
  if [ -z "$GITHUB_USERNAME" ]; then
    echo "Error: GitHub username not provided. Please set the GITHUB_USERNAME variable."
    exit 1
  fi

  # Check if repository name is provided
  if [ -z "$REPO_NAME" ]; then
    echo "Error: Repository name not provided. Please set the REPO_NAME variable."
    exit 1
  fi

  # Create the repository
  echo "Creating GitHub repository '$REPO_NAME'..."
  create_repo
  echo "Repository '$REPO_NAME' created successfully!"
}

# Run the script
main
