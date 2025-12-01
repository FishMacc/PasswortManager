"""
Performance-Messung für UI-Komponenten

Misst Rendering-Zeit, Memory-Usage und Response-Zeit.
"""
import time
import logging
import psutil
import os
from typing import Callable, Dict, Any, Optional
from contextlib import contextmanager
from PyQt6.QtCore import QElapsedTimer

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Sammelt und analysiert Performance-Metriken"""

    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.process = psutil.Process(os.getpid())

    @contextmanager
    def measure(self, name: str, category: str = "general"):
        """
        Context Manager für Performance-Messung

        Args:
            name: Name der Messung
            category: Kategorie (z.B. "rendering", "database", "ui")

        Usage:
            with perf.measure("render_dialog", "ui"):
                dialog.show()
        """
        # Start-Metriken
        start_time = time.perf_counter()
        start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        try:
            yield
        finally:
            # End-Metriken
            end_time = time.perf_counter()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB

            duration = (end_time - start_time) * 1000  # ms
            memory_delta = end_memory - start_memory

            # Speichere Metrik
            if category not in self.metrics:
                self.metrics[category] = {}

            self.metrics[category][name] = {
                "duration_ms": round(duration, 2),
                "memory_delta_mb": round(memory_delta, 2),
                "start_memory_mb": round(start_memory, 2),
                "end_memory_mb": round(end_memory, 2),
                "timestamp": time.time()
            }

            # Log
            if duration > 100:  # Warne bei langsamen Operationen
                logger.warning(f"⚠️  {category}/{name}: {duration:.2f}ms (langsam!)")
            else:
                logger.info(f"✓ {category}/{name}: {duration:.2f}ms")

            if memory_delta > 10:  # Warne bei hohem Memory-Verbrauch
                logger.warning(f"⚠️  {category}/{name}: {memory_delta:.2f}MB Memory-Zuwachs")

    def measure_function(self, func: Callable, name: str, category: str = "function",
                        iterations: int = 1) -> Dict[str, Any]:
        """
        Misst Performance einer Funktion über mehrere Iterationen

        Args:
            func: Die zu messende Funktion
            name: Name der Messung
            category: Kategorie
            iterations: Anzahl Wiederholungen

        Returns:
            Dict mit avg_duration_ms, min_duration_ms, max_duration_ms, total_memory_delta_mb
        """
        durations = []
        start_memory = self.process.memory_info().rss / 1024 / 1024

        for i in range(iterations):
            start_time = time.perf_counter()

            try:
                func()
            except Exception as e:
                logger.error(f"Fehler in Iteration {i}: {e}")
                continue

            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000
            durations.append(duration)

        end_memory = self.process.memory_info().rss / 1024 / 1024

        if not durations:
            return {}

        result = {
            "name": name,
            "category": category,
            "iterations": iterations,
            "avg_duration_ms": round(sum(durations) / len(durations), 2),
            "min_duration_ms": round(min(durations), 2),
            "max_duration_ms": round(max(durations), 2),
            "total_duration_ms": round(sum(durations), 2),
            "memory_delta_mb": round(end_memory - start_memory, 2)
        }

        logger.info(f"📊 {category}/{name} ({iterations}x): "
                   f"Avg={result['avg_duration_ms']:.2f}ms, "
                   f"Min={result['min_duration_ms']:.2f}ms, "
                   f"Max={result['max_duration_ms']:.2f}ms")

        return result

    def measure_qt_render(self, widget, name: str) -> float:
        """
        Misst Qt Rendering-Zeit

        Args:
            widget: Das Qt Widget
            name: Name der Messung

        Returns:
            Rendering-Zeit in ms
        """
        timer = QElapsedTimer()
        timer.start()

        widget.repaint()

        elapsed = timer.elapsed()

        logger.info(f"🎨 Rendering {name}: {elapsed}ms")

        return elapsed

    def get_memory_usage(self) -> Dict[str, float]:
        """
        Gibt aktuellen Memory-Verbrauch zurück

        Returns:
            Dict mit rss_mb, vms_mb, percent
        """
        mem_info = self.process.memory_info()

        return {
            "rss_mb": round(mem_info.rss / 1024 / 1024, 2),  # Resident Set Size
            "vms_mb": round(mem_info.vms / 1024 / 1024, 2),  # Virtual Memory Size
            "percent": round(self.process.memory_percent(), 2)
        }

    def get_cpu_usage(self) -> float:
        """
        Gibt aktuellen CPU-Verbrauch zurück

        Returns:
            CPU-Prozent
        """
        return round(self.process.cpu_percent(interval=0.1), 2)

    def get_summary(self) -> Dict[str, Any]:
        """
        Gibt Zusammenfassung aller Metriken zurück

        Returns:
            Dict mit Kategorien und deren Metriken
        """
        summary = {
            "categories": {},
            "total_measurements": 0,
            "memory_usage": self.get_memory_usage(),
            "cpu_usage": self.get_cpu_usage()
        }

        for category, measurements in self.metrics.items():
            cat_summary = {
                "count": len(measurements),
                "total_duration_ms": 0,
                "avg_duration_ms": 0,
                "slowest": None,
                "fastest": None
            }

            durations = []
            for name, data in measurements.items():
                duration = data.get("duration_ms", 0)
                durations.append((name, duration))
                cat_summary["total_duration_ms"] += duration

            if durations:
                cat_summary["avg_duration_ms"] = round(
                    cat_summary["total_duration_ms"] / len(durations), 2
                )
                cat_summary["slowest"] = max(durations, key=lambda x: x[1])
                cat_summary["fastest"] = min(durations, key=lambda x: x[1])

            summary["categories"][category] = cat_summary
            summary["total_measurements"] += len(measurements)

        return summary

    def print_report(self):
        """Gibt detaillierten Performance-Report aus"""
        print("\n" + "="*60)
        print("📊 PERFORMANCE REPORT")
        print("="*60)

        summary = self.get_summary()

        # System-Info
        print(f"\n💻 System:")
        print(f"  Memory: {summary['memory_usage']['rss_mb']:.2f} MB "
              f"({summary['memory_usage']['percent']:.1f}%)")
        print(f"  CPU: {summary['cpu_usage']:.1f}%")

        # Kategorien
        print(f"\n📈 Messungen: {summary['total_measurements']} gesamt")

        for category, data in summary["categories"].items():
            print(f"\n{category.upper()}:")
            print(f"  Anzahl: {data['count']}")
            print(f"  Gesamt: {data['total_duration_ms']:.2f}ms")
            print(f"  Durchschnitt: {data['avg_duration_ms']:.2f}ms")

            if data['slowest']:
                name, duration = data['slowest']
                print(f"  Langsamste: {name} ({duration:.2f}ms)")

            if data['fastest']:
                name, duration = data['fastest']
                print(f"  Schnellste: {name} ({duration:.2f}ms)")

        # Detaillierte Metriken
        print(f"\n📋 Detaillierte Metriken:")
        for category, measurements in self.metrics.items():
            print(f"\n  {category}:")
            for name, data in measurements.items():
                duration = data.get("duration_ms", 0)
                memory = data.get("memory_delta_mb", 0)

                status = "✓"
                if duration > 100:
                    status = "⚠️"
                if duration > 500:
                    status = "❌"

                print(f"    {status} {name}: {duration:.2f}ms "
                      f"(Memory: {memory:+.2f}MB)")

        print("\n" + "="*60 + "\n")

    def export_json(self, filepath: str):
        """
        Exportiert Metriken als JSON

        Args:
            filepath: Pfad zur JSON-Datei
        """
        import json

        data = {
            "summary": self.get_summary(),
            "metrics": self.metrics,
            "timestamp": time.time()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Performance-Daten exportiert: {filepath}")

    def reset(self):
        """Setzt alle Metriken zurück"""
        self.metrics.clear()
        logger.info("Performance-Metriken zurückgesetzt")


# Singleton-Instanz
performance = PerformanceMetrics()
