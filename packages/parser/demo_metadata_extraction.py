#!/usr/bin/env python3
"""
Demo script for Enhanced Metadata Extraction in Paper2Data

This script demonstrates the comprehensive metadata extraction capabilities
including title, authors, abstract, keywords, DOI, publication info, and more.
"""

import os
import sys
import tempfile
import json
from datetime import datetime
from typing import Dict, Any

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from paper2data.metadata_extractor import (
    MetadataExtractor, EnhancedMetadata, Author, PublicationInfo, Citation,
    PaperType, PublicationStatus, extract_metadata, export_metadata
)

def create_sample_pdf_content() -> str:
    """Create sample PDF-like text content for demonstration"""
    return """
    Machine Learning Applications in Healthcare: A Comprehensive Survey
    
    John Doe¹, Jane Smith², Michael Johnson¹
    
    ¹MIT Computer Science and Artificial Intelligence Laboratory
    ²Harvard Medical School
    
    Corresponding Author: john.doe@mit.edu
    ORCID: 0000-0000-0000-0001 (John Doe)
    
    Abstract: This paper presents a comprehensive survey of machine learning techniques 
    applied to healthcare applications. We analyze various approaches including supervised 
    learning, unsupervised learning, and reinforcement learning methods. Our analysis 
    covers applications in medical imaging, drug discovery, personalized medicine, 
    and clinical decision support systems. The results demonstrate significant improvements 
    in accuracy and efficiency compared to traditional methods.
    
    Keywords: machine learning, healthcare, artificial intelligence, medical imaging, 
    drug discovery, personalized medicine
    
    DOI: 10.1234/journal.ml.healthcare.2023.001
    
    1. Introduction
    
    Machine learning has emerged as a transformative technology in healthcare, 
    offering unprecedented opportunities to improve patient outcomes and clinical 
    decision-making processes.
    
    2. Literature Review
    
    Previous work in this area has focused on specific applications...
    
    3. Methodology
    
    We conducted a systematic review of machine learning applications...
    
    4. Results
    
    Our analysis reveals several key findings...
    
    5. Discussion
    
    The implications of these findings are significant...
    
    6. Conclusion
    
    This survey provides a comprehensive overview of machine learning in healthcare...
    
    Acknowledgments
    
    We thank the reviewers for their valuable feedback.
    
    References
    
    [1] Smith, J., Brown, A. (2020). "Deep Learning in Medical Imaging". 
        Nature Medicine, 26(8), 1234-1245. doi:10.1038/s41591-020-0842-3
    
    [2] Johnson, M., Williams, R. (2021). "AI-Driven Drug Discovery: 
        Current State and Future Prospects". Cell, 184(6), 1617-1635. 
        doi:10.1016/j.cell.2021.02.047
    
    [3] Davis, L., Wilson, K. (2022). "Personalized Medicine Through 
        Machine Learning: A Review". New England Journal of Medicine, 
        386(4), 354-362. doi:10.1056/NEJMra2104356
    
    [4] Taylor, S., Anderson, P. (2023). "Clinical Decision Support Systems 
        Enhanced by AI". The Lancet Digital Health, 5(3), e156-e167. 
        doi:10.1016/S2589-7500(23)00028-1
    
    Published in: Journal of Medical AI, Volume 15, Issue 3, 2023
    Pages: 123-145
    Publisher: Medical AI Press
    """

def demonstrate_basic_functionality():
    """Demonstrate basic metadata extraction functionality"""
    print("=" * 80)
    print("ENHANCED METADATA EXTRACTION DEMO")
    print("=" * 80)
    
    # Create metadata extractor
    extractor = MetadataExtractor()
    print(f"✓ Created MetadataExtractor instance")
    
    # Test individual component extraction
    sample_text = create_sample_pdf_content()
    
    print("\n1. TITLE EXTRACTION")
    print("-" * 50)
    title = extractor._extract_title(sample_text)
    print(f"Extracted Title: '{title}'")
    print(f"Title Confidence: {extractor._calculate_title_confidence(title):.2f}")
    
    print("\n2. ABSTRACT EXTRACTION")
    print("-" * 50)
    abstract = extractor._extract_abstract(sample_text)
    print(f"Extracted Abstract: '{abstract[:100]}...'")
    print(f"Abstract Length: {len(abstract)} characters")
    print(f"Abstract Confidence: {extractor._calculate_abstract_confidence(abstract):.2f}")
    
    print("\n3. AUTHOR EXTRACTION")
    print("-" * 50)
    authors = extractor._extract_authors(sample_text)
    print(f"Number of Authors: {len(authors)}")
    for i, author in enumerate(authors, 1):
        print(f"  Author {i}: {author.name}")
        if author.email:
            print(f"    Email: {author.email}")
        if author.orcid:
            print(f"    ORCID: {author.orcid}")
        if author.affiliations:
            print(f"    Affiliations: {', '.join(author.affiliations)}")
    print(f"Author Confidence: {extractor._calculate_author_confidence(authors):.2f}")
    
    print("\n4. KEYWORDS EXTRACTION")
    print("-" * 50)
    keywords = extractor._extract_keywords(sample_text)
    print(f"Keywords: {', '.join(keywords)}")
    print(f"Number of Keywords: {len(keywords)}")
    
    print("\n5. DOI EXTRACTION")
    print("-" * 50)
    doi = extractor._extract_doi(sample_text)
    print(f"DOI: {doi}")
    
    print("\n6. PUBLICATION INFO EXTRACTION")
    print("-" * 50)
    pub_info = extractor._extract_publication_info(sample_text)
    print(f"Journal: {pub_info.journal}")
    print(f"Year: {pub_info.year}")
    print(f"Volume: {pub_info.volume}")
    print(f"Publisher: {pub_info.publisher}")
    
    print("\n7. CITATION EXTRACTION")
    print("-" * 50)
    citations = extractor._extract_citations(sample_text)
    print(f"Number of Citations: {len(citations)}")
    for i, citation in enumerate(citations, 1):
        print(f"  Citation {i}:")
        print(f"    Authors: {', '.join(citation.authors)}")
        print(f"    Title: {citation.title}")
        print(f"    Year: {citation.year}")
        print(f"    DOI: {citation.doi}")
    
    print("\n8. SUBJECT CATEGORIES")
    print("-" * 50)
    categories = extractor._extract_subject_categories(sample_text)
    print(f"Subject Categories: {', '.join(categories)}")
    
    print("\n9. PAPER TYPE DETERMINATION")
    print("-" * 50)
    metadata = EnhancedMetadata(title=title, abstract=abstract)
    metadata.publication_info = pub_info
    paper_type = extractor._determine_paper_type(sample_text, metadata)
    print(f"Paper Type: {paper_type.value}")

def demonstrate_full_extraction():
    """Demonstrate full metadata extraction with mock PDF"""
    print("\n" + "=" * 80)
    print("FULL METADATA EXTRACTION DEMO")
    print("=" * 80)
    
    # Create a temporary PDF-like file for demonstration
    sample_text = create_sample_pdf_content()
    
    # Create mock metadata for comprehensive demonstration
    metadata = EnhancedMetadata(
        title="Machine Learning Applications in Healthcare: A Comprehensive Survey",
        abstract="This paper presents a comprehensive survey of machine learning techniques applied to healthcare applications. We analyze various approaches including supervised learning, unsupervised learning, and reinforcement learning methods.",
        authors=[
            Author(
                name="John Doe",
                position=1,
                email="john.doe@mit.edu",
                orcid="0000-0000-0000-0001",
                affiliations=["MIT Computer Science and Artificial Intelligence Laboratory"],
                is_corresponding=True
            ),
            Author(
                name="Jane Smith",
                position=2,
                affiliations=["Harvard Medical School"]
            ),
            Author(
                name="Michael Johnson",
                position=3,
                affiliations=["MIT Computer Science and Artificial Intelligence Laboratory"]
            )
        ],
        keywords=["machine learning", "healthcare", "artificial intelligence", "medical imaging", "drug discovery", "personalized medicine"],
        doi="10.1234/journal.ml.healthcare.2023.001",
        publication_info=PublicationInfo(
            journal="Journal of Medical AI",
            year=2023,
            volume="15",
            issue="3",
            pages="123-145",
            publisher="Medical AI Press"
        ),
        citations=[
            Citation(
                text="Smith, J., Brown, A. (2020). \"Deep Learning in Medical Imaging\". Nature Medicine, 26(8), 1234-1245.",
                authors=["J. Smith", "A. Brown"],
                title="Deep Learning in Medical Imaging",
                year=2020,
                journal="Nature Medicine",
                doi="10.1038/s41591-020-0842-3",
                position=1
            ),
            Citation(
                text="Johnson, M., Williams, R. (2021). \"AI-Driven Drug Discovery: Current State and Future Prospects\". Cell, 184(6), 1617-1635.",
                authors=["M. Johnson", "R. Williams"],
                title="AI-Driven Drug Discovery: Current State and Future Prospects",
                year=2021,
                journal="Cell",
                doi="10.1016/j.cell.2021.02.047",
                position=2
            )
        ],
        subject_categories=["Machine Learning", "Artificial Intelligence", "Medicine", "Computer Science"],
        paper_type=PaperType.JOURNAL_ARTICLE,
        publication_status=PublicationStatus.PUBLISHED,
        page_count=23,
        word_count=8542,
        language="en",
        title_confidence=0.95,
        abstract_confidence=0.88,
        author_confidence=0.92,
        extraction_date=datetime.now()
    )
    
    print("\n1. COMPREHENSIVE METADATA OVERVIEW")
    print("-" * 50)
    print(f"Title: {metadata.title}")
    print(f"Paper Type: {metadata.paper_type.value}")
    print(f"Publication Status: {metadata.publication_status.value}")
    print(f"DOI: {metadata.doi}")
    print(f"Page Count: {metadata.page_count}")
    print(f"Word Count: {metadata.word_count:,}")
    print(f"Language: {metadata.language}")
    
    print("\n2. AUTHORS INFORMATION")
    print("-" * 50)
    for author in metadata.authors:
        print(f"• {author.name} (Position: {author.position})")
        if author.email:
            print(f"  Email: {author.email}")
        if author.orcid:
            print(f"  ORCID: {author.orcid}")
        if author.affiliations:
            print(f"  Affiliations: {', '.join(author.affiliations)}")
        if author.is_corresponding:
            print(f"  ✓ Corresponding Author")
    
    print("\n3. PUBLICATION INFORMATION")
    print("-" * 50)
    pub_info = metadata.publication_info
    print(f"Journal: {pub_info.journal}")
    print(f"Year: {pub_info.year}")
    print(f"Volume: {pub_info.volume}")
    print(f"Issue: {pub_info.issue}")
    print(f"Pages: {pub_info.pages}")
    print(f"Publisher: {pub_info.publisher}")
    
    print("\n4. ABSTRACT")
    print("-" * 50)
    print(f"Abstract: {metadata.abstract}")
    print(f"Abstract Length: {len(metadata.abstract)} characters")
    
    print("\n5. KEYWORDS")
    print("-" * 50)
    print(f"Keywords: {', '.join(metadata.keywords)}")
    print(f"Number of Keywords: {len(metadata.keywords)}")
    
    print("\n6. CITATIONS")
    print("-" * 50)
    print(f"Number of Citations: {len(metadata.citations)}")
    for citation in metadata.citations:
        print(f"• {citation.title} ({citation.year})")
        print(f"  Authors: {', '.join(citation.authors)}")
        print(f"  Journal: {citation.journal}")
        print(f"  DOI: {citation.doi}")
    
    print("\n7. SUBJECT CATEGORIES")
    print("-" * 50)
    print(f"Categories: {', '.join(metadata.subject_categories)}")
    
    print("\n8. CONFIDENCE SCORES")
    print("-" * 50)
    print(f"Title Confidence: {metadata.title_confidence:.2f}")
    print(f"Abstract Confidence: {metadata.abstract_confidence:.2f}")
    print(f"Author Confidence: {metadata.author_confidence:.2f}")
    
    print("\n9. METADATA STATISTICS")
    print("-" * 50)
    print(f"Total Authors: {len(metadata.authors)}")
    print(f"Authors with Email: {sum(1 for a in metadata.authors if a.email)}")
    print(f"Authors with ORCID: {sum(1 for a in metadata.authors if a.orcid)}")
    print(f"Authors with Affiliations: {sum(1 for a in metadata.authors if a.affiliations)}")
    print(f"Total Citations: {len(metadata.citations)}")
    print(f"Citations with DOI: {sum(1 for c in metadata.citations if c.doi)}")
    print(f"Average Citation Year: {sum(c.year for c in metadata.citations if c.year) / len([c for c in metadata.citations if c.year]):.0f}")
    
    return metadata

def demonstrate_export_functionality(metadata: EnhancedMetadata):
    """Demonstrate metadata export functionality"""
    print("\n" + "=" * 80)
    print("EXPORT FUNCTIONALITY DEMO")
    print("=" * 80)
    
    # Export to JSON
    print("\n1. JSON EXPORT")
    print("-" * 50)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json_path = f.name
    
    try:
        success = export_metadata(metadata, json_path, 'json')
        if success:
            print(f"✓ Successfully exported to JSON: {json_path}")
            
            # Read and display sample
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            print(f"JSON file size: {os.path.getsize(json_path)} bytes")
            print(f"JSON structure contains {len(data)} top-level keys:")
            for key in sorted(data.keys()):
                print(f"  • {key}")
            
            # Display a sample of the JSON content
            print("\nSample JSON content:")
            sample_keys = ['title', 'doi', 'paper_type', 'publication_status']
            for key in sample_keys:
                if key in data:
                    print(f"  {key}: {data[key]}")
        else:
            print("✗ Failed to export to JSON")
    
    finally:
        if os.path.exists(json_path):
            os.unlink(json_path)
    
    print("\n2. DICTIONARY CONVERSION")
    print("-" * 50)
    data_dict = metadata.to_dict()
    print(f"Dictionary contains {len(data_dict)} keys")
    print(f"Serializable: {all(isinstance(v, (str, int, float, bool, list, dict, type(None))) for v in data_dict.values())}")
    
    # Show data types
    type_counts = {}
    for value in data_dict.values():
        type_name = type(value).__name__
        type_counts[type_name] = type_counts.get(type_name, 0) + 1
    
    print("Data type distribution:")
    for type_name, count in sorted(type_counts.items()):
        print(f"  {type_name}: {count}")

def demonstrate_advanced_features():
    """Demonstrate advanced features and edge cases"""
    print("\n" + "=" * 80)
    print("ADVANCED FEATURES DEMO")
    print("=" * 80)
    
    extractor = MetadataExtractor()
    
    print("\n1. PATTERN MATCHING ROBUSTNESS")
    print("-" * 50)
    
    # Test various title formats
    title_tests = [
        "Machine Learning in Healthcare",
        "TITLE: Advanced Neural Networks",
        "\"Deep Learning: A Comprehensive Guide\"",
        "   Artificial Intelligence Applications   ",
    ]
    
    for title_test in title_tests:
        cleaned = extractor._clean_title(title_test)
        confidence = extractor._calculate_title_confidence(cleaned)
        print(f"'{title_test}' → '{cleaned}' (confidence: {confidence:.2f})")
    
    print("\n2. AUTHOR PARSING VARIATIONS")
    print("-" * 50)
    
    author_tests = [
        "John Doe, Jane Smith, and Michael Johnson",
        "J. Doe, J. Smith & M. Johnson",
        "Doe, J., Smith, J., Johnson, M.",
        "John Doe et al.",
    ]
    
    for author_test in author_tests:
        authors = extractor._parse_authors(author_test)
        print(f"'{author_test}' → {len(authors)} authors: {[a.name for a in authors]}")
    
    print("\n3. IDENTIFIER EXTRACTION")
    print("-" * 50)
    
    # Test DOI patterns
    doi_tests = [
        "DOI: 10.1234/journal.2023.001",
        "https://doi.org/10.1234/journal.2023.001",
        "Available at doi.org/10.1234/journal.2023.001",
        "10.1234/journal.2023.001",
    ]
    
    for doi_test in doi_tests:
        doi = extractor._extract_doi(doi_test)
        print(f"'{doi_test}' → DOI: {doi}")
    
    # Test arXiv patterns
    arxiv_tests = [
        "arXiv:2023.12345v1",
        "https://arxiv.org/abs/2023.12345",
        "Available at arxiv.org/abs/2023.12345v2",
    ]
    
    for arxiv_test in arxiv_tests:
        arxiv_id = extractor._extract_arxiv_id(arxiv_test)
        print(f"'{arxiv_test}' → arXiv: {arxiv_id}")
    
    print("\n4. CONFIDENCE SCORING EXAMPLES")
    print("-" * 50)
    
    # Test confidence with different quality inputs
    quality_tests = [
        ("Excellent Title: Machine Learning in Healthcare", "High Quality"),
        ("ML in HC", "Low Quality"),
        ("", "Empty"),
        ("A" * 300, "Too Long"),
    ]
    
    for test_input, description in quality_tests:
        confidence = extractor._calculate_title_confidence(test_input)
        print(f"{description}: {confidence:.2f} confidence")

def demonstrate_integration_examples():
    """Demonstrate integration with other Paper2Data components"""
    print("\n" + "=" * 80)
    print("INTEGRATION EXAMPLES")
    print("=" * 80)
    
    print("\n1. GLOBAL FUNCTION USAGE")
    print("-" * 50)
    print("# Extract metadata from PDF file")
    print("from paper2data import extract_metadata")
    print("metadata = extract_metadata('research_paper.pdf')")
    print("print(f'Title: {metadata.title}')")
    print("print(f'Authors: {len(metadata.authors)}')")
    
    print("\n2. EXPORT TO DIFFERENT FORMATS")
    print("-" * 50)
    print("# Export metadata to JSON")
    print("from paper2data import export_metadata")
    print("export_metadata(metadata, 'metadata.json', 'json')")
    
    print("\n3. CONFIDENCE-BASED FILTERING")
    print("-" * 50)
    print("# Filter high-confidence results")
    print("if metadata.title_confidence > 0.8:")
    print("    print(f'High confidence title: {metadata.title}')")
    print("if metadata.abstract_confidence > 0.7:")
    print("    print('High confidence abstract available')")
    
    print("\n4. AUTHOR ANALYSIS")
    print("-" * 50)
    print("# Analyze author information")
    print("corresponding_authors = [a for a in metadata.authors if a.is_corresponding]")
    print("authors_with_orcid = [a for a in metadata.authors if a.orcid]")
    print("print(f'Corresponding authors: {len(corresponding_authors)}')")
    print("print(f'Authors with ORCID: {len(authors_with_orcid)}')")
    
    print("\n5. CITATION NETWORK ANALYSIS")
    print("-" * 50)
    print("# Analyze citation patterns")
    print("recent_citations = [c for c in metadata.citations if c.year and c.year > 2020]")
    print("citations_with_doi = [c for c in metadata.citations if c.doi]")
    print("print(f'Recent citations: {len(recent_citations)}')")
    print("print(f'Citations with DOI: {len(citations_with_doi)}')")

def main():
    """Main demo function"""
    print("Paper2Data Enhanced Metadata Extraction Demo")
    print("=" * 80)
    print("This demo showcases the comprehensive metadata extraction capabilities")
    print("of Paper2Data, including title, authors, abstract, keywords, DOI,")
    print("publication information, citations, and confidence scoring.")
    print()
    
    try:
        # Run demonstrations
        demonstrate_basic_functionality()
        metadata = demonstrate_full_extraction()
        demonstrate_export_functionality(metadata)
        demonstrate_advanced_features()
        demonstrate_integration_examples()
        
        print("\n" + "=" * 80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("✓ All metadata extraction features demonstrated")
        print("✓ Export functionality tested")
        print("✓ Advanced features showcased")
        print("✓ Integration examples provided")
        print("\nThe Enhanced Metadata Extraction system is ready for use!")
        
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 