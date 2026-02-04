# Pigment Workspace Reliability Audit

Tools, methodologies, and sample data for auditing Pigment workspace reliability.

## Contents

### Skill Files

| File | Topic | Description |
|------|-------|-------------|
| `11-workspace-reliability-audit.md` | Audit Framework | Complete manual audit checklist and methodology |
| `12-programmatic-audit-apis.md` | API Auditing | Audit Logs API, Metadata API, SIEM integration |
| `13-performance-data-analysis.md` | Performance Analysis | Execution data analysis, cross-referencing, scoring |

### Sample Data

Located in `sample-data/`:

| File | Records | Description |
|------|---------|-------------|
| `Executions_anonymized_basic.csv` | ~35K | Metric execution performance data |
| `Views_Executions_anonymized_basic.csv` | ~7.8K | View rendering performance data |
| `Armset_Upmset_Executions_anonymized_basic.csv` | ~1.4K | ARMSET/UPMSET operations data |

## Audit Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RELIABILITY AUDIT WORKFLOW                    │
└─────────────────────────────────────────────────────────────────┘

1. COLLECT DATA
   ├── Performance CSVs (execution times, rows, dimensions)
   ├── Metadata API (application/block structure)
   └── Audit Logs API (user activity, changes)

2. ANALYZE
   ├── 11-workspace-reliability-audit.md → Manual checklist
   ├── 12-programmatic-audit-apis.md → API-based automation
   └── 13-performance-data-analysis.md → Data analysis scripts

3. SCORE
   ├── Performance (execution times)
   ├── Optimization (scoping %)
   ├── Complexity (dimensions)
   └── Views (render times)

4. REPORT & REMEDIATE
   ├── Executive summary
   ├── Priority matrix
   └── Actionable recommendations
```

## Data Sources Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Performance    │     │   Metadata API  │     │  Audit Logs API │
│  CSV Exports    │     │                 │     │                 │
│                 │     │  • Block names  │     │  • User actions │
│  • exec_time    │     │  • Dimensions   │     │  • Timestamps   │
│  • computed_rows│     │  • App struct   │     │  • Changes      │
│  • nb_dims      │     │                 │     │                 │
│  • scoped_level │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                  ┌──────────────────────────┐
                  │    COMBINED ANALYSIS     │
                  │                          │
                  │  • Slow metrics + names  │
                  │  • User → performance    │
                  │  • App workload ranking  │
                  └──────────────────────────┘
```

## Reliability Score

### Components (0-100)

| Component | Weight | Source |
|-----------|--------|--------|
| Performance | 25 pts | Avg execution_time |
| Optimization | 25 pts | % FullyScoped calculations |
| Complexity | 25 pts | % metrics with nb_dims ≤ 6 |
| Views | 25 pts | % views with render < 3s |

### Grading

| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | A | Excellent |
| 75-89 | B | Good |
| 60-74 | C | Needs Improvement |
| 40-59 | D | Poor |
| 0-39 | F | Critical |

## Alert Thresholds

| Metric | Watch | Warning | Critical |
|--------|-------|---------|----------|
| Metric execution | > 3s | > 5s | > 30s |
| View render | > 2s | > 3s | > 15s |
| Computed rows | > 500K | > 1M | > 10M |
| Dimensions | > 5 | > 6 | > 10 |
| Non-scoped % | > 20% | > 30% | > 50% |

## Sample Queries

### Top 10 Slowest Metrics
```python
executions_df.nlargest(10, 'execution_time')[
    ['application', 'metric_name', 'execution_time', 'nb_dims', 'scoped_level']
]
```

### Scoping Optimization Opportunities
```python
executions_df[
    (executions_df['scoped_level'] == 'NoChange') &
    (executions_df['execution_time'] > 5000)
].groupby('metric_name')['execution_time'].mean()
```

### Application Load Distribution
```python
executions_df.groupby('application')['execution_time'].sum().sort_values(ascending=False)
```

## Audit Frequency

| Audit Type | Frequency | Scope |
|------------|-----------|-------|
| Quick Health Check | Weekly | Key metrics, errors |
| Standard Audit | Monthly | Performance, security |
| Comprehensive Audit | Quarterly | Full reliability review |

## Related Modeling Knowledge

For understanding Pigment concepts referenced in audits, see:
- `../modeling-knowledge/05-performance-optimization.md`
- `../modeling-knowledge/08-security-permissions.md`
- `../modeling-knowledge/10-architecture-best-practices.md`
