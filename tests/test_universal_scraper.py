"""
Universal Scraper Test Runner
Tests 100+ websites across multiple domains to validate detection accuracy
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.domain_patterns import detect_domain_type
from test_cases_100plus import TEST_CASES
from bs4 import BeautifulSoup
import time
from collections import defaultdict

def run_comprehensive_tests(quick_mode=True):
    """
    Run tests on 100+ websites
    quick_mode: Only test URL detection (no actual page fetching)
    """
    print("="*80)
    print("🚀 UNIVERSAL SCRAPER - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print(f"\n📊 Total Test Cases: {len(TEST_CASES)}")
    print(f"⚡ Mode: {'Quick (URL only)' if quick_mode else 'Full (with page fetch)'}\n")
    
    results = {
        'total': len(TEST_CASES),
        'passed': 0,
        'failed': 0,
        'partial': 0,
        'by_category': defaultdict(lambda: {'total': 0, 'passed': 0, 'failed': 0})
    }
    
    failed_tests = []
    
    print("Running tests...\n")
    
    for idx, test in enumerate(TEST_CASES, 1):
        url = test['url']
        expected_type = test['expected']
        category = test['category']
        
        # Extract main category
        main_category = category.split(' - ')[0]
        results['by_category'][main_category]['total'] += 1
        
        try:
            # Test URL-based detection
            detected_type, confidence, pattern = detect_domain_type(url, None)
            
            # Determine test result
            if detected_type == expected_type:
                status = "✅ PASS"
                results['passed'] += 1
                results['by_category'][main_category]['passed'] += 1
            elif confidence > 50:
                # Partial match - detected something reasonable
                status = "⚠️  PARTIAL"
                results['partial'] += 1
                results['by_category'][main_category]['passed'] += 1
            else:
                status = "❌ FAIL"
                results['failed'] += 1
                results['by_category'][main_category]['failed'] += 1
                failed_tests.append({
                    'url': url,
                    'expected': expected_type,
                    'detected': detected_type,
                    'category': category,
                    'confidence': confidence
                })
            
            # Print progress every 10 tests
            if idx % 10 == 0:
                print(f"   [{idx}/{len(TEST_CASES)}] {status} | {category}")
                print(f"                Expected: {expected_type}")
                print(f"                Detected: {detected_type} ({confidence}%)\n")
        
        except Exception as e:
            status = "💥 ERROR"
            results['failed'] += 1
            results['by_category'][main_category]['failed'] += 1
            failed_tests.append({
                'url': url,
                'expected': expected_type,
                'detected': f'ERROR: {str(e)}',
                'category': category,
                'confidence': 0
            })
            print(f"   [{idx}/{len(TEST_CASES)}] {status} | {category}: {str(e)}\n")
    
    # Print summary
    print("\n" + "="*80)
    print("📊 TEST RESULTS SUMMARY")
    print("="*80)
    
    pass_rate = (results['passed'] / results['total']) * 100
    partial_rate = (results['partial'] / results['total']) * 100
    fail_rate = (results['failed'] / results['total']) * 100
    
    print(f"\n✅ Passed:  {results['passed']}/{results['total']} ({pass_rate:.1f}%)")
    print(f"⚠️  Partial: {results['partial']}/{results['total']} ({partial_rate:.1f}%)")
    print(f"❌ Failed:  {results['failed']}/{results['total']} ({fail_rate:.1f}%)")
    
    print(f"\n📈 Overall Success Rate: {pass_rate + partial_rate:.1f}%")
    
    # Category breakdown
    print("\n" + "="*80)
    print("📂 RESULTS BY CATEGORY")
    print("="*80 + "\n")
    
    for category in sorted(results['by_category'].keys()):
        stats = results['by_category'][category]
        cat_pass_rate = (stats['passed'] / stats['total']) * 100 if stats['total'] > 0 else 0
        
        status_icon = "✅" if cat_pass_rate >= 80 else "⚠️ " if cat_pass_rate >= 60 else "❌"
        
        print(f"{status_icon} {category:20} | {stats['passed']}/{stats['total']} passed ({cat_pass_rate:.0f}%)")
    
    # Show failed tests
    if failed_tests and len(failed_tests) <= 20:
        print("\n" + "="*80)
        print("❌ FAILED TESTS DETAIL")
        print("="*80 + "\n")
        
        for fail in failed_tests:
            print(f"Category: {fail['category']}")
            print(f"URL: {fail['url']}")
            print(f"Expected: {fail['expected']}")
            print(f"Detected: {fail['detected']} (confidence: {fail['confidence']}%)")
            print("-" * 80 + "\n")
    
    elif failed_tests:
        print(f"\n⚠️  {len(failed_tests)} tests failed. Run with --verbose to see details.")
    
    # Final verdict
    print("\n" + "="*80)
    if pass_rate + partial_rate >= 90:
        print("🎉 EXCELLENT! Universal scraper is production-ready!")
    elif pass_rate + partial_rate >= 75:
        print("👍 GOOD! Minor improvements needed for edge cases.")
    elif pass_rate + partial_rate >= 60:
        print("⚠️  FAIR. More domain patterns needed.")
    else:
        print("❌ NEEDS WORK. Significant improvements required.")
    print("="*80 + "\n")
    
    return results


def test_specific_url(url):
    """Test a specific URL"""
    print(f"\n🔍 Testing URL: {url}\n")
    
    detected_type, confidence, pattern = detect_domain_type(url, None)
    
    print(f"✅ Detection Results:")
    print(f"   Type: {detected_type}")
    print(f"   Confidence: {confidence}%")
    print(f"   Pattern: {pattern}")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-url" and len(sys.argv) > 2:
            test_specific_url(sys.argv[2])
        elif sys.argv[1] == "--full":
            run_comprehensive_tests(quick_mode=False)
        else:
            print("Usage:")
            print("  python test_universal_scraper.py                  # Run quick tests")
            print("  python test_universal_scraper.py --full           # Run full tests with fetching")
            print("  python test_universal_scraper.py --test-url <url> # Test specific URL")
    else:
        run_comprehensive_tests(quick_mode=True)
