"""
Regression tests for section detection functionality.

Ensures that section detection quality doesn't degrade from current high performance.
Tests section pattern recognition, markdown formatting, and extraction accuracy.
"""

import pytest
from typing import Dict, Any, List


@pytest.mark.regression
@pytest.mark.section_detection
class TestSectionDetectionRegression:
    """Regression tests for section detection to maintain quality."""
    
    def test_maintains_section_count_quality(self, section_extractor, sample_section_text):
        """Ensure section detection continues to find expected number of sections."""
        # Mock the PDF document to return our sample text
        with pytest.mock.patch.object(section_extractor, '_extract_page_text_robust') as mock_extract:
            mock_extract.return_value = sample_section_text
            
            with pytest.mock.patch.object(section_extractor, '_open_document') as mock_open:
                mock_doc = pytest.mock.Mock()
                mock_doc.page_count = 1
                mock_open.return_value = mock_doc
                
                results = section_extractor.extract()
        
        assert 'sections' in results
        sections = results['sections']
        
        # Should detect all major sections
        expected_sections = {
            'abstract', 'introduction', 'methodology', 'results', 
            'conclusion', 'references'
        }
        
        found_sections = set(sections.keys())
        major_sections_found = len(found_sections.intersection(expected_sections))
        
        # Should find at least 5 of the 6 major sections (allows for some variation)
        assert major_sections_found >= 5, \
            f"Section detection regression: found {major_sections_found} major sections, expected ≥5"
        
        # Total section count should be reasonable (including subsections)
        assert len(sections) >= 5, \
            f"Total section count regression: found {len(sections)}, expected ≥5"
    
    def test_maintains_section_pattern_recognition(self, section_extractor):
        """Ensure section pattern recognition remains accurate."""
        test_patterns = [
            ("# Abstract", "abstract"),
            ("## Introduction", "introduction"), 
            ("### Methodology", "methodology"),
            ("# 1. Introduction", "introduction"),
            ("## 2.1 Data Preprocessing", "data_preprocessing"),
            ("# Results and Discussion", "results_and_discussion"),
            ("## Conclusion", "conclusion"),
            ("# References", "references"),
            ("## Bibliography", "bibliography"),
        ]
        
        for pattern, expected_key in test_patterns:
            # Test that pattern is recognized
            sections = section_extractor._detect_sections_from_text(f"{pattern}\n\nSample content here.")
            
            # Should detect at least one section
            assert len(sections) >= 1, f"Failed to detect section from pattern: {pattern}"
            
            # The detected section key should be reasonable
            detected_keys = list(sections.keys())
            assert any(expected_key.lower() in key.lower() or key.lower() in expected_key.lower() 
                      for key in detected_keys), \
                f"Pattern recognition regression for {pattern}: expected key containing '{expected_key}', got {detected_keys}"
    
    def test_maintains_content_extraction_quality(self, section_extractor, sample_section_text):
        """Ensure section content extraction maintains quality."""
        with pytest.mock.patch.object(section_extractor, '_extract_page_text_robust') as mock_extract:
            mock_extract.return_value = sample_section_text
            
            with pytest.mock.patch.object(section_extractor, '_open_document') as mock_open:
                mock_doc = pytest.mock.Mock()
                mock_doc.page_count = 1
                mock_open.return_value = mock_doc
                
                results = section_extractor.extract()
        
        sections = results['sections']
        
        # Check that content is extracted properly
        for section_name, content in sections.items():
            assert isinstance(content, str), f"Section {section_name} content should be string"
            assert len(content.strip()) > 0, f"Section {section_name} should have non-empty content"
            
            # Content should not include the section header itself
            assert not content.strip().startswith('#'), f"Section {section_name} content should not include header"
        
        # Specific content checks for known sections
        if 'abstract' in sections:
            abstract_content = sections['abstract'].lower()
            assert 'novel approach' in abstract_content or 'machine learning' in abstract_content, \
                "Abstract content extraction regression"
        
        if 'introduction' in sections:
            intro_content = sections['introduction'].lower()
            assert 'machine learning' in intro_content or 'important' in intro_content, \
                "Introduction content extraction regression"
    
    def test_maintains_markdown_formatting_quality(self, section_extractor):
        """Ensure markdown formatting for sections remains consistent."""
        test_content = """
        # Abstract
        
        This is the abstract content with important information.
        
        # Introduction
        
        Introduction content here with multiple sentences.
        The second sentence continues the thought.
        
        ## Subsection
        
        Subsection content that should be properly handled.
        """
        
        sections = section_extractor._detect_sections_from_text(test_content)
        
        # Should properly handle different heading levels
        assert len(sections) >= 2, "Should detect multiple sections with different heading levels"
        
        # Content should be clean (no extra whitespace)
        for section_name, content in sections.items():
            lines = content.strip().split('\n')
            # No line should be just whitespace
            assert not any(line.strip() == '' for line in lines if line), \
                f"Section {section_name} contains unnecessary whitespace lines"
    
    def test_maintains_nested_section_handling(self, section_extractor):
        """Ensure nested sections (subsections) are handled properly."""
        nested_content = """
        # Main Section
        
        Main section content here.
        
        ## Subsection 1
        
        First subsection content.
        
        ### Sub-subsection
        
        Deep nested content.
        
        ## Subsection 2
        
        Second subsection content.
        
        # Another Main Section
        
        Another main section.
        """
        
        sections = section_extractor._detect_sections_from_text(nested_content)
        
        # Should detect multiple sections including nested ones
        assert len(sections) >= 4, f"Should detect nested sections, found {len(sections)}"
        
        # Section names should reflect hierarchy
        section_names = list(sections.keys())
        has_subsections = any('subsection' in name.lower() for name in section_names)
        assert has_subsections, "Should detect subsections in nested content"


@pytest.mark.unit
@pytest.mark.section_detection  
class TestSectionDetectionUnit:
    """Unit tests for section detection components."""
    
    def test_section_pattern_matching(self, section_extractor):
        """Test individual section pattern matching."""
        # Test that all expected patterns are recognized
        patterns_to_test = [
            "# Introduction",
            "## 2. Methodology", 
            "### 3.1 Data Collection",
            "#### Subsection",
            "Abstract",
            "INTRODUCTION",
            "1. Background",
            "2.1. Related Work"
        ]
        
        for pattern in patterns_to_test:
            test_text = f"{pattern}\n\nSome content here."
            sections = section_extractor._detect_sections_from_text(test_text)
            assert len(sections) >= 1, f"Failed to detect section from pattern: {pattern}"
    
    def test_content_cleaning(self, section_extractor):
        """Test that section content is properly cleaned."""
        messy_content = """
        # Test Section
        
        
        This is content with    extra    spaces.
        
        
        And multiple empty lines.
        
        
        
        More content here.
        """
        
        sections = section_extractor._detect_sections_from_text(messy_content)
        
        if sections:
            for section_name, content in sections.items():
                # Content should not have excessive whitespace
                lines = content.split('\n')
                consecutive_empty = 0
                max_consecutive_empty = 0
                
                for line in lines:
                    if line.strip() == '':
                        consecutive_empty += 1
                        max_consecutive_empty = max(max_consecutive_empty, consecutive_empty)
                    else:
                        consecutive_empty = 0
                
                assert max_consecutive_empty <= 2, \
                    f"Section {section_name} has too many consecutive empty lines: {max_consecutive_empty}"
    
    def test_special_character_handling(self, section_extractor):
        """Test handling of special characters in section headers and content."""
        special_content = """
        # Introduction & Background
        
        Content with special characters: α, β, γ, and equations like E=mc².
        
        ## Results & Discussion
        
        More content with symbols: ±, ≤, ≥, →, ∈, ∑.
        
        ### Section with "Quotes"
        
        Content with quotes and other punctuation!
        """
        
        sections = section_extractor._detect_sections_from_text(special_content)
        
        # Should handle special characters without errors
        assert len(sections) >= 2, "Should detect sections with special characters"
        
        for section_name, content in sections.items():
            # Content should preserve special characters
            assert len(content) > 0, f"Section {section_name} should have content"
            # Should not crash on special characters
            assert isinstance(content, str), f"Section {section_name} content should be string"


@pytest.mark.performance
@pytest.mark.section_detection
class TestSectionDetectionPerformance:
    """Performance tests for section detection."""
    
    def test_section_detection_performance(self, section_extractor, performance_monitor, benchmark_data):
        """Test that section detection maintains reasonable performance."""
        performance_monitor.start()
        
        # Test with medium-sized document
        large_content = f"""
        # Abstract
        {benchmark_data['medium_document']}
        
        # Introduction  
        {benchmark_data['medium_document']}
        
        # Methodology
        {benchmark_data['medium_document']}
        
        # Results
        {benchmark_data['medium_document']}
        
        # Conclusion
        {benchmark_data['medium_document']}
        """
        
        sections = section_extractor._detect_sections_from_text(large_content)
        
        metrics = performance_monitor.stop()
        
        # Performance requirements
        assert metrics['execution_time_seconds'] < 5.0, \
            f"Section detection too slow: {metrics['execution_time_seconds']:.2f}s"
        
        assert len(sections) >= 5, "Should detect expected number of sections even with large content"
    
    @pytest.mark.slow
    def test_large_document_handling(self, section_extractor, benchmark_data):
        """Test section detection with very large documents."""
        # Create a large document with many sections
        large_doc_parts = []
        for i in range(20):
            large_doc_parts.append(f"# Section {i+1}")
            large_doc_parts.append(benchmark_data['small_document'])  # 1KB per section
        
        large_document = "\n\n".join(large_doc_parts)
        
        sections = section_extractor._detect_sections_from_text(large_document)
        
        # Should handle large documents without crashing
        assert len(sections) >= 15, f"Should detect most sections in large document, found {len(sections)}"
        
        # Memory usage should be reasonable (not testing exact values due to variability)
        assert isinstance(sections, dict), "Should return proper data structure" 