"""
Performance analyzer for metric and view execution times.
"""

from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd

from ..config import Config
from ..data_loader import PerformanceData


@dataclass
class PerformanceFinding:
    """A single performance finding."""

    entity_type: str  # "metric" or "view"
    entity_id: str
    entity_name: str
    application: str
    severity: str  # "watch", "warning", "critical"
    avg_execution_time: float
    max_execution_time: float
    execution_count: int
    avg_computed_rows: Optional[float] = None
    dimensions: Optional[int] = None


@dataclass
class PerformanceAnalysisResult:
    """Results of performance analysis."""

    # Metric summary stats
    metric_total_executions: int = 0
    metric_total_execution_time_ms: float = 0
    metric_avg_execution_time_ms: float = 0
    metric_p50_execution_time_ms: float = 0
    metric_p95_execution_time_ms: float = 0
    metric_p99_execution_time_ms: float = 0

    # Metric findings by severity
    metric_critical_count: int = 0
    metric_warning_count: int = 0
    metric_watch_count: int = 0

    # Metric findings
    metric_findings: List[PerformanceFinding] = field(default_factory=list)

    # View summary stats
    view_total_executions: int = 0
    view_total_execution_time_ms: float = 0
    view_avg_execution_time_ms: float = 0
    view_p50_execution_time_ms: float = 0
    view_p95_execution_time_ms: float = 0
    view_p99_execution_time_ms: float = 0

    # View findings by severity
    view_critical_count: int = 0
    view_warning_count: int = 0
    view_watch_count: int = 0

    # View findings
    view_findings: List[PerformanceFinding] = field(default_factory=list)

    # For scoring
    score: float = 0.0  # 0-25 points


class PerformanceAnalyzer:
    """Analyze execution performance of metrics and views."""

    def __init__(self, config: Config):
        self.config = config
        self.thresholds = config.thresholds

    def analyze(self, data: PerformanceData) -> PerformanceAnalysisResult:
        """Run performance analysis on the data."""

        result = PerformanceAnalysisResult()

        # Analyze metric executions
        if data.has_executions:
            self._analyze_metrics(data.executions, result)

        # Analyze view executions
        if data.has_views:
            self._analyze_views(data.views, result)

        # Calculate score
        result.score = self._calculate_score(result)

        # Sort findings by severity and execution time
        severity_order = {"critical": 0, "warning": 1, "watch": 2}
        result.metric_findings.sort(
            key=lambda f: (severity_order.get(f.severity, 3), -f.avg_execution_time)
        )
        result.view_findings.sort(
            key=lambda f: (severity_order.get(f.severity, 3), -f.avg_execution_time)
        )

        # Limit findings
        result.metric_findings = result.metric_findings[:self.config.max_findings_per_category]
        result.view_findings = result.view_findings[:self.config.max_findings_per_category]

        return result

    def _analyze_metrics(self, df: pd.DataFrame, result: PerformanceAnalysisResult):
        """Analyze metric execution performance."""

        # Overall stats
        result.metric_total_executions += len(df)
        result.metric_total_execution_time_ms += df["execution_time"].sum()

        exec_times = df["execution_time"].dropna()
        if len(exec_times) > 0:
            result.metric_avg_execution_time_ms = exec_times.mean()
            result.metric_p50_execution_time_ms = exec_times.quantile(0.5)
            result.metric_p95_execution_time_ms = exec_times.quantile(0.95)
            result.metric_p99_execution_time_ms = exec_times.quantile(0.99)

        # Group by metric
        metric_stats = df.groupby(
            ["application", "metric_id", "metric_name"]
        ).agg({
            "execution_time": ["mean", "max", "count"],
            "computed_rows": "mean",
            "nb_dims": "first",
        }).reset_index()

        metric_stats.columns = [
            "application", "metric_id", "metric_name",
            "avg_time", "max_time", "exec_count",
            "avg_rows", "dimensions"
        ]

        # Find slow metrics
        thresholds = self.thresholds.metric_execution

        for _, row in metric_stats.iterrows():
            avg_time = row["avg_time"]

            if pd.isna(avg_time):
                continue

            severity = None
            if avg_time >= thresholds.critical:
                severity = "critical"
                result.metric_critical_count += 1
            elif avg_time >= thresholds.warning:
                severity = "warning"
                result.metric_warning_count += 1
            elif avg_time >= thresholds.watch:
                severity = "watch"
                result.metric_watch_count += 1

            if severity:
                result.metric_findings.append(PerformanceFinding(
                    entity_type="metric",
                    entity_id=row["metric_id"],
                    entity_name=row["metric_name"],
                    application=row["application"],
                    severity=severity,
                    avg_execution_time=round(avg_time, 2),
                    max_execution_time=round(row["max_time"], 2),
                    execution_count=int(row["exec_count"]),
                    avg_computed_rows=round(row["avg_rows"], 0) if pd.notna(row["avg_rows"]) else None,
                    dimensions=int(row["dimensions"]) if pd.notna(row["dimensions"]) else None,
                ))

    def _analyze_views(self, df: pd.DataFrame, result: PerformanceAnalysisResult):
        """Analyze view render performance."""

        thresholds = self.thresholds.view_render

        # Group by view
        view_stats = df.groupby(
            ["app_id", "blockId", "blockName"]
        ).agg({
            "execution_time": ["mean", "max", "count"],
            "computed_rows": "mean",
        }).reset_index()

        view_stats.columns = [
            "app_id", "block_id", "block_name",
            "avg_time", "max_time", "exec_count", "avg_rows"
        ]

        result.view_total_executions += len(df)
        result.view_total_execution_time_ms += df["execution_time"].sum()

        exec_times = df["execution_time"].dropna()
        if len(exec_times) > 0:
            result.view_avg_execution_time_ms = exec_times.mean()
            result.view_p50_execution_time_ms = exec_times.quantile(0.5)
            result.view_p95_execution_time_ms = exec_times.quantile(0.95)
            result.view_p99_execution_time_ms = exec_times.quantile(0.99)

        for _, row in view_stats.iterrows():
            avg_time = row["avg_time"]

            if pd.isna(avg_time):
                continue

            severity = None
            if avg_time >= thresholds.critical:
                severity = "critical"
                result.view_critical_count += 1
            elif avg_time >= thresholds.warning:
                severity = "warning"
                result.view_warning_count += 1
            elif avg_time >= thresholds.watch:
                severity = "watch"
                result.view_watch_count += 1

            if severity:
                result.view_findings.append(PerformanceFinding(
                    entity_type="view",
                    entity_id=row["block_id"],
                    entity_name=row["block_name"],
                    application=row["app_id"],
                    severity=severity,
                    avg_execution_time=round(avg_time, 2),
                    max_execution_time=round(row["max_time"], 2),
                    execution_count=int(row["exec_count"]),
                    avg_computed_rows=round(row["avg_rows"], 0) if pd.notna(row["avg_rows"]) else None,
                ))

    def _calculate_score(self, result: PerformanceAnalysisResult) -> float:
        """Calculate performance score (0-25 points)."""

        max_score = self.config.scoring.performance_weight

        # Base score on average execution time
        avg_time = result.metric_avg_execution_time_ms

        if avg_time < 1000:
            base_score = max_score
        elif avg_time < 2000:
            base_score = max_score * 0.9
        elif avg_time < 3000:
            base_score = max_score * 0.8
        elif avg_time < 5000:
            base_score = max_score * 0.6
        elif avg_time < 10000:
            base_score = max_score * 0.4
        else:
            base_score = max_score * 0.2

        # Penalty for critical issues
        critical_penalty = min(result.metric_critical_count * 2, max_score * 0.3)

        return max(0, round(base_score - critical_penalty, 1))
