# Database Cleanup Instructions

## Problem
You have **old sources** in the database that were uploaded before the metadata extraction fix. These show URLs instead of proper titles.

## Current State (from test_metadata.py)
```
✅ 1 GOOD video: "AI Engineering Basics" (with channel & duration)
❌ 3 BAD videos: URLs as names (need deletion)
❌ 1 BAD web page: URL as name (need deletion)
```

## Solution

### Step 1: Run Cleanup Script
```bash
python clear_old_videos.py
```

This will:
1. Show all sources
2. Identify old sources with URLs as names
3. Ask for confirmation
4. Delete them

### Step 2: Re-upload Content
After cleanup, re-upload the videos and web pages. The new code will:
- ✅ Extract video titles, channels, and durations
- ✅ Extract web page titles
- ✅ Display properly in the UI

### Step 3: Verify
```bash
python test_metadata.py
```

Should show all sources with proper metadata.

## What Was Fixed

### Videos Now Show:
```
✅ AI Engineering Basics
   📺 Telusko Alien • ⏱️ 11:02
```

Instead of:
```
❌ https://www.youtube.com/watch?v=...
   🎬 Duration: Video
```

### Web Pages Now Show:
```
✅ GitHub - microsoft/vscode
```

Instead of:
```
❌ https://github.com/microsoft/vscode
```

## About the 503 Error

The error you saw:
```
503 Service Unavailable: The model is overloaded
```

This is **NOT a bug** in our code. It's Google's Gemini API being temporarily overloaded. The fix I added will now show a user-friendly message:

```
⚠️ The AI model is currently overloaded. Please try again in a few moments.
```

Just wait 30-60 seconds and try again.

## Summary

1. ✅ **Code is fixed** - New uploads work perfectly
2. ❌ **Old data needs cleanup** - Run `clear_old_videos.py`
3. ✅ **Re-upload after cleanup** - Will have proper metadata
4. ⚠️ **503 errors are temporary** - Just retry after a moment
