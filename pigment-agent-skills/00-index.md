# Pigment Modeler Agent - Skills Index

## Purpose

This collection of skill files provides comprehensive knowledge for an AI agent specialized in Pigment modeling. Each file covers a specific domain of Pigment expertise.

## Skill Files Overview

| File | Topic | Description |
|------|-------|-------------|
| `01-fundamentals.md` | Core Concepts | Blocks, Dimensions, Metrics, Tables, Properties |
| `02-formulas-syntax.md` | Formula Language | Syntax, operators, comments, basic functions |
| `03-modifiers.md` | Data Transformation | BY, ADD, REMOVE, SELECT, FILTER, EXCLUDE |
| `04-functions-reference.md` | Functions | IF, SWITCH, SPREAD, aggregations, text, dates |
| `05-performance-optimization.md` | Performance | Optimization strategies, modifier order, scalability |
| `06-data-loading-integration.md` | Data Integration | Imports, connectors, APIs, data pipelines |
| `07-reporting-visualization.md` | Reporting | Boards, Views, Widgets, Charts, KPIs |
| `08-security-permissions.md` | Security | Roles, Permissions, Access Rights, SCIM |
| `09-scenarios-versioning.md` | Scenarios | Versions, What-If, Snapshots, Data Slices |
| `10-architecture-best-practices.md` | Architecture | Design patterns, naming, anti-patterns |
| `11-workspace-reliability-audit.md` | Audit & Quality | Workspace health checks, reliability assessment |
| `12-programmatic-audit-apis.md` | API Auditing | Audit Logs API, Metadata API, SIEM integration |
| `13-performance-data-analysis.md` | Performance Analysis | Execution data analysis, cross-referencing, scoring |

## Quick Reference by Task

### Building a New Model
1. Start with `01-fundamentals.md` for core concepts
2. Reference `10-architecture-best-practices.md` for design
3. Use `02-formulas-syntax.md` and `03-modifiers.md` for calculations

### Writing Formulas
1. `02-formulas-syntax.md` - Basic syntax
2. `03-modifiers.md` - Data transformations
3. `04-functions-reference.md` - Available functions

### Optimizing Performance
1. `05-performance-optimization.md` - Primary reference
2. `03-modifiers.md` - Optimal modifier order

### Setting Up Data Flows
1. `06-data-loading-integration.md` - Import methods
2. `01-fundamentals.md` - Dimension vs Transaction vs Metric decision

### Building Reports
1. `07-reporting-visualization.md` - Boards and Widgets
2. `09-scenarios-versioning.md` - Scenario comparison

### Configuring Security
1. `08-security-permissions.md` - Complete security guide

### Planning and Forecasting
1. `09-scenarios-versioning.md` - Scenarios and versions
2. `10-architecture-best-practices.md` - Planning architecture

### Auditing a Workspace
1. `11-workspace-reliability-audit.md` - Complete audit framework
2. `12-programmatic-audit-apis.md` - Automated auditing via APIs
3. `13-performance-data-analysis.md` - Execution data analysis & scoring
4. `10-architecture-best-practices.md` - Anti-patterns to detect
5. `05-performance-optimization.md` - Performance assessment
6. `08-security-permissions.md` - Security audit checklist

## Key Concepts Summary

### Block Types
- **Dimension List** (Blue): Structure/axes of model
- **Transaction List** (Green): Event/transaction data
- **Metric** (Purple): Calculations and data
- **Table** (Red): Summarized views

### Essential Modifiers
```
FILTER → SELECT → BY (Agg) → REMOVE → BY (Alloc) → ADD
```

### Default Roles
- **Admin**: Full access
- **Modeler**: Build models, no security config
- **Reader**: View only

### Core Best Practices
1. Avoid hard-coding values
2. Break complex formulas into components
3. Use consistent naming conventions
4. Minimize unnecessary dimensions
5. Document your work

## Official Resources

- **Documentation**: https://kb.pigment.com
- **Community**: https://community.pigment.com
- **Academy**: https://academy.pigment.com
- **Support**: https://support.pigment.com

## Usage Notes for Agent

When assisting with Pigment modeling:

1. **Identify the task type** and reference appropriate skill files
2. **Start with fundamentals** if user is new to Pigment
3. **Provide syntax examples** from the skill files
4. **Warn about common anti-patterns** from best practices
5. **Cite official documentation** when available
6. **Recommend performance optimizations** proactively

## Version

- Created: 2026-02-03
- Sources: Pigment Documentation (kb.pigment.com), Pigment Community (community.pigment.com)
- Coverage: Pigment EPM platform fundamentals through advanced architecture
