"""
Test script to verify metadata extraction and display
"""
import requests
import json
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BACKEND_URL = "http://localhost:8000"

def test_sources():
    """Test sources endpoint"""
    print("=" * 80)
    print("🔍 TESTING SOURCES ENDPOINT")
    print("=" * 80)
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/sources")
        if response.status_code == 200:
            data = response.json()
            sources = data.get("sources", [])
            
            print(f"\n✅ Found {len(sources)} sources\n")
            
            # Group by type
            videos = [s for s in sources if s.get("source_type") == "video"]
            web_pages = [s for s in sources if s.get("source_type") == "web_page"]
            documents = [s for s in sources if s.get("source_type") == "document"]
            
            # Test Videos
            print("📹 VIDEOS:")
            print("-" * 80)
            if videos:
                for video in videos:
                    source_name = video.get("source_name", "Unknown")
                    metadata = video.get("metadata", {})
                    channel = metadata.get("channel", "Unknown")
                    duration = metadata.get("duration", "Unknown")
                    
                    # Check if source_name is URL (BAD) or title (GOOD)
                    is_url = source_name.startswith("http")
                    status = "❌ BAD" if is_url else "✅ GOOD"
                    
                    print(f"\n{status} Video:")
                    print(f"  Name: {source_name}")
                    print(f"  Channel: {channel}")
                    print(f"  Duration: {duration}")
                    
                    if is_url:
                        print(f"  ⚠️ ISSUE: Source name is URL instead of title!")
            else:
                print("  No videos found")
            
            # Test Web Pages
            print("\n\n🌐 WEB PAGES:")
            print("-" * 80)
            if web_pages:
                for page in web_pages:
                    source_name = page.get("source_name", "Unknown")
                    
                    # Check if source_name is URL (BAD) or title (GOOD)
                    is_url = source_name.startswith("http")
                    status = "❌ BAD" if is_url else "✅ GOOD"
                    
                    print(f"\n{status} Web Page:")
                    print(f"  Name: {source_name}")
                    
                    if is_url:
                        print(f"  ⚠️ ISSUE: Source name is URL instead of title!")
            else:
                print("  No web pages found")
            
            # Test Documents
            print("\n\n📄 DOCUMENTS:")
            print("-" * 80)
            if documents:
                for doc in documents:
                    source_name = doc.get("source_name", "Unknown")
                    print(f"\n✅ Document:")
                    print(f"  Name: {source_name}")
            else:
                print("  No documents found")
            
            # Summary
            print("\n" + "=" * 80)
            print("📊 SUMMARY")
            print("=" * 80)
            
            bad_videos = [v for v in videos if v.get("source_name", "").startswith("http")]
            bad_web = [w for w in web_pages if w.get("source_name", "").startswith("http")]
            
            if bad_videos:
                print(f"❌ {len(bad_videos)} video(s) with URL as name - NEED TO DELETE & RE-UPLOAD")
            else:
                print(f"✅ All {len(videos)} video(s) have proper titles")
            
            if bad_web:
                print(f"❌ {len(bad_web)} web page(s) with URL as name - NEED TO DELETE & RE-UPLOAD")
            else:
                print(f"✅ All {len(web_pages)} web page(s) have proper titles")
            
            print(f"✅ {len(documents)} document(s)")
            
        else:
            print(f"❌ Failed to get sources: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ Error: {e}")

def test_video_upload():
    """Test video upload"""
    print("\n\n" + "=" * 80)
    print("🎥 TESTING VIDEO UPLOAD")
    print("=" * 80)
    
    test_url = "https://www.youtube.com/watch?v=VtjVyM08SZA"
    
    print(f"\nTesting with: {test_url}")
    print("Expected:")
    print("  Title: AI Engineering Basics")
    print("  Channel: Telusko Alien")
    print("  Duration: XX:XX (actual duration)")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/upload/video",
            json={"video_url": test_url}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if already exists
            if data.get("message") and "already exists" in data.get("message", ""):
                print(f"\n⚠️ Video already exists in database")
                print(f"   Message: {data.get('message')}")
                print(f"\n💡 To test properly, delete the old video first using clear_old_videos.py")
            else:
                print(f"\n✅ Upload successful!")
                print(f"   Title: {data.get('title', 'N/A')}")
                print(f"   Channel: {data.get('channel', 'N/A')}")
                print(f"   Duration: {data.get('duration', 'N/A')}")
        else:
            print(f"\n❌ Upload failed: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_sources()
    # Uncomment to test upload
    # test_video_upload()
