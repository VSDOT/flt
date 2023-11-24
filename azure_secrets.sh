#!/bin/bash

REPO_NAME="$3"
REPO_OWNER="$1"
PAT="$2"

USER_SEC1="$4"
USER_SEC2="$5"
USER_SEC3="$6"
USER_SEC4="$7"


#KEY_ID="$(curl -L \
#  -H "Accept: application/vnd.github+json" \
#  -H "Authorization: Bearer ${PAT}" \
#  -H "X-GitHub-Api-Version: 2022-11-28" \
#  https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/secrets/public-key | grep "key_id" | sed -i 's/[key_id:," ]//g')"

KEY_NAME="$(curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${PAT}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/secrets/public-key | grep "key_id" | sed 's/[key_id:," ]//g')"

#sed -i 's/[key_id:," ]//g' san.txt && export KEY_ID="$(cat san.txt)"

#export SECRET="$(echo "${SECRET_VALUE}" | base64)"

# Define an associative array of secrets
declare -A secrets=(
  ["KEY_SUBSCRIPTION"]="$USER_SEC1"
  ["KEY_TENENT"]="$USER_SEC2"
  ["KEY_CLIENT"]="$USER_SEC3"
  ["KEY_CLIENT_SEC"]="$USER_SEC4"
 # ["SECRET_3"]="secret_value_3"
  # Add more secrets here as needed
)

for secret_name in "${!secrets[@]}"; do
  secret_value="${secrets[$secret_name]}"
  curl -L \
    -X PUT \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${PAT}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/secrets/${secret_name} \
    -d '{"encrypted_value":"'$(echo -n $secret_value | base64)'","key_id":"'$KEY_NAME'"}'
done

