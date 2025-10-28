"""
Script to clear old video entries with URL as source_name
Run this to clean up the database before testing
"""
import requests
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BACKEND_URL = "http://localhost:8000"

def get_all_sources():
    """Get all sources from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/sources")
        if response.status_code == 200:
            return response.json().get("sources", [])
        else:
            print(f"❌ Failed to get sources: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def delete_source(source_id, source_name):
    """Delete a source"""
    try:
        response = requests.delete(f"{BACKEND_URL}/api/v1/sources/{source_id}")
        if response.status_code == 200:
            print(f"✅ Deleted: {source_name}")
            return True
        else:
            print(f"❌ Failed to delete {source_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting {source_name}: {e}")
        return False

def main():
    print("🔍 Fetching all sources...")
    sources = get_all_sources()
    
    if not sources:
        print("ℹ️ No sources found")
        return
    
    print(f"\n📊 Found {len(sources)} sources\n")
    
    # Find sources with URLs as source_name (videos and web pages)
    old_sources = []
    for source in sources:
        source_type = source.get("source_type", "")
        source_name = source.get("source_name", "")
        
        # Check if source_name is a URL (starts with http)
        if source_name.startswith("http"):
            old_sources.append(source)
            if source_type == "video":
                print(f"🎥 Old Video: {source_name[:60]}...")
            elif source_type == "web_page":
                print(f"🌐 Old Web Page: {source_name[:60]}...")
            else:
                print(f"📄 Old Source: {source_name[:60]}...")
        else:
            if source_type == "video":
                print(f"✅ Good Video: {source_name}")
                channel = source.get("metadata", {}).get("channel", "Unknown")
                duration = source.get("metadata", {}).get("duration", "Unknown")
                print(f"   📺 {channel} • ⏱️ {duration}")
            elif source_type == "web_page":
                print(f"✅ Good Web Page: {source_name}")
            else:
                print(f"✅ Good Source: {source_name}")
    
    if not old_sources:
        print("\n✅ No old sources found! All sources have proper metadata.")
        return
    
    print(f"\n⚠️ Found {len(old_sources)} old source(s) with URL as name")
    
    # Ask for confirmation
    response = input("\n❓ Delete these old sources? (yes/no): ").strip().lower()
    
    if response == "yes":
        print("\n🗑️ Deleting old sources...")
        for source in old_sources:
            delete_source(source["source_id"], source["source_name"])
        print("\n✅ Cleanup complete!")
    else:
        print("\n❌ Cancelled")

if __name__ == "__main__":
    main()
