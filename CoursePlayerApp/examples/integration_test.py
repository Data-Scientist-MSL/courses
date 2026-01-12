#!/usr/bin/env python3
"""
Integration Test Example - CoursePlayerApp

This example shows how to write integration tests for CoursePlayerApp
that test the complete flow from license activation to feature usage.

Run: python integration_test.py
Or: pytest integration_test.py -v
"""

import sys
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Mock External Services
# ============================================================================

class TierLevel(Enum):
    """User tier levels"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ENTERPRISE = "enterprise"


@dataclass
class LicenseInfo:
    """License information"""
    key: str
    tier: TierLevel
    valid: bool
    expires_at: str
    user_id: str


class MockCoursesGTMAPI:
    """Mock CoursesGTM API for testing"""
    
    def __init__(self):
        self.licenses = {
            "BASIC-TEST-KEY": LicenseInfo(
                key="BASIC-TEST-KEY",
                tier=TierLevel.BASIC,
                valid=True,
                expires_at="2026-12-31",
                user_id="user-basic"
            ),
            "INT-TEST-KEY": LicenseInfo(
                key="INT-TEST-KEY",
                tier=TierLevel.INTERMEDIATE,
                valid=True,
                expires_at="2026-12-31",
                user_id="user-intermediate"
            ),
            "ADV-TEST-KEY": LicenseInfo(
                key="ADV-TEST-KEY",
                tier=TierLevel.ADVANCED,
                valid=True,
                expires_at="2026-12-31",
                user_id="user-advanced"
            ),
            "EXPIRED-KEY": LicenseInfo(
                key="EXPIRED-KEY",
                tier=TierLevel.BASIC,
                valid=False,
                expires_at="2025-12-31",
                user_id="user-expired"
            )
        }
        self.feature_usage = {}
    
    def validate_license(self, license_key: str) -> Dict[str, Any]:
        """Validate a license key"""
        if license_key not in self.licenses:
            return {"valid": False, "error": "Invalid license key"}
        
        license_info = self.licenses[license_key]
        return {
            "valid": license_info.valid,
            "tier": license_info.tier.value,
            "expires_at": license_info.expires_at,
            "user_id": license_info.user_id
        }
    
    def can_use_feature(self, user_id: str, feature: str) -> bool:
        """Check if user can use a feature"""
        # Find user's tier
        tier = None
        for license_info in self.licenses.values():
            if license_info.user_id == user_id:
                tier = license_info.tier
                break
        
        if not tier:
            return False
        
        # Feature availability by tier
        features_by_tier = {
            TierLevel.BASIC: ['video_streaming', 'slide_view'],
            TierLevel.INTERMEDIATE: ['video_streaming', 'slide_view', 'video_download', 'ai_tutor'],
            TierLevel.ADVANCED: ['video_streaming', 'slide_view', 'video_download', 'ai_tutor', 'notebook_gpu']
        }
        
        return feature in features_by_tier.get(tier, [])
    
    def get_feature_usage(self, user_id: str, feature: str) -> int:
        """Get feature usage count"""
        key = f"{user_id}:{feature}"
        return self.feature_usage.get(key, 0)
    
    def increment_feature_usage(self, user_id: str, feature: str):
        """Increment feature usage"""
        key = f"{user_id}:{feature}"
        self.feature_usage[key] = self.feature_usage.get(key, 0) + 1


# ============================================================================
# Integration Test Cases
# ============================================================================

class IntegrationTestRunner:
    """Run integration tests"""
    
    def __init__(self):
        self.api = MockCoursesGTMAPI()
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def assert_equal(self, actual, expected, test_name: str):
        """Assert two values are equal"""
        if actual == expected:
            self.passed += 1
            self.results.append(f"✅ PASS: {test_name}")
            return True
        else:
            self.failed += 1
            self.results.append(f"❌ FAIL: {test_name}")
            self.results.append(f"   Expected: {expected}")
            self.results.append(f"   Actual: {actual}")
            return False
    
    def assert_true(self, condition, test_name: str):
        """Assert condition is true"""
        return self.assert_equal(condition, True, test_name)
    
    def assert_false(self, condition, test_name: str):
        """Assert condition is false"""
        return self.assert_equal(condition, False, test_name)
    
    # ========================================================================
    # Test Cases
    # ========================================================================
    
    def test_license_validation_valid(self):
        """Test valid license validation"""
        result = self.api.validate_license("BASIC-TEST-KEY")
        
        self.assert_true(result['valid'], "Valid license should be accepted")
        self.assert_equal(result['tier'], "basic", "Tier should be basic")
        self.assert_equal(result['user_id'], "user-basic", "User ID should match")
    
    def test_license_validation_invalid(self):
        """Test invalid license validation"""
        result = self.api.validate_license("INVALID-KEY")
        
        self.assert_false(result['valid'], "Invalid license should be rejected")
        self.assert_true('error' in result, "Error message should be present")
    
    def test_license_validation_expired(self):
        """Test expired license validation"""
        result = self.api.validate_license("EXPIRED-KEY")
        
        self.assert_false(result['valid'], "Expired license should be invalid")
    
    def test_basic_tier_feature_access(self):
        """Test feature access for Basic tier"""
        user_id = "user-basic"
        
        # Should have access to basic features
        self.assert_true(
            self.api.can_use_feature(user_id, "video_streaming"),
            "Basic tier should have video streaming"
        )
        
        # Should NOT have access to advanced features
        self.assert_false(
            self.api.can_use_feature(user_id, "video_download"),
            "Basic tier should not have video download"
        )
        self.assert_false(
            self.api.can_use_feature(user_id, "ai_tutor"),
            "Basic tier should not have AI tutor"
        )
    
    def test_intermediate_tier_feature_access(self):
        """Test feature access for Intermediate tier"""
        user_id = "user-intermediate"
        
        # Should have basic features
        self.assert_true(
            self.api.can_use_feature(user_id, "video_streaming"),
            "Intermediate tier should have video streaming"
        )
        
        # Should have intermediate features
        self.assert_true(
            self.api.can_use_feature(user_id, "video_download"),
            "Intermediate tier should have video download"
        )
        self.assert_true(
            self.api.can_use_feature(user_id, "ai_tutor"),
            "Intermediate tier should have AI tutor"
        )
        
        # Should NOT have advanced features
        self.assert_false(
            self.api.can_use_feature(user_id, "notebook_gpu"),
            "Intermediate tier should not have GPU notebooks"
        )
    
    def test_advanced_tier_feature_access(self):
        """Test feature access for Advanced tier"""
        user_id = "user-advanced"
        
        # Should have all features
        self.assert_true(
            self.api.can_use_feature(user_id, "video_streaming"),
            "Advanced tier should have video streaming"
        )
        self.assert_true(
            self.api.can_use_feature(user_id, "video_download"),
            "Advanced tier should have video download"
        )
        self.assert_true(
            self.api.can_use_feature(user_id, "ai_tutor"),
            "Advanced tier should have AI tutor"
        )
        self.assert_true(
            self.api.can_use_feature(user_id, "notebook_gpu"),
            "Advanced tier should have GPU notebooks"
        )
    
    def test_ai_tutor_quota_tracking(self):
        """Test AI tutor quota is tracked correctly"""
        user_id = "user-intermediate"
        feature = "ai_tutor"
        
        # Initial usage should be 0
        usage = self.api.get_feature_usage(user_id, feature)
        self.assert_equal(usage, 0, "Initial usage should be 0")
        
        # Increment usage 3 times
        for _ in range(3):
            self.api.increment_feature_usage(user_id, feature)
        
        # Usage should now be 3
        usage = self.api.get_feature_usage(user_id, feature)
        self.assert_equal(usage, 3, "Usage should be 3 after 3 increments")
    
    def test_complete_user_flow(self):
        """Test complete user flow from license to feature usage"""
        license_key = "INT-TEST-KEY"
        
        # Step 1: Validate license
        license_result = self.api.validate_license(license_key)
        self.assert_true(license_result['valid'], "License should be valid")
        
        user_id = license_result['user_id']
        
        # Step 2: Check course access
        can_stream = self.api.can_use_feature(user_id, "video_streaming")
        self.assert_true(can_stream, "User should be able to stream videos")
        
        # Step 3: Use AI tutor
        can_use_ai = self.api.can_use_feature(user_id, "ai_tutor")
        self.assert_true(can_use_ai, "User should be able to use AI tutor")
        
        # Step 4: Track usage
        initial_usage = self.api.get_feature_usage(user_id, "ai_tutor")
        self.api.increment_feature_usage(user_id, "ai_tutor")
        new_usage = self.api.get_feature_usage(user_id, "ai_tutor")
        self.assert_equal(new_usage, initial_usage + 1, "Usage should be incremented by 1")
        
        # Step 5: Check quota limit (mock: intermediate has 50 limit)
        remaining = 50 - new_usage
        self.assert_true(remaining > 0, "Should have questions remaining")
    
    def test_upgrade_flow(self):
        """Test tier upgrade flow"""
        # Start with basic tier
        basic_user = "user-basic"
        
        # Cannot use intermediate features
        can_download = self.api.can_use_feature(basic_user, "video_download")
        self.assert_false(can_download, "Basic tier cannot download videos")
        
        # Simulate upgrade to intermediate
        # In real system, this would be a separate API call
        # For this test, we just verify the license change would work
        
        int_license = self.api.validate_license("INT-TEST-KEY")
        int_user = int_license['user_id']
        
        # After upgrade, can use intermediate features
        can_download = self.api.can_use_feature(int_user, "video_download")
        self.assert_true(can_download, "Intermediate tier can download videos")
    
    # ========================================================================
    # Test Runner
    # ========================================================================
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 70)
        print("🧪 CoursePlayerApp Integration Tests")
        print("=" * 70)
        print()
        
        tests = [
            self.test_license_validation_valid,
            self.test_license_validation_invalid,
            self.test_license_validation_expired,
            self.test_basic_tier_feature_access,
            self.test_intermediate_tier_feature_access,
            self.test_advanced_tier_feature_access,
            self.test_ai_tutor_quota_tracking,
            self.test_complete_user_flow,
            self.test_upgrade_flow
        ]
        
        for test in tests:
            print(f"Running: {test.__name__}")
            test()
            print()
        
        # Print results
        print("=" * 70)
        print("📊 Test Results")
        print("=" * 70)
        print()
        
        for result in self.results:
            print(result)
        
        print()
        print(f"Total: {self.passed + self.failed} tests")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print()
        
        if self.failed == 0:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"⚠️  {self.failed} test(s) failed")
            return 1


# ============================================================================
# Main
# ============================================================================

def main():
    """Run integration tests"""
    runner = IntegrationTestRunner()
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
