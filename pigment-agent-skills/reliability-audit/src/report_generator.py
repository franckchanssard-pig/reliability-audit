"""
Report generator for reliability audit results.

Generates CSV and HTML reports.
"""

import csv
from pathlib import Path
from typing import List
from datetime import datetime

from .config import Config
from .scoring import ReliabilityScore


class ReportGenerator:
    """Generate audit reports in various formats."""

    def __init__(self, config: Config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent

    def generate(self, score: ReliabilityScore) -> List[str]:
        """Generate reports in configured formats."""

        output_dir = self.base_dir / self.config.output_directory
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        generated_files = []

        for fmt in self.config.output_formats:
            if fmt == "csv":
                files = self._generate_csv(score, output_dir, timestamp)
                generated_files.extend(files)
            elif fmt == "html":
                file = self._generate_html(score, output_dir, timestamp)
                generated_files.append(file)

        return generated_files

    def _generate_csv(self, score: ReliabilityScore, output_dir: Path, timestamp: str) -> List[str]:
        """Generate CSV reports."""

        files = []

        # Summary CSV
        summary_file = output_dir / f"audit_summary_{timestamp}.csv"
        with open(summary_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Timestamp", score.timestamp])
            writer.writerow(["Total Score", score.total_score])
            writer.writerow(["Grade", score.grade])
            writer.writerow(["Performance Score", score.performance_score])
            writer.writerow(["Optimization Score", score.optimization_score])
            writer.writerow(["Complexity Score", score.complexity_score])
            writer.writerow(["Views Score", score.views_score])
            writer.writerow([])
            writer.writerow(["Data Summary", ""])
            for key, value in score.data_summary.items():
                writer.writerow([key, value])

        files.append(str(summary_file))

        # Performance findings CSV
        if score.performance_result and score.performance_result.findings:
            perf_file = output_dir / f"performance_findings_{timestamp}.csv"
            with open(perf_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Entity Type", "Entity ID", "Entity Name", "Application",
                    "Severity", "Avg Execution Time (ms)", "Max Execution Time (ms)",
                    "Execution Count", "Avg Computed Rows", "Dimensions"
                ])
                for finding in score.performance_result.findings:
                    writer.writerow([
                        finding.entity_type,
                        finding.entity_id,
                        finding.entity_name,
                        finding.application,
                        finding.severity,
                        finding.avg_execution_time,
                        finding.max_execution_time,
                        finding.execution_count,
                        finding.avg_computed_rows or "",
                        finding.dimensions or "",
                    ])
            files.append(str(perf_file))

        # Scoping findings CSV
        if score.scoping_result and score.scoping_result.findings:
            scoping_file = output_dir / f"scoping_findings_{timestamp}.csv"
            with open(scoping_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Metric ID", "Metric Name", "Application", "Scoped Level",
                    "Avg Execution Time (ms)", "Total Execution Time (ms)",
                    "Execution Count", "Potential Savings %"
                ])
                for finding in score.scoping_result.findings:
                    writer.writerow([
                        finding.metric_id,
                        finding.metric_name,
                        finding.application,
                        finding.scoped_level,
                        finding.avg_execution_time,
                        finding.total_execution_time,
                        finding.execution_count,
                        finding.potential_savings_pct,
                    ])
            files.append(str(scoping_file))

        # Complexity findings CSV
        if score.complexity_result and score.complexity_result.findings:
            complexity_file = output_dir / f"complexity_findings_{timestamp}.csv"
            with open(complexity_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Metric ID", "Metric Name", "Application", "Dimensions",
                    "Severity", "Avg Execution Time (ms)", "Avg Computed Rows"
                ])
                for finding in score.complexity_result.findings:
                    writer.writerow([
                        finding.metric_id,
                        finding.metric_name,
                        finding.application,
                        finding.dimensions,
                        finding.severity,
                        finding.avg_execution_time,
                        finding.avg_computed_rows or "",
                    ])
            files.append(str(complexity_file))

        return files

    def _generate_html(self, score: ReliabilityScore, output_dir: Path, timestamp: str) -> str:
        """Generate HTML report."""

        html_file = output_dir / f"audit_report_{timestamp}.html"

        # Determine colors
        grade_colors = {
            "A": "#22c55e",  # green
            "B": "#84cc16",  # lime
            "C": "#eab308",  # yellow
            "D": "#f97316",  # orange
            "F": "#ef4444",  # red
        }
        grade_color = grade_colors.get(score.grade, "#6b7280")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pigment Reliability Audit Report</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f9fafb;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #111827; margin-bottom: 0.5rem; }}
        h2 {{ color: #374151; margin: 2rem 0 1rem; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }}
        h3 {{ color: #4b5563; margin: 1.5rem 0 0.75rem; }}
        .timestamp {{ color: #6b7280; font-size: 0.875rem; margin-bottom: 2rem; }}

        .score-card {{
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        .score-header {{
            display: flex;
            align-items: center;
            gap: 2rem;
            margin-bottom: 1.5rem;
        }}
        .grade {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: {grade_color};
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            font-weight: bold;
        }}
        .total-score {{
            font-size: 2rem;
            font-weight: bold;
        }}
        .total-score span {{ font-size: 1rem; color: #6b7280; }}

        .score-breakdown {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}
        .score-item {{
            background: #f3f4f6;
            padding: 1rem;
            border-radius: 0.5rem;
        }}
        .score-item-label {{ font-size: 0.875rem; color: #6b7280; }}
        .score-item-value {{ font-size: 1.5rem; font-weight: bold; }}
        .score-bar {{
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            margin-top: 0.5rem;
            overflow: hidden;
        }}
        .score-bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s;
        }}

        .recommendations {{
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        .recommendation {{
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            border-radius: 0 0.5rem 0.5rem 0;
        }}
        .recommendation.critical {{
            background: #fee2e2;
            border-left-color: #ef4444;
        }}

        .findings {{
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{ background: #f9fafb; font-weight: 600; }}
        tr:hover {{ background: #f9fafb; }}

        .severity {{
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .severity.critical {{ background: #fee2e2; color: #dc2626; }}
        .severity.warning {{ background: #fef3c7; color: #d97706; }}
        .severity.watch {{ background: #dbeafe; color: #2563eb; }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        .stat {{
            background: #f3f4f6;
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
        }}
        .stat-value {{ font-size: 1.5rem; font-weight: bold; color: #111827; }}
        .stat-label {{ font-size: 0.75rem; color: #6b7280; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Pigment Reliability Audit Report</h1>
        <p class="timestamp">Generated: {score.timestamp}</p>

        <div class="score-card">
            <div class="score-header">
                <div class="grade">{score.grade}</div>
                <div>
                    <div class="total-score">{score.total_score} <span>/ 100</span></div>
                    <div style="color: #6b7280">Overall Reliability Score</div>
                </div>
            </div>

            <div class="score-breakdown">
                {self._render_score_item("Performance", score.performance_score, 25)}
                {self._render_score_item("Optimization", score.optimization_score, 25)}
                {self._render_score_item("Complexity", score.complexity_score, 25)}
                {self._render_score_item("Views", score.views_score, 25)}
            </div>
        </div>

        {self._render_data_summary(score)}

        {self._render_recommendations(score)}

        {self._render_performance_findings(score)}

        {self._render_scoping_analysis(score)}

        {self._render_complexity_findings(score)}

        {self._render_workload_analysis(score)}
    </div>
</body>
</html>"""

        with open(html_file, "w") as f:
            f.write(html)

        return str(html_file)

    def _render_score_item(self, label: str, value: float, max_val: int) -> str:
        pct = (value / max_val) * 100
        color = "#22c55e" if pct >= 70 else "#eab308" if pct >= 40 else "#ef4444"
        return f"""
            <div class="score-item">
                <div class="score-item-label">{label}</div>
                <div class="score-item-value">{value}</div>
                <div class="score-bar">
                    <div class="score-bar-fill" style="width: {pct}%; background: {color};"></div>
                </div>
            </div>"""

    def _render_data_summary(self, score: ReliabilityScore) -> str:
        summary = score.data_summary
        return f"""
        <div class="findings">
            <h2>📊 Data Summary</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value">{summary.get('executions_records', 0):,}</div>
                    <div class="stat-label">Executions</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{summary.get('views_records', 0):,}</div>
                    <div class="stat-label">View Renders</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{summary.get('unique_applications', 0)}</div>
                    <div class="stat-label">Applications</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{summary.get('unique_metrics', 0)}</div>
                    <div class="stat-label">Unique Metrics</div>
                </div>
            </div>
        </div>"""

    def _render_recommendations(self, score: ReliabilityScore) -> str:
        if not score.recommendations:
            return ""

        items = ""
        for rec in score.recommendations:
            css_class = "critical" if "CRITICAL" in rec or "🔴" in rec else ""
            items += f'<div class="recommendation {css_class}">{rec}</div>\n'

        return f"""
        <div class="recommendations">
            <h2>💡 Recommendations</h2>
            {items}
        </div>"""

    def _render_performance_findings(self, score: ReliabilityScore) -> str:
        if not score.performance_result or not score.performance_result.findings:
            return ""

        perf = score.performance_result

        rows = ""
        for f in perf.findings[:20]:
            rows += f"""
            <tr>
                <td>{f.entity_type}</td>
                <td>{f.entity_name}</td>
                <td>{f.application}</td>
                <td><span class="severity {f.severity}">{f.severity}</span></td>
                <td>{f.avg_execution_time:,.0f} ms</td>
                <td>{f.max_execution_time:,.0f} ms</td>
                <td>{f.execution_count}</td>
                <td>{f.dimensions or '-'}</td>
            </tr>"""

        return f"""
        <div class="findings">
            <h2>⚡ Performance Findings</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value">{perf.avg_execution_time_ms:,.0f} ms</div>
                    <div class="stat-label">Avg Execution Time</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{perf.p95_execution_time_ms:,.0f} ms</div>
                    <div class="stat-label">P95 Execution Time</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #ef4444">{perf.critical_count}</div>
                    <div class="stat-label">Critical Issues</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #f59e0b">{perf.warning_count}</div>
                    <div class="stat-label">Warnings</div>
                </div>
            </div>
            <h3>Top Issues</h3>
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Name</th>
                        <th>Application</th>
                        <th>Severity</th>
                        <th>Avg Time</th>
                        <th>Max Time</th>
                        <th>Count</th>
                        <th>Dims</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""

    def _render_scoping_analysis(self, score: ReliabilityScore) -> str:
        if not score.scoping_result:
            return ""

        scoping = score.scoping_result

        rows = ""
        for f in scoping.findings[:15]:
            rows += f"""
            <tr>
                <td>{f.metric_name}</td>
                <td>{f.application}</td>
                <td>{f.avg_execution_time:,.0f} ms</td>
                <td>{f.total_execution_time:,.0f} ms</td>
                <td>{f.execution_count}</td>
                <td>{f.potential_savings_pct}%</td>
            </tr>"""

        findings_table = ""
        if rows:
            findings_table = f"""
            <h3>Optimization Candidates (NoChange metrics with high execution time)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Metric Name</th>
                        <th>Application</th>
                        <th>Avg Time</th>
                        <th>Total Time</th>
                        <th>Count</th>
                        <th>Potential Savings</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>"""

        return f"""
        <div class="findings">
            <h2>🎯 Scoping Optimization</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value" style="color: #22c55e">{scoping.fully_scoped_pct:.0f}%</div>
                    <div class="stat-label">Fully Scoped</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #eab308">{scoping.partially_scoped_pct:.0f}%</div>
                    <div class="stat-label">Partially Scoped</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #ef4444">{scoping.no_change_pct:.0f}%</div>
                    <div class="stat-label">Not Scoped</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{scoping.potential_savings_ms/3600000:.1f}h</div>
                    <div class="stat-label">Potential Savings</div>
                </div>
            </div>
            {findings_table}
        </div>"""

    def _render_complexity_findings(self, score: ReliabilityScore) -> str:
        if not score.complexity_result:
            return ""

        complexity = score.complexity_result

        rows = ""
        for f in complexity.findings[:15]:
            avg_rows_str = f"{f.avg_computed_rows:,.0f}" if f.avg_computed_rows else "-"
            rows += f"""
            <tr>
                <td>{f.metric_name}</td>
                <td>{f.application}</td>
                <td><span class="severity {f.severity}">{f.dimensions}</span></td>
                <td>{f.avg_execution_time:,.0f} ms</td>
                <td>{avg_rows_str}</td>
            </tr>"""

        findings_table = ""
        if rows:
            findings_table = f"""
            <h3>High-Dimension Metrics</h3>
            <table>
                <thead>
                    <tr>
                        <th>Metric Name</th>
                        <th>Application</th>
                        <th>Dimensions</th>
                        <th>Avg Time</th>
                        <th>Avg Rows</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>"""

        correlation_info = ""
        if complexity.dims_time_correlation is not None:
            correlation_info = f"""
            <p style="margin-top: 1rem; color: #6b7280;">
                📊 Correlation between dimensions and execution time: <strong>{complexity.dims_time_correlation:.2f}</strong>
                {' (strong)' if abs(complexity.dims_time_correlation) > 0.5 else ' (moderate)' if abs(complexity.dims_time_correlation) > 0.3 else ' (weak)'}
            </p>"""

        return f"""
        <div class="findings">
            <h2>📐 Dimensional Complexity</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value">{complexity.avg_dimensions:.1f}</div>
                    <div class="stat-label">Avg Dimensions</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{complexity.max_dimensions}</div>
                    <div class="stat-label">Max Dimensions</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #ef4444">{complexity.critical_count}</div>
                    <div class="stat-label">Critical (&gt;10 dims)</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #f59e0b">{complexity.warning_count}</div>
                    <div class="stat-label">Warning (&gt;6 dims)</div>
                </div>
            </div>
            {correlation_info}
            {findings_table}
        </div>"""

    def _render_workload_analysis(self, score: ReliabilityScore) -> str:
        if not score.workload_result:
            return ""

        workload = score.workload_result

        rows = ""
        for app in workload.app_workloads[:10]:
            rows += f"""
            <tr>
                <td>{app.application}</td>
                <td>{app.total_execution_time_ms/1000:,.1f}s</td>
                <td>{app.total_executions:,}</td>
                <td>{app.unique_metrics}</td>
                <td>{app.pct_of_total_time:.1f}%</td>
            </tr>"""

        return f"""
        <div class="findings">
            <h2>📈 Workload Distribution</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value">{workload.total_execution_time_hours:.1f}h</div>
                    <div class="stat-label">Total Compute Time</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{workload.unique_applications}</div>
                    <div class="stat-label">Applications</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{workload.total_view_executions:,}</div>
                    <div class="stat-label">View Renders</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{workload.slow_views_pct:.1f}%</div>
                    <div class="stat-label">Slow Views</div>
                </div>
            </div>
            <h3>Applications by Compute Load</h3>
            <table>
                <thead>
                    <tr>
                        <th>Application</th>
                        <th>Total Time</th>
                        <th>Executions</th>
                        <th>Metrics</th>
                        <th>% of Total</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""
