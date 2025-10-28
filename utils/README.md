# Utility Scripts

This folder contains utility scripts for maintenance, testing, and cleanup tasks.

---

## Scripts

### 1. `clear_old_videos.py`
**Purpose:** Clean up old sources with URLs as names (from before metadata extraction fix)

**Usage:**
```bash
cd StudyAgent
python utils/clear_old_videos.py
```

**What it does:**
- Fetches all sources from backend
- Identifies sources with URLs as `source_name`
- Shows list of old sources
- Asks for confirmation
- Deletes old sources

**When to use:**
- After upgrading to version with metadata extraction
- When cleaning up test data
- When sources show URLs instead of titles

---

### 2. `test_metadata.py`
**Purpose:** Test and verify metadata extraction for videos and web pages

**Usage:**
```bash
cd StudyAgent
python utils/test_metadata.py
```

**What it does:**
- Tests sources endpoint
- Checks if videos have proper titles, channels, and durations
- Checks if web pages have proper titles
- Identifies sources with issues
- Provides summary report

**When to use:**
- After uploading new content
- To verify metadata extraction is working
- To identify problematic sources
- During development/testing

---

### 3. `CLEANUP_INSTRUCTIONS.md`
**Purpose:** Detailed instructions for database cleanup

**Contents:**
- Problem explanation
- Current state analysis
- Step-by-step cleanup procedure
- Verification steps
- Troubleshooting tips

**When to use:**
- When encountering metadata issues
- Before major upgrades
- During maintenance

---

## Requirements

All scripts require:
- Backend running at `http://localhost:8000`
- Python 3.11+
- `requests` library

Install dependencies:
```bash
pip install requests
```

---

## Common Tasks

### Clean up old data
```bash
python utils/clear_old_videos.py
# Type 'yes' when prompted
```

### Verify metadata
```bash
python utils/test_metadata.py
```

### Check specific source
```bash
# Use backend API directly
curl http://localhost:8000/api/v1/sources
```

---

## Notes

- Always backup data before cleanup
- Test scripts connect to localhost:8000
- Scripts are safe to run (ask for confirmation)
- Check logs if scripts fail

---

## Troubleshooting

**Script can't connect:**
```bash
# Check backend is running
curl http://localhost:8000/health
```

**Encoding errors on Windows:**
- Scripts handle UTF-8 encoding automatically
- If issues persist, check console encoding

**Permission errors:**
- Ensure backend is accessible
- Check firewall settings

---

**Last Updated:** October 2025
