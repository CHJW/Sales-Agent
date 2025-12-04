#!/usr/bin/env python3
"""
Test script for vector debug aggregation functionality
"""

import sys
import os

# Add scripts directory to path
sys.path.append('scripts')

try:
    from aggregate_vector_debug import aggregate_vector_debug_info, generate_vector_performance_report
    
    print("🧪 Testing vector debug aggregation...")
    
    # Test aggregation with simulated debug files
    aggregated = aggregate_vector_debug_info(".")
    
    if aggregated:
        print("✅ Successfully aggregated vector debug data")
        print(f"📊 Summary: {aggregated['summary']}")
        
        # Generate test report
        generate_vector_performance_report(aggregated, "test_vector_performance_report.md")
        print("✅ Generated test performance report")
        
        # Display key metrics
        print("\n📈 Key Performance Metrics:")
        print(f"   Total Queries: {aggregated['summary']['total_queries']}")
        print(f"   Average Query Time: {aggregated['performance']['query_times']['avg']}s")
        print(f"   Fast Queries: {aggregated['efficiency']['fast_queries']}")
        print(f"   Moderate Queries: {aggregated['efficiency']['moderate_queries']}")
        print(f"   Slow Queries: {aggregated['efficiency']['slow_queries']}")
        print(f"   Throughput: {aggregated['efficiency']['avg_chunks_per_second']} chunks/sec")
        
    else:
        print("❌ No vector debug data found")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error during testing: {e}")