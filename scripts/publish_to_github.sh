#!/usr/bin/env bash
# Pulse Linux GitHub Organization Publisher
# Automates creating the main OS repository and organization profile under the new GitHub organization.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

ORG_NAME="${1:-pulse-linux}"

echo "================================================================"
echo "  Pulse Linux GitHub Organization Publishing Tool"
echo "  Target Organization: @${ORG_NAME}"
echo "================================================================"

# Verify gh CLI authentication
if ! gh auth status >/dev/null 2>&1; then
    echo "ERROR: GitHub CLI is not authenticated. Run 'gh auth login' first."
    exit 1
fi

CURRENT_USER=$(gh api user -q .login)
echo "[+] Authenticated as: @${CURRENT_USER}"

# Check if target organization exists and user is a member
echo "[+] Checking organization @${ORG_NAME}..."
if ! gh api "orgs/${ORG_NAME}" >/dev/null 2>&1; then
    echo ""
    echo "[-] Organization @${ORG_NAME} does not exist yet or you do not have access."
    echo "    Please create it first via GitHub's free plan creator:"
    echo "    https://github.com/organizations/plan"
    echo ""
    echo "    Recommended handle: ${ORG_NAME}"
    echo "    Organization Name : Pulse Linux"
    echo ""
    exit 1
fi

echo "[✓] Organization @${ORG_NAME} confirmed!"

# 1. Create main repository if not exists
echo "[+] Checking repository ${ORG_NAME}/pulse..."
if ! gh repo view "${ORG_NAME}/pulse" >/dev/null 2>&1; then
    echo "    Creating public repository ${ORG_NAME}/pulse..."
    gh repo create "${ORG_NAME}/pulse" \
        --public \
        --description "Pulse Linux — One Operating System. Two Worlds. Unlimited Possibilities. Debian-based Workstation combining Developer Productivity and Modular Security Tooling." \
        --homepage "https://pulselinux.org"
fi

# Set topics
echo "[+] Configuring repository topics..."
gh repo edit "${ORG_NAME}/pulse" \
    --add-topic "linux" \
    --add-topic "debian" \
    --add-topic "operating-system" \
    --add-topic "gnome" \
    --add-topic "cybersecurity" \
    --add-topic "developer-tools" \
    --add-topic "distro" \
    --add-topic "iso" || true

# Push git code
cd "${REPO_ROOT}"
echo "[+] Pushing code to ${ORG_NAME}/pulse..."
if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "https://github.com/${ORG_NAME}/pulse.git"
else
    git remote add origin "https://github.com/${ORG_NAME}/pulse.git"
fi

git push -u origin main

# 2. Setup organization profile repository (.github)
echo "[+] Setting up organization profile repository (${ORG_NAME}/.github)..."
if ! gh repo view "${ORG_NAME}/.github" >/dev/null 2>&1; then
    gh repo create "${ORG_NAME}/.github" \
        --public \
        --description "Pulse Linux Organization Profile and Community Health"
fi

TMP_PROFILE_DIR=$(mktemp -d)
cp -r "${REPO_ROOT}/.github" "${TMP_PROFILE_DIR}/"
cd "${TMP_PROFILE_DIR}"
git init -b main
git config user.name "kalidevelopers"
git config user.email "kalidevelopers001@gmail.com"
git add .
git commit -m "feat: initialize Pulse Linux organization profile banner and documentation"
git remote add origin "https://github.com/${ORG_NAME}/.github.git"
git push -u origin main --force
rm -rf "${TMP_PROFILE_DIR}"

echo ""
echo "================================================================"
echo "  [SUCCESS] Pulse Linux published to GitHub!"
echo "  Organization: https://github.com/${ORG_NAME}"
echo "  OS Repository: https://github.com/${ORG_NAME}/pulse"
echo "  Profile Repo : https://github.com/${ORG_NAME}/.github"
echo "================================================================"
