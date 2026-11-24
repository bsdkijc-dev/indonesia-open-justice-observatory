#!/usr/bin/env bash
set -euo pipefail

# Stage 6 Private Staging Deployment Script (Dell Precision Workstation)
# Prerequisites:
#   1. Explicit human approval obtained for staging.
#   2. SSH key configured for git@github.com:bsdkijc-dev/indonesia-open-justice-observatory.git
#   3. Kaggle API credentials configured for ~/.kaggle-venv/bin/kaggle (handle: judicialcollege)

echo "[1/3] Running Stage 5 Independent QA Gate..."
python3 stage5_independent_qa.py

echo "[2/3] Staging to GitHub feature branch (bsdkijc-dev/indonesia-open-justice-observatory)..."
echo "Review git status and run:"
echo "  git checkout -b feat/landmark-decisions-pilot-v1"
echo "  git add stage1_* stage2_* stage3_* stage4_* stage5_* stage7_* stage8_9_* data_dictionary.csv dataset-metadata.json README_STAGE6_STAGING.md"
echo "  git commit -m 'feat: add Stage 1-9 Landmark Decisions pilot and privacy gate'"
echo "  git push -u origin feat/landmark-decisions-pilot-v1"

echo "[3/3] Staging to Kaggle as PRIVATE dataset (judicialcollege/ma-ri-landmark-decisions-pilot)..."
echo "Run when ready:"
echo "  ~/.kaggle-venv/bin/kaggle datasets create -p . --dir-mode zip"
