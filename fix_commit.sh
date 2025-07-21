#!/bin/bash

# This script will fix the commit message for the commit with typo
export GIT_SEQUENCE_EDITOR="sed -i 's/^pick 5ee1dd8/reword 5ee1dd8/'"
git rebase -i HEAD~4

# The rebase will stop at the commit, then we need to fix the message
echo "Now fixing the commit message..."
export GIT_EDITOR="sed -i 's/Refaactored/Refactored/'"
git commit --amend --no-edit
