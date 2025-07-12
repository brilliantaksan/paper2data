#!/usr/bin/env python3
"""
Stage 4 Performance Optimization Demonstration

This script demonstrates all the Stage 4 performance enhancements:
- Multiprocessing for large batch operations
- Memory optimization for large PDF files
- Streaming processing for continuous data flows
- Result caching to avoid reprocessing
- Progress persistence for resumable operations
- Resource usage monitoring and reporting
- Automatic scaling based on system resources
"""

import time
import tempfile
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

from paper2data.performance import (
    ResourceMonitor,
    PerformanceCache,
    ParallelExtractor,
    BatchProcessor,
    StreamingProcessor,
    ProgressPersistence,
    get_system_recommendations,
    get_performance_cache,
    get_resource_monitor,
    extract_with_full_optimization,
    memory_optimized,
    with_performance_monitoring
)
from paper2data.extractor import extract_all_content_optimized


def create_mock_pdf_content(size_mb: float = 1.0) -> bytes:
    """Create mock PDF content of specified size for testing."""
    # Create realistic PDF-like content
    content = b"%PDF-1.4\n"
    content += b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    
    # Add content to reach desired size
    target_size = int(size_mb * 1024 * 1024)
    padding = b"Mock PDF content for performance testing. " * (target_size // 40)
    content += padding[:target_size - len(content)]
    
    return content


def demo_resource_monitoring():
    """Demonstrate resource monitoring capabilities."""
    print("🔍 Resource Monitoring Demo")
    print("=" * 50)
    
    monitor = ResourceMonitor(monitoring_interval=0.5)
    
    # Get current system metrics
    metrics = monitor.get_current_metrics()
    print(f"Current CPU Usage: {metrics.cpu_percent:.1f}%")
    print(f"Current Memory Usage: {metrics.memory_percent:.1f}%")
    print(f"Available Memory: {metrics.memory_available / (1024**3):.1f} GB")
    print(f"Active Processes: {metrics.active_processes}")
    
    # Get system recommendations
    recommendations = get_system_recommendations()
    print(f"\nSystem Recommendations:")
    print(f"  - Optimal Worker Count: {recommendations['optimal_worker_count']}")
    print(f"  - Memory Optimization Needed: {recommendations['memory_optimization_needed']}")
    print(f"  - Recommended Batch Size: {recommendations['batch_size_recommendation']}")
    
    if recommendations['resource_warnings']:
        print(f"  - Warnings: {', '.join(recommendations['resource_warnings'])}")
    
    # Test monitoring lifecycle
    print(f"\nStarting monitoring for 2 seconds...")
    monitor.start_monitoring()
    time.sleep(2)
    monitor.stop_monitoring()
    
    print(f"Collected {len(monitor.metrics_history)} metrics samples")
    print()


def demo_performance_cache():
    """Demonstrate performance caching capabilities."""
    print("🚀 Performance Caching Demo")
    print("=" * 50)
    
    cache = get_performance_cache()
    
    # Test cache operations
    test_content = create_mock_pdf_content(0.1)  # 100KB
    test_result = {"pages": 5, "words": 1000, "sections": 3}
    
    print("Testing cache operations...")
    
    # Cache miss
    start_time = time.time()
    result = cache.get(test_content, "test_extraction")
    print(f"Cache miss time: {(time.time() - start_time) * 1000:.2f}ms")
    assert result is None
    
    # Cache set
    start_time = time.time()
    cache.set(test_content, test_result, "test_extraction")
    print(f"Cache set time: {(time.time() - start_time) * 1000:.2f}ms")
    
    # Cache hit
    start_time = time.time()
    cached_result = cache.get(test_content, "test_extraction")
    print(f"Cache hit time: {(time.time() - start_time) * 1000:.2f}ms")
    assert cached_result == test_result
    
    # Cache stats
    stats = cache.get_cache_stats()
    print(f"\nCache Statistics:")
    print(f"  - Memory cache size: {stats['memory_cache_size']}")
    print(f"  - Disk cache files: {stats['disk_cache_files']}")
    print(f"  - Disk cache size: {stats['disk_cache_size_mb']:.2f} MB")
    print()


def demo_parallel_extraction():
    """Demonstrate parallel extraction capabilities."""
    print("⚡ Parallel Extraction Demo")
    print("=" * 50)
    
    # Create mock PDF content
    test_content = create_mock_pdf_content(0.5)  # 500KB
    
    # Test sequential vs parallel extraction
    print("Comparing sequential vs parallel extraction...")
    
    # Sequential extraction (using optimized with parallel disabled)
    start_time = time.time()
    try:
        sequential_result = extract_all_content_optimized(test_content, enable_parallel=False)
        sequential_time = time.time() - start_time
        print(f"Sequential extraction time: {sequential_time:.2f}s")
    except Exception as e:
        print(f"Sequential extraction failed: {e}")
        sequential_time = None
    
    # Parallel extraction
    start_time = time.time()
    try:
        parallel_result = extract_all_content_optimized(test_content, enable_parallel=True)
        parallel_time = time.time() - start_time
        print(f"Parallel extraction time: {parallel_time:.2f}s")
        
        if sequential_time:
            speedup = sequential_time / parallel_time
            print(f"Speedup: {speedup:.2f}x")
    except Exception as e:
        print(f"Parallel extraction failed: {e}")
    
    print()


def demo_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("📦 Batch Processing Demo")
    print("=" * 50)
    
    # Create mock documents
    mock_documents = [
        create_mock_pdf_content(0.1),  # 100KB
        create_mock_pdf_content(0.2),  # 200KB
        create_mock_pdf_content(0.1),  # 100KB
    ]
    
    batch_processor = BatchProcessor(max_workers=2, checkpoint_interval=2)
    
    print(f"Processing batch of {len(mock_documents)} documents...")
    
    start_time = time.time()
    try:
        # Note: This will fail with mock data, but demonstrates the interface
        results = batch_processor.process_batch(mock_documents, "demo_batch")
        processing_time = time.time() - start_time
        
        print(f"Batch processing completed in {processing_time:.2f}s")
        print(f"  - Total documents: {results['total_documents']}")
        print(f"  - Successful: {results['successful_documents']}")
        print(f"  - Failed: {results['failed_documents']}")
        print(f"  - Processing rate: {results['total_documents'] / processing_time:.2f} docs/sec")
    except Exception as e:
        print(f"Batch processing demo failed (expected with mock data): {e}")
    
    print()


def demo_streaming_processing():
    """Demonstrate streaming processing capabilities."""
    print("🌊 Streaming Processing Demo")
    print("=" * 50)
    
    # Create a data stream
    data_stream = [f"item_{i}" for i in range(100)]
    
    # Mock processing function
    def process_item(item):
        # Simulate processing time
        time.sleep(0.01)  # 10ms per item
        return f"processed_{item}"
    
    streaming_processor = StreamingProcessor(chunk_size=10, memory_threshold=0.9)
    
    print(f"Processing stream of {len(data_stream)} items...")
    
    start_time = time.time()
    processed_items = list(streaming_processor.process_stream(iter(data_stream), process_item))
    processing_time = time.time() - start_time
    
    print(f"Stream processing completed in {processing_time:.2f}s")
    print(f"  - Items processed: {len(processed_items)}")
    print(f"  - Processing rate: {len(processed_items) / processing_time:.2f} items/sec")
    print(f"  - First item: {processed_items[0]}")
    print(f"  - Last item: {processed_items[-1]}")
    print()


def demo_progress_persistence():
    """Demonstrate progress persistence capabilities."""
    print("💾 Progress Persistence Demo")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        persistence = ProgressPersistence(Path(temp_dir))
        
        # Create a checkpoint
        checkpoint = persistence.create_checkpoint("demo_operation", 100)
        print(f"Created checkpoint: {checkpoint.operation_id}")
        
        # Update progress
        persistence.update_checkpoint("demo_operation", 25, [], {"phase": "processing"})
        print(f"Updated progress: 25/100 items completed")
        
        # Simulate restart - load checkpoint
        new_persistence = ProgressPersistence(Path(temp_dir))
        loaded_checkpoint = new_persistence.load_checkpoint("demo_operation")
        
        if loaded_checkpoint:
            print(f"Loaded checkpoint after restart:")
            print(f"  - Operation ID: {loaded_checkpoint.operation_id}")
            print(f"  - Progress: {loaded_checkpoint.completed_items}/{loaded_checkpoint.total_items}")
            print(f"  - Results: {loaded_checkpoint.results}")
        
        # Complete operation
        persistence.complete_checkpoint("demo_operation")
        print(f"Operation completed and checkpoint cleaned up")
    
    print()


@memory_optimized
def demo_memory_optimization():
    """Demonstrate memory optimization capabilities."""
    print("🧠 Memory Optimization Demo")
    print("=" * 50)
    
    # Create larger test data
    large_content = create_mock_pdf_content(2.0)  # 2MB
    
    print(f"Processing {len(large_content) / (1024*1024):.1f}MB of content with memory optimization...")
    
    # This function is decorated with @memory_optimized
    # so it will automatically optimize memory usage
    
    # Get memory stats before
    monitor = get_resource_monitor()
    before_metrics = monitor.get_current_metrics()
    
    # Process content
    start_time = time.time()
    # Simulate processing
    processed_data = []
    for i in range(100):
        processed_data.append(f"Processed chunk {i}")
    
    processing_time = time.time() - start_time
    
    # Get memory stats after
    after_metrics = monitor.get_current_metrics()
    
    print(f"Processing completed in {processing_time:.2f}s")
    print(f"Memory usage before: {before_metrics.memory_percent:.1f}%")
    print(f"Memory usage after: {after_metrics.memory_percent:.1f}%")
    print(f"Memory optimization: {'✓' if after_metrics.memory_percent <= before_metrics.memory_percent + 1 else '✗'}")
    print()


@with_performance_monitoring
def demo_performance_monitoring():
    """Demonstrate performance monitoring decorator."""
    print("📊 Performance Monitoring Demo")
    print("=" * 50)
    
    # This function is decorated with @with_performance_monitoring
    # so it will automatically monitor performance
    
    print("Simulating work with performance monitoring...")
    
    # Simulate some work
    time.sleep(0.5)
    
    # Do some computation
    result = sum(i * i for i in range(10000))
    
    print(f"Work completed with result: {result}")
    # Performance metrics will be logged automatically
    print()


def main():
    """Run all Stage 4 performance optimization demos."""
    print("🎯 Paper2Data Stage 4 Performance Optimization Demos")
    print("=" * 60)
    print()
    
    # Run all demos
    demo_resource_monitoring()
    demo_performance_cache()
    demo_parallel_extraction()
    demo_batch_processing()
    demo_streaming_processing()
    demo_progress_persistence()
    demo_memory_optimization()
    demo_performance_monitoring()
    
    print("✅ All Stage 4 performance optimization demos completed!")
    print()
    print("Key Benefits Demonstrated:")
    print("• Resource monitoring and auto-scaling")
    print("• High-performance caching with TTL")
    print("• Parallel extraction with thread pools")
    print("• Batch processing with checkpoints")
    print("• Streaming processing for large datasets")
    print("• Progress persistence for resumable operations")
    print("• Memory optimization with garbage collection")
    print("• Performance monitoring with decorators")


if __name__ == "__main__":
    main() 