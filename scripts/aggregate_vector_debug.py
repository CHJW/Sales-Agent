#!/usr/bin/env python3
"""
Aggregate Vector Debug Information
Collects and summarizes vector database performance metrics from debug files
"""

import os
import json
import glob
from datetime import datetime
import statistics

def aggregate_vector_debug_info(debug_dir="."):
    """Aggregate vector debug information from JSON files"""
    
    # Find all vector debug files
    debug_files = glob.glob(os.path.join(debug_dir, "vector_query_debug_*.json"))
    
    if not debug_files:
        print("⚠️  No vector debug files found")
        return None
    
    print(f"🔍 Found {len(debug_files)} vector debug files")
    
    # Aggregate data
    all_queries = []
    total_chunks = 0
    query_times = []
    search_times = []
    model_load_times = []
    db_connect_times = []
    section_filters = {}
    
    for debug_file in debug_files:
        try:
            with open(debug_file, 'r') as f:
                debug_data = json.load(f)
                
            all_queries.append(debug_data)
            
            # Extract metrics
            results = debug_data.get('results', {})
            total_chunks += results.get('chunks_found', 0)
            query_times.append(results.get('total_time_seconds', 0))
            search_times.append(results.get('search_time', 0))
            model_load_times.append(results.get('model_load_time', 0))
            db_connect_times.append(results.get('db_connection_time', 0))
            
            # Track section filter usage
            section_filter = debug_data.get('section_filter')
            if section_filter:
                section_filters[section_filter] = section_filters.get(section_filter, 0) + 1
                
        except Exception as e:
            print(f"⚠️  Error reading {debug_file}: {e}")
    
    if not all_queries:
        return None
    
    # Calculate aggregated metrics
    aggregated = {
        'summary': {
            'total_queries': len(all_queries),
            'total_chunks_retrieved': total_chunks,
            'avg_chunks_per_query': round(total_chunks / len(all_queries), 2),
            'timeframe': {
                'first_query': min(q['timestamp'] for q in all_queries),
                'last_query': max(q['timestamp'] for q in all_queries)
            }
        },
        'performance': {
            'query_times': {
                'min': round(min(query_times), 3),
                'max': round(max(query_times), 3),
                'avg': round(statistics.mean(query_times), 3),
                'median': round(statistics.median(query_times), 3)
            },
            'search_times': {
                'min': round(min(search_times), 3),
                'max': round(max(search_times), 3), 
                'avg': round(statistics.mean(search_times), 3),
                'median': round(statistics.median(search_times), 3)
            },
            'model_load_times': {
                'min': round(min(model_load_times), 3),
                'max': round(max(model_load_times), 3),
                'avg': round(statistics.mean(model_load_times), 3),
                'median': round(statistics.median(model_load_times), 3)
            },
            'db_connect_times': {
                'min': round(min(db_connect_times), 3),
                'max': round(max(db_connect_times), 3),
                'avg': round(statistics.mean(db_connect_times), 3),
                'median': round(statistics.median(db_connect_times), 3)
            }
        },
        'efficiency': {
            'fast_queries': len([t for t in search_times if t < 0.1]),
            'moderate_queries': len([t for t in search_times if 0.1 <= t < 0.5]),
            'slow_queries': len([t for t in search_times if t >= 0.5]),
            'section_filter_usage': section_filters,
            'avg_chunks_per_second': round(total_chunks / sum(query_times), 2) if sum(query_times) > 0 else 0
        },
        'queries': all_queries  # Include full query details
    }
    
    return aggregated

def generate_vector_performance_report(aggregated_data, output_file="vector_performance_report.md"):
    """Generate a markdown report from aggregated vector debug data"""
    
    if not aggregated_data:
        print("❌ No data to generate report")
        return
    
    summary = aggregated_data['summary']
    perf = aggregated_data['performance']
    eff = aggregated_data['efficiency']
    
    report = f"""# Vector Database Performance Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Total Vector Queries:** {summary['total_queries']}
- **Total Chunks Retrieved:** {summary['total_chunks_retrieved']}
- **Average Chunks per Query:** {summary['avg_chunks_per_query']}
- **Query Performance:** {eff['fast_queries']} fast, {eff['moderate_queries']} moderate, {eff['slow_queries']} slow
- **Overall Throughput:** {eff['avg_chunks_per_second']} chunks/second

## Performance Metrics

### Query Times (Total End-to-End)
- **Fastest:** {perf['query_times']['min']}s
- **Slowest:** {perf['query_times']['max']}s  
- **Average:** {perf['query_times']['avg']}s
- **Median:** {perf['query_times']['median']}s

### Search Times (Vector Similarity Search)
- **Fastest:** {perf['search_times']['min']}s
- **Slowest:** {perf['search_times']['max']}s
- **Average:** {perf['search_times']['avg']}s
- **Median:** {perf['search_times']['median']}s

### Model Loading Times
- **Fastest:** {perf['model_load_times']['min']}s
- **Slowest:** {perf['model_load_times']['max']}s
- **Average:** {perf['model_load_times']['avg']}s
- **Median:** {perf['model_load_times']['median']}s

### Database Connection Times  
- **Fastest:** {perf['db_connect_times']['min']}s
- **Slowest:** {perf['db_connect_times']['max']}s
- **Average:** {perf['db_connect_times']['avg']}s
- **Median:** {perf['db_connect_times']['median']}s

## Query Distribution
- **Fast Queries (< 0.1s):** {eff['fast_queries']} ({round(eff['fast_queries']/summary['total_queries']*100, 1)}%)
- **Moderate Queries (0.1-0.5s):** {eff['moderate_queries']} ({round(eff['moderate_queries']/summary['total_queries']*100, 1)}%)
- **Slow Queries (> 0.5s):** {eff['slow_queries']} ({round(eff['slow_queries']/summary['total_queries']*100, 1)}%)

## Section Filter Usage
"""
    
    for section, count in eff['section_filter_usage'].items():
        percentage = round(count / summary['total_queries'] * 100, 1)
        report += f"- **{section}:** {count} queries ({percentage}%)\n"
    
    unfiltered = summary['total_queries'] - sum(eff['section_filter_usage'].values())
    if unfiltered > 0:
        percentage = round(unfiltered / summary['total_queries'] * 100, 1)
        report += f"- **No filter:** {unfiltered} queries ({percentage}%)\n"
    
    report += f"""
## Query Details
| Query ID | Timestamp | Query | Chunks | Time (s) | Efficiency |
|----------|-----------|-------|--------|----------|------------|
"""
    
    for query in aggregated_data['queries']:
        query_id = query['query_id']
        timestamp = query['timestamp'][:16]  # Just date and time
        query_text = query['query'][:50] + "..." if len(query['query']) > 50 else query['query']
        chunks = query['results']['chunks_found']
        time_s = query['results']['total_time_seconds']
        efficiency = query['performance']['search_efficiency']
        
        report += f"| {query_id} | {timestamp} | {query_text} | {chunks} | {time_s} | {efficiency} |\n"
    
    report += """
## Recommendations
"""
    
    # Add performance recommendations
    if eff['slow_queries'] > summary['total_queries'] * 0.2:
        report += "- ⚠️  **High slow query rate** - Consider query optimization or hardware upgrade\n"
    
    if perf['model_load_times']['avg'] > 1.0:
        report += "- 🔄 **Model loading overhead** - Consider keeping model in memory for better performance\n"
    
    if sum(eff['section_filter_usage'].values()) < summary['total_queries'] * 0.5:
        report += "- 🎯 **Low section filter usage** - Encourage more targeted queries for better performance\n"
    
    if eff['avg_chunks_per_second'] > 100:
        report += "- ✅ **Excellent throughput** - Vector database performing optimally\n"
    elif eff['avg_chunks_per_second'] > 50:
        report += "- ✅ **Good throughput** - Vector database performing well\n"
    else:
        report += "- ⚠️  **Low throughput** - Investigate performance bottlenecks\n"
    
    # Save report
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"📊 Vector performance report saved to {output_file}")

def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Aggregate Vector Debug Information')
    parser.add_argument('--input-dir', default='.', help='Directory containing vector debug files')
    parser.add_argument('--output', default='vector_performance_report.md', help='Output file for performance report')
    
    args = parser.parse_args()
    
    print("🔍 Aggregating vector debug information...")
    aggregated = aggregate_vector_debug_info(args.input_dir)
    
    if aggregated:
        print("📊 Generating performance report...")
        generate_vector_performance_report(aggregated, args.output)
        
        # Save raw data as JSON
        json_output = args.output.replace('.md', '.json')
        with open(json_output, 'w') as f:
            json.dump(aggregated, f, indent=2)
        print(f"📁 Raw debug data saved to {json_output}")
    else:
        print("❌ No vector debug data found to aggregate")

if __name__ == "__main__":
    main()