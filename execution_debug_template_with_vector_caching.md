# RFP Analysis Execution Report with Vector Caching

## Summary
- **Start Time:** {start_time}
- **End Time:** {end_time}
- **Total Duration:** {duration}
- **Execution Mode:** {execution_mode}
- **Success Rate:** {success_rate}

## Vector Database Performance
- **Database Status:** {vector_db_status}
- **Total Chunks Indexed:** {total_chunks}
- **Vector Queries Executed:** {total_queries}
- **Average Query Time:** {avg_query_time}s
- **Cache Hit Rate:** {cache_hit_rate}%

### Vector Query Breakdown
| Query ID | Phase | Query Type | Chunks Found | Time (s) | Efficiency | Section Filter |
|----------|-------|------------|--------------|----------|------------|----------------|
{vector_query_table}

### Vector Database Statistics
- **Database Size:** {db_size_mb} MB
- **Index Build Time:** {index_build_time}s  
- **Model Load Time:** {model_load_time}s (average)
- **Search Performance:** {search_performance}
- **Section Distribution:**
  - Requirements: {req_chunks} chunks
  - Timeline: {timeline_chunks} chunks  
  - Evaluation: {eval_chunks} chunks
  - Pricing: {pricing_chunks} chunks
  - Technical: {tech_chunks} chunks
  - General: {general_chunks} chunks

## Phase Breakdown
| Phase | Duration | Status | Prompts | Vector Queries | Success Rate |
|-------|----------|--------|---------|----------------|--------------|
{phase_breakdown_table}

## Generated Files
### Extracts ({extract_count} files)
{extract_files}

### Analysis ({analysis_count} files)  
{analysis_files}

### Summary ({summary_count} files)
{summary_files}

### Supporting Files ({support_count} files)
{support_files}

## Vector Caching Efficiency Analysis

### Query Performance Metrics
- **Fastest Query:** {fastest_query} ({fastest_time}s)
- **Slowest Query:** {slowest_query} ({slowest_time}s)
- **Most Chunks Retrieved:** {max_chunks_query} ({max_chunks} chunks)
- **Model Loading Overhead:** {model_overhead_total}s total

### Caching Effectiveness
- **Duplicate Queries:** {duplicate_queries} (potential cache opportunities)
- **Section Filter Usage:** {section_filter_usage}%
- **Query Complexity Distribution:**
  - Simple (< 0.1s): {simple_queries}
  - Moderate (0.1-0.5s): {moderate_queries}  
  - Complex (> 0.5s): {complex_queries}

### Optimization Recommendations
{optimization_recommendations}

## Errors and Issues
{error_section}

## Token Usage Analysis (Traditional vs Vector-Enhanced)
| Metric | Traditional | With Vector DB | Improvement |
|--------|-------------|----------------|-------------|
| Input Tokens | {traditional_input_tokens} | {vector_input_tokens} | {token_reduction}% |
| Processing Time | {traditional_time} | {vector_time} | {time_improvement}% |
| Context Utilization | {traditional_context}% | {vector_context}% | {context_efficiency}% |

## Performance Notes
- **Vector Database Benefits:** {vector_benefits}
- **Query Optimization:** {query_optimization}  
- **Resource Utilization:** {resource_utilization}
- **Scalability:** {scalability_notes}

## Key Findings Summary
### **Strategic Recommendation:** {recommendation}
- **Opportunity Value:** {opportunity_value}
- **Competitive Position:** {competitive_position}
- **Win Probability:** {win_probability}

### **Critical Success Factors:**
{success_factors}

### **Immediate Actions:**
{immediate_actions}

## Execution Quality Metrics
- **File Creation Success Rate:** {file_success_rate}
- **Prompt Compliance:** {prompt_compliance}
- **State Management:** {state_management}
- **Vector Query Reliability:** {vector_reliability}
- **Debug Logging:** {debug_logging}
- **User Experience:** {user_experience}

## Vector Database Validation Results
- **Index Integrity:** {index_integrity}
- **Query Accuracy:** {query_accuracy}
- **Performance Consistency:** {performance_consistency}  
- **Resource Efficiency:** {resource_efficiency}
- **Scalability Test:** {scalability_test}

**WORKFLOW EXECUTION STATUS: {final_status}**

---
*Debug template includes vector caching metrics for performance validation*
*Generated with enhanced vector database monitoring capabilities*