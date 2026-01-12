"""
CoursesGTM Integration Example

This example demonstrates how to integrate with the CoursesGTM API.

Shows:
- License validation
- Feature checking
- Course content retrieval
- Progress tracking
- AI tutor quota management

Run with: python examples/integration_example.py
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class CoursesGTMClient:
    """Example CoursesGTM API client"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def validate_license(self, license_key: str) -> Dict:
        """Validate license and get tier information"""
        response = self.session.post(
            f"{self.base_url}/api/v1/license/validate",
            json={"license_key": license_key}
        )
        response.raise_for_status()
        return response.json()
    
    def get_enabled_features(self, license_key: str) -> List[str]:
        """Get list of enabled features for license"""
        validation = self.validate_license(license_key)
        return validation.get("enabled_features", [])
    
    def get_course(self, course_id: str) -> Dict:
        """Get course content and structure"""
        response = self.session.get(f"{self.base_url}/api/v1/courses/{course_id}")
        response.raise_for_status()
        return response.json()
    
    def update_progress(self, course_id: str, lesson_id: str) -> Dict:
        """Mark lesson as completed"""
        response = self.session.post(
            f"{self.base_url}/api/v1/progress/{course_id}/update",
            json={
                "lesson_id": lesson_id,
                "completed": True,
                "timestamp": datetime.now().isoformat()
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_ai_tutor_quota(self) -> Dict:
        """Get remaining AI tutor quota"""
        response = self.session.get(f"{self.base_url}/api/v1/ai-tutor/quota")
        response.raise_for_status()
        return response.json()
    
    def check_feature_access(self, feature_name: str, tier: str) -> bool:
        """Check if feature is available for tier"""
        # Load feature flags
        with open('../config/feature_flags.json', 'r') as f:
            feature_flags = json.load(f)
        
        feature = feature_flags['features'].get(feature_name, {})
        enabled_tiers = feature.get('enabled_tiers', [])
        
        return tier in enabled_tiers


def demo_license_validation():
    """Demo: Validate license and get tier"""
    print("\n=== License Validation Demo ===")
    
    client = CoursesGTMClient(
        base_url="http://localhost:8000",
        api_key="demo_api_key"
    )
    
    # Validate license
    try:
        result = client.validate_license("DEMO-LICENSE-KEY")
        
        print(f"✅ License Valid: {result['valid']}")
        print(f"   Tier: {result['tier']}")
        print(f"   User: {result['user_email']}")
        print(f"   Expires: {result['expires_at']}")
        print(f"   Features: {len(result['enabled_features'])} enabled")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ License validation failed: {e}")


def demo_feature_gating():
    """Demo: Check feature access based on tier"""
    print("\n=== Feature Gating Demo ===")
    
    client = CoursesGTMClient(
        base_url="http://localhost:8000",
        api_key="demo_api_key"
    )
    
    tiers = ['basic', 'intermediate', 'advanced']
    features = ['video_download', 'ai_tutor', 'offline_mode']
    
    for tier in tiers:
        print(f"\n{tier.upper()} Tier:")
        for feature in features:
            has_access = client.check_feature_access(feature, tier)
            status = "✅" if has_access else "❌"
            print(f"  {status} {feature}")


def demo_course_access():
    """Demo: Retrieve course content"""
    print("\n=== Course Content Retrieval Demo ===")
    
    client = CoursesGTMClient(
        base_url="http://localhost:8000",
        api_key="demo_api_key"
    )
    
    try:
        course = client.get_course("ml-fundamentals")
        
        print(f"📚 Course: {course['title']}")
        print(f"   Modules: {len(course['modules'])}")
        print(f"   Total Lessons: {sum(len(m['lessons']) for m in course['modules'])}")
        print(f"   Required Tier: {course['tier_requirement']}")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to retrieve course: {e}")


def demo_progress_tracking():
    """Demo: Track lesson completion"""
    print("\n=== Progress Tracking Demo ===")
    
    client = CoursesGTMClient(
        base_url="http://localhost:8000",
        api_key="demo_api_key"
    )
    
    try:
        result = client.update_progress(
            course_id="ml-fundamentals",
            lesson_id="lesson-001"
        )
        
        print(f"✅ Progress updated:")
        print(f"   XP Earned: {result.get('xp_earned', 0)}")
        print(f"   New Total XP: {result.get('total_xp', 0)}")
        print(f"   Level: {result.get('level', 1)}")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to update progress: {e}")


def demo_ai_quota():
    """Demo: Check AI tutor quota"""
    print("\n=== AI Tutor Quota Demo ===")
    
    client = CoursesGTMClient(
        base_url="http://localhost:8000",
        api_key="demo_api_key"
    )
    
    try:
        quota = client.get_ai_tutor_quota()
        
        if quota['remaining'] == 'unlimited':
            print("✨ Unlimited AI Tutor access (Advanced tier)")
        else:
            remaining = quota['remaining']
            total = quota['total']
            print(f"📊 AI Tutor Quota:")
            print(f"   Remaining: {remaining}/{total}")
            print(f"   Resets: {quota['reset_date']}")
            
            if remaining < 10:
                print("   ⚠️ Low quota - consider upgrading!")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to check quota: {e}")


def demo_upgrade_flow():
    """Demo: Simulate upgrade flow"""
    print("\n=== Upgrade Flow Demo ===")
    
    print("Current Tier: Basic")
    print("Target Tier: Intermediate")
    print("\nNew Features:")
    print("  ✅ AI Tutor (50 questions/month)")
    print("  ✅ Video Downloads (720p)")
    print("  ✅ Interactive Labs")
    print("  ✅ Certificates")
    print("\nPrice: $29/month")
    print("\n[Redirect to LemonSqueezy checkout...]")


if __name__ == "__main__":
    print("CoursePlayerApp - CoursesGTM Integration Examples")
    print("=" * 50)
    
    # Note: These demos use mock data since we don't have a live API
    print("\n⚠️  Note: Using mock data for demonstration")
    print("    In production, replace with actual API endpoint\n")
    
    # Run demos
    demo_license_validation()
    demo_feature_gating()
    demo_course_access()
    demo_progress_tracking()
    demo_ai_quota()
    demo_upgrade_flow()
    
    print("\n" + "=" * 50)
    print("✅ Integration examples completed!")
    print("\nNext steps:")
    print("1. Set up CoursesGTM API endpoint")
    print("2. Configure API keys in .env file")
    print("3. Test with real license keys")
    print("4. Implement error handling")
    print("5. Add retry logic for production")
