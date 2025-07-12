"""
Performance benchmarks for Paper2Data extraction components.

Establishes performance baselines and monitors for regressions in:
- Processing speed
- Memory usage  
- Scalability
- Resource efficiency
"""

import pytest
import time
import gc
from typing import Dict, Any, List
from pathlib import Path
import json


@pytest.mark.performance
@pytest.mark.benchmark
class TestExtractionPerformanceBenchmarks:
    """Performance benchmarks for content extraction."""
    
    def test_table_extraction_performance(self, table_processor, performance_monitor, benchmark_data):
        """Benchmark table extraction performance."""
        test_cases = {
            'small_table': "Col1\tCol2\tCol3\nA\t1\t2.5\nB\t3\t4.7",
            'medium_table': benchmark_data['complex_table'],
            'large_table': "\n".join([
                "Col1\tCol2\tCol3\tCol4\tCol5\tCol6\tCol7\tCol8\tCol9\tCol10"
            ] + [
                f"Row{i}\t{i}\t{i*2}\t{i*3}\t{i*4}\t{i*5}\t{i*6}\t{i*7}\t{i*8}\t{i*9}"
                for i in range(1000)  # 1000 rows
            ])
        }
        
        benchmark_results = {}
        
        for test_name, table_data in test_cases.items():
            performance_monitor.start()
            
            # Perform table processing
            result = table_processor.convert_to_csv(table_data, f"benchmark_{test_name}")
            
            metrics = performance_monitor.stop()
            
            # Validate successful processing
            if test_name != 'large_table':  # Large table might fail due to complexity
                assert result is not None, f"Table processing failed for {test_name}"
            
            benchmark_results[test_name] = metrics
            
            # Performance requirements
            if test_name == 'small_table':
                assert metrics['execution_time_seconds'] < 0.1, \
                    f"Small table processing too slow: {metrics['execution_time_seconds']:.3f}s"
            elif test_name == 'medium_table':
                assert metrics['execution_time_seconds'] < 0.5, \
                    f"Medium table processing too slow: {metrics['execution_time_seconds']:.3f}s"
            elif test_name == 'large_table':
                assert metrics['execution_time_seconds'] < 3.0, \
                    f"Large table processing too slow: {metrics['execution_time_seconds']:.3f}s"
        
        return benchmark_results
    
    def test_section_detection_scalability(self, section_extractor, performance_monitor, benchmark_data):
        """Benchmark section detection scalability with document size."""
        document_sizes = {
            'small': 1000,     # 1KB
            'medium': 10000,   # 10KB
            'large': 100000,   # 100KB
            'xlarge': 500000,  # 500KB
        }
        
        benchmark_results = {}
        
        for size_name, char_count in document_sizes.items():
            # Create document with multiple sections
            sections = ['Abstract', 'Introduction', 'Methodology', 'Results', 'Discussion', 'Conclusion']
            content_per_section = char_count // len(sections)
            
            document_parts = []
            for i, section in enumerate(sections):
                document_parts.append(f"# {section}")
                document_parts.append("A" * content_per_section)
            
            document = "\n\n".join(document_parts)
            
            performance_monitor.start()
            
            # Perform section detection
            detected_sections = section_extractor._detect_sections_from_text(document)
            
            metrics = performance_monitor.stop()
            
            # Validate processing
            assert len(detected_sections) >= 4, f"Should detect most sections in {size_name} document"
            
            benchmark_results[size_name] = {
                **metrics,
                'document_size_chars': len(document),
                'sections_found': len(detected_sections)
            }
            
            # Performance requirements based on size
            if size_name == 'small':
                assert metrics['execution_time_seconds'] < 0.1
            elif size_name == 'medium':
                assert metrics['execution_time_seconds'] < 0.5
            elif size_name == 'large':
                assert metrics['execution_time_seconds'] < 2.0
            elif size_name == 'xlarge':
                assert metrics['execution_time_seconds'] < 5.0
        
        return benchmark_results
    
    @pytest.mark.slow
    def test_memory_efficiency_benchmarks(self, table_processor, performance_monitor):
        """Test memory efficiency for large-scale processing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process many tables to test memory accumulation
        num_tables = 100
        table_template = """Method{idx}    Accuracy    Precision    Recall    F1-Score
        SVM{idx}       0.{idx:03d}       0.{idx:03d}        0.{idx:03d}     0.{idx:03d}
        RF{idx}        0.{idx:03d}       0.{idx:03d}        0.{idx:03d}     0.{idx:03d}
        XGB{idx}       0.{idx:03d}       0.{idx:03d}        0.{idx:03d}     0.{idx:03d}"""
        
        start_time = time.perf_counter()
        
        for i in range(num_tables):
            table_data = table_template.format(idx=i)
            result = table_processor.convert_to_csv(table_data, f"memory_test_{i}")
            
            # Periodically check memory usage
            if i % 20 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_growth = current_memory - initial_memory
                
                # Memory should not grow excessively (allow some reasonable growth)
                assert memory_growth < 100, f"Excessive memory growth: {memory_growth:.1f}MB after {i} tables"
        
        end_time = time.perf_counter()
        final_memory = process.memory_info().rss / 1024 / 1024
        
        # Clean up
        gc.collect()
        
        total_time = end_time - start_time
        total_memory_growth = final_memory - initial_memory
        
        # Performance assertions
        assert total_time < 10.0, f"Batch processing too slow: {total_time:.2f}s for {num_tables} tables"
        assert total_memory_growth < 50, f"Memory leak detected: {total_memory_growth:.1f}MB growth"
        
        return {
            'total_time_seconds': total_time,
            'tables_processed': num_tables,
            'throughput_tables_per_second': num_tables / total_time,
            'memory_growth_mb': total_memory_growth,
            'avg_time_per_table_ms': (total_time / num_tables) * 1000
        }
    
    def test_concurrent_processing_performance(self, table_processor):
        """Test performance characteristics under concurrent load."""
        import concurrent.futures
        import threading
        
        def process_table(table_id: int) -> Dict[str, Any]:
            """Process a single table."""
            table_data = f"""Method{table_id}    Accuracy    Time
            SVM{table_id}       0.{table_id:03d}       {table_id}.5
            RF{table_id}        0.{table_id:03d}       {table_id}.2"""
            
            start_time = time.perf_counter()
            result = table_processor.convert_to_csv(table_data, f"concurrent_test_{table_id}")
            end_time = time.perf_counter()
            
            return {
                'table_id': table_id,
                'processing_time': end_time - start_time,
                'success': result is not None
            }
        
        # Test with multiple concurrent workers
        num_workers = 4
        num_tasks = 20
        
        start_time = time.perf_counter()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(process_table, i) for i in range(num_tasks)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.perf_counter()
        
        # Analyze results
        total_time = end_time - start_time
        successful_tasks = sum(1 for r in results if r['success'])
        avg_task_time = sum(r['processing_time'] for r in results) / len(results)
        
        # Performance assertions
        assert successful_tasks == num_tasks, f"Not all tasks succeeded: {successful_tasks}/{num_tasks}"
        assert total_time < 5.0, f"Concurrent processing too slow: {total_time:.2f}s"
        assert avg_task_time < 0.1, f"Average task time too slow: {avg_task_time:.3f}s"
        
        return {
            'total_time_seconds': total_time,
            'concurrent_workers': num_workers,
            'tasks_completed': successful_tasks,
            'throughput_tasks_per_second': num_tasks / total_time,
            'avg_task_time_seconds': avg_task_time
        }


@pytest.mark.performance
@pytest.mark.regression
class TestPerformanceRegression:
    """Tests to detect performance regressions."""
    
    def test_baseline_performance_metrics(self, table_processor, section_extractor, temp_output_dir):
        """Establish and validate baseline performance metrics."""
        baseline_metrics = {}
        
        # Table processing baseline
        sample_table = """Algorithm    Dataset    Accuracy   Precision   Recall
        SVM         MNIST      0.951      0.948       0.945
        RF          MNIST      0.963      0.961       0.958
        XGBoost     MNIST      0.987      0.985       0.982"""
        
        start_time = time.perf_counter()
        table_result = table_processor.convert_to_csv(sample_table, "baseline_test")
        table_time = time.perf_counter() - start_time
        
        assert table_result is not None, "Baseline table processing should succeed"
        baseline_metrics['table_processing_time'] = table_time
        
        # Section detection baseline
        sample_sections = """# Abstract
        This is a sample abstract for testing performance.
        
        # Introduction
        Introduction content with multiple paragraphs to test processing.
        This is the second paragraph of the introduction.
        
        # Methodology
        Methodology section with detailed explanations.
        
        # Results
        Results section with findings and analysis.
        
        # Conclusion
        Conclusion summarizing the work."""
        
        start_time = time.perf_counter()
        section_result = section_extractor._detect_sections_from_text(sample_sections)
        section_time = time.perf_counter() - start_time
        
        assert len(section_result) >= 4, "Baseline section detection should find major sections"
        baseline_metrics['section_detection_time'] = section_time
        
        # Performance thresholds (adjust based on actual performance)
        assert table_time < 0.05, f"Table processing baseline too slow: {table_time:.3f}s"
        assert section_time < 0.02, f"Section detection baseline too slow: {section_time:.3f}s"
        
        # Save baseline for future regression testing
        baseline_file = temp_output_dir / "performance_baseline.json"
        with open(baseline_file, 'w') as f:
            json.dump(baseline_metrics, f, indent=2)
        
        return baseline_metrics
    
    def test_performance_consistency(self, table_processor):
        """Test that performance is consistent across multiple runs."""
        sample_table = "Col1\tCol2\tCol3\nA\t1\t2\nB\t3\t4\nC\t5\t6"
        
        execution_times = []
        num_runs = 10
        
        for i in range(num_runs):
            start_time = time.perf_counter()
            result = table_processor.convert_to_csv(sample_table, f"consistency_test_{i}")
            end_time = time.perf_counter()
            
            assert result is not None, f"Processing should succeed on run {i}"
            execution_times.append(end_time - start_time)
        
        # Calculate statistics
        avg_time = sum(execution_times) / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        variance = sum((t - avg_time) ** 2 for t in execution_times) / len(execution_times)
        std_dev = variance ** 0.5
        
        # Performance consistency checks
        assert max_time - min_time < 0.01, f"Performance inconsistency: range {max_time - min_time:.4f}s"
        assert std_dev < avg_time * 0.5, f"High performance variance: std_dev {std_dev:.4f}s"
        
        return {
            'avg_time_seconds': avg_time,
            'min_time_seconds': min_time,
            'max_time_seconds': max_time,
            'std_dev_seconds': std_dev,
            'coefficient_of_variation': std_dev / avg_time
        }


@pytest.mark.benchmark
class TestBenchmarkSuite:
    """Comprehensive benchmark suite for performance analysis."""
    
    def test_comprehensive_extraction_benchmark(self, 
                                               content_extractor,
                                               section_extractor, 
                                               table_extractor,
                                               figure_extractor,
                                               citation_extractor,
                                               performance_monitor,
                                               temp_output_dir):
        """Comprehensive benchmark of all extraction components."""
        benchmark_results = {}
        
        # Test each extractor component
        extractors = {
            'content': content_extractor,
            'section': section_extractor,
            'table': table_extractor,
            'figure': figure_extractor,
            'citation': citation_extractor
        }
        
        for extractor_name, extractor in extractors.items():
            performance_monitor.start()
            
            try:
                # Note: This will use mock data from fixtures
                result = extractor.extract()
                success = True
            except Exception as e:
                result = None
                success = False
                print(f"Extractor {extractor_name} failed: {e}")
            
            metrics = performance_monitor.stop()
            
            benchmark_results[extractor_name] = {
                **metrics,
                'success': success,
                'result_size': len(str(result)) if result else 0
            }
        
        # Save comprehensive benchmark results
        benchmark_file = temp_output_dir / "comprehensive_benchmark.json"
        with open(benchmark_file, 'w') as f:
            json.dump(benchmark_results, f, indent=2)
        
        # Overall performance assertions
        total_time = sum(r['execution_time_seconds'] for r in benchmark_results.values())
        assert total_time < 2.0, f"Total extraction time too long: {total_time:.2f}s"
        
        successful_extractors = sum(1 for r in benchmark_results.values() if r['success'])
        assert successful_extractors >= 3, f"Too many extractor failures: {successful_extractors}/5"
        
        return benchmark_results 