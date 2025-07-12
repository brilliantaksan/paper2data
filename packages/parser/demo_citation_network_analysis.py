#!/usr/bin/env python3
"""
Demo script for Citation Network Analysis in Paper2Data

This script demonstrates the comprehensive citation network analysis capabilities
including network construction, graph metrics, bibliometric analysis, and
citation influence measurement.
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from typing import Dict, Any, List

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from paper2data.citation_network_analyzer import (
    CitationNetworkAnalyzer, NetworkType, CentralityMetric,
    build_citation_network, analyze_citation_networks
)

def create_sample_papers_dataset() -> List[Dict[str, Any]]:
    """Create a comprehensive sample dataset for demonstration"""
    return [
        {
            "title": "Deep Learning Foundations: A Comprehensive Survey",
            "authors": [
                {"name": "Alice Johnson", "position": 1},
                {"name": "Bob Smith", "position": 2},
                {"name": "Carol Davis", "position": 3}
            ],
            "publication_info": {
                "year": 2018,
                "journal": "Journal of AI Research",
                "volume": "25",
                "issue": "3",
                "pages": "45-78"
            },
            "doi": "10.1234/jair.2018.deep.foundations",
            "arxiv_id": "1801.12345",
            "keywords": ["deep learning", "neural networks", "artificial intelligence", "machine learning"],
            "citations": [
                {
                    "text": "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.",
                    "title": "Deep Learning",
                    "authors": ["I. Goodfellow", "Y. Bengio", "A. Courville"],
                    "year": 2016,
                    "journal": "MIT Press",
                    "doi": "10.1234/mit.2016.deeplearning"
                },
                {
                    "text": "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444.",
                    "title": "Deep learning",
                    "authors": ["Y. LeCun", "Y. Bengio", "G. Hinton"],
                    "year": 2015,
                    "journal": "Nature",
                    "doi": "10.1038/nature14539"
                }
            ]
        },
        {
            "title": "Neural Network Architectures for Computer Vision",
            "authors": [
                {"name": "David Wilson", "position": 1},
                {"name": "Alice Johnson", "position": 2},
                {"name": "Eva Brown", "position": 3}
            ],
            "publication_info": {
                "year": 2019,
                "journal": "Computer Vision Review",
                "volume": "12",
                "issue": "2",
                "pages": "123-156"
            },
            "doi": "10.1234/cvr.2019.neural.architectures",
            "keywords": ["computer vision", "neural networks", "deep learning", "CNN"],
            "citations": [
                {
                    "text": "Johnson, A., Smith, B., & Davis, C. (2018). Deep Learning Foundations: A Comprehensive Survey. Journal of AI Research, 25(3), 45-78.",
                    "title": "Deep Learning Foundations: A Comprehensive Survey",
                    "authors": ["A. Johnson", "B. Smith", "C. Davis"],
                    "year": 2018,
                    "journal": "Journal of AI Research",
                    "doi": "10.1234/jair.2018.deep.foundations"
                },
                {
                    "text": "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444.",
                    "title": "Deep learning",
                    "authors": ["Y. LeCun", "Y. Bengio", "G. Hinton"],
                    "year": 2015,
                    "journal": "Nature",
                    "doi": "10.1038/nature14539"
                }
            ]
        },
        {
            "title": "Transformer Networks and Attention Mechanisms",
            "authors": [
                {"name": "Frank Miller", "position": 1},
                {"name": "Grace Chen", "position": 2}
            ],
            "publication_info": {
                "year": 2020,
                "journal": "Natural Language Processing Review",
                "volume": "8",
                "issue": "1",
                "pages": "1-34"
            },
            "doi": "10.1234/nlpr.2020.transformers",
            "keywords": ["transformers", "attention mechanisms", "natural language processing", "deep learning"],
            "citations": [
                {
                    "text": "Johnson, A., Smith, B., & Davis, C. (2018). Deep Learning Foundations: A Comprehensive Survey. Journal of AI Research, 25(3), 45-78.",
                    "title": "Deep Learning Foundations: A Comprehensive Survey",
                    "authors": ["A. Johnson", "B. Smith", "C. Davis"],
                    "year": 2018,
                    "journal": "Journal of AI Research",
                    "doi": "10.1234/jair.2018.deep.foundations"
                },
                {
                    "text": "Wilson, D., Johnson, A., & Brown, E. (2019). Neural Network Architectures for Computer Vision. Computer Vision Review, 12(2), 123-156.",
                    "title": "Neural Network Architectures for Computer Vision",
                    "authors": ["D. Wilson", "A. Johnson", "E. Brown"],
                    "year": 2019,
                    "journal": "Computer Vision Review",
                    "doi": "10.1234/cvr.2019.neural.architectures"
                }
            ]
        },
        {
            "title": "Reinforcement Learning in Complex Environments",
            "authors": [
                {"name": "Henry Garcia", "position": 1},
                {"name": "Isabel Rodriguez", "position": 2},
                {"name": "Bob Smith", "position": 3}
            ],
            "publication_info": {
                "year": 2021,
                "journal": "Machine Learning Advances",
                "volume": "15",
                "issue": "4",
                "pages": "89-121"
            },
            "doi": "10.1234/mla.2021.reinforcement",
            "keywords": ["reinforcement learning", "complex environments", "artificial intelligence", "agents"],
            "citations": [
                {
                    "text": "Johnson, A., Smith, B., & Davis, C. (2018). Deep Learning Foundations: A Comprehensive Survey. Journal of AI Research, 25(3), 45-78.",
                    "title": "Deep Learning Foundations: A Comprehensive Survey",
                    "authors": ["A. Johnson", "B. Smith", "C. Davis"],
                    "year": 2018,
                    "journal": "Journal of AI Research",
                    "doi": "10.1234/jair.2018.deep.foundations"
                }
            ]
        },
        {
            "title": "Generative Adversarial Networks: Theory and Applications",
            "authors": [
                {"name": "Jack Thompson", "position": 1},
                {"name": "Kate Williams", "position": 2},
                {"name": "David Wilson", "position": 3}
            ],
            "publication_info": {
                "year": 2022,
                "journal": "Generative AI Review",
                "volume": "3",
                "issue": "1",
                "pages": "15-48"
            },
            "doi": "10.1234/gar.2022.gans",
            "keywords": ["generative adversarial networks", "GANs", "generative models", "deep learning"],
            "citations": [
                {
                    "text": "Wilson, D., Johnson, A., & Brown, E. (2019). Neural Network Architectures for Computer Vision. Computer Vision Review, 12(2), 123-156.",
                    "title": "Neural Network Architectures for Computer Vision",
                    "authors": ["D. Wilson", "A. Johnson", "E. Brown"],
                    "year": 2019,
                    "journal": "Computer Vision Review",
                    "doi": "10.1234/cvr.2019.neural.architectures"
                },
                {
                    "text": "Miller, F., & Chen, G. (2020). Transformer Networks and Attention Mechanisms. Natural Language Processing Review, 8(1), 1-34.",
                    "title": "Transformer Networks and Attention Mechanisms",
                    "authors": ["F. Miller", "G. Chen"],
                    "year": 2020,
                    "journal": "Natural Language Processing Review",
                    "doi": "10.1234/nlpr.2020.transformers"
                }
            ]
        }
    ]

def demonstrate_basic_network_construction():
    """Demonstrate basic citation network construction"""
    print("=" * 80)
    print("CITATION NETWORK CONSTRUCTION DEMO")
    print("=" * 80)
    
    # Create analyzer and sample data
    analyzer = CitationNetworkAnalyzer()
    papers = create_sample_papers_dataset()
    
    print(f"✓ Created CitationNetworkAnalyzer instance")
    print(f"✓ Sample dataset: {len(papers)} papers")
    
    print("\n1. CITATION NETWORK CONSTRUCTION")
    print("-" * 50)
    
    # Build citation network
    citation_network = analyzer.build_citation_network(papers)
    
    print(f"Citation Network Built:")
    print(f"  • Nodes (Papers): {citation_network.number_of_nodes()}")
    print(f"  • Edges (Citations): {citation_network.number_of_edges()}")
    print(f"  • Network Type: {'Directed' if citation_network.is_directed() else 'Undirected'}")
    
    # Display node information
    print(f"\nPaper Nodes:")
    for node_id, data in citation_network.nodes(data=True):
        print(f"  • {node_id[:20]}... → '{data.get('title', 'Unknown')[:50]}...'")
        print(f"    Authors: {len(data.get('authors', []))}, Year: {data.get('year', 'Unknown')}")
    
    # Display edge information
    print(f"\nCitation Edges:")
    for source, target, data in citation_network.edges(data=True):
        print(f"  • {source[:20]}... → {target[:20]}...")
        print(f"    Type: {data.get('edge_type', 'Unknown')}, Year: {data.get('year', 'Unknown')}")
    
    return analyzer, papers

def demonstrate_multiple_network_types(analyzer, papers):
    """Demonstrate construction of multiple network types"""
    print("\n" + "=" * 80)
    print("MULTIPLE NETWORK TYPES DEMO")
    print("=" * 80)
    
    # Get citation network
    citation_network = analyzer.networks[NetworkType.CITATION]
    
    print("\n1. CO-CITATION NETWORK")
    print("-" * 50)
    
    # Build co-citation network
    cocitation_network = analyzer.build_cocitation_network(citation_network)
    
    print(f"Co-citation Network:")
    print(f"  • Nodes: {cocitation_network.number_of_nodes()}")
    print(f"  • Edges: {cocitation_network.number_of_edges()}")
    print(f"  • Threshold: {analyzer.cocitation_threshold} minimum co-citations")
    
    print("\n2. BIBLIOGRAPHIC COUPLING NETWORK")
    print("-" * 50)
    
    # Build bibliographic coupling network
    coupling_network = analyzer.build_bibliographic_coupling_network(citation_network)
    
    print(f"Bibliographic Coupling Network:")
    print(f"  • Nodes: {coupling_network.number_of_nodes()}")
    print(f"  • Edges: {coupling_network.number_of_edges()}")
    print(f"  • Threshold: {analyzer.coupling_threshold} minimum shared references")
    
    print("\n3. AUTHOR COLLABORATION NETWORK")
    print("-" * 50)
    
    # Build author collaboration network
    author_network = analyzer.build_author_collaboration_network(papers)
    
    print(f"Author Collaboration Network:")
    print(f"  • Nodes (Authors): {author_network.number_of_nodes()}")
    print(f"  • Edges (Collaborations): {author_network.number_of_edges()}")
    
    # Display author nodes
    print(f"\nAuthor Nodes:")
    for node_id, data in author_network.nodes(data=True):
        print(f"  • {node_id}")
    
    print("\n4. KEYWORD CO-OCCURRENCE NETWORK")
    print("-" * 50)
    
    # Build keyword co-occurrence network
    keyword_network = analyzer.build_keyword_cooccurrence_network(papers)
    
    print(f"Keyword Co-occurrence Network:")
    print(f"  • Nodes (Keywords): {keyword_network.number_of_nodes()}")
    print(f"  • Edges (Co-occurrences): {keyword_network.number_of_edges()}")
    
    # Display keyword nodes
    print(f"\nKeyword Nodes:")
    for node_id, data in keyword_network.nodes(data=True):
        print(f"  • '{node_id}'")

def demonstrate_network_metrics(analyzer):
    """Demonstrate comprehensive network metrics calculation"""
    print("\n" + "=" * 80)
    print("NETWORK METRICS ANALYSIS DEMO")
    print("=" * 80)
    
    citation_network = analyzer.networks[NetworkType.CITATION]
    
    print("\n1. BASIC NETWORK METRICS")
    print("-" * 50)
    
    # Calculate basic metrics
    metrics = analyzer.calculate_network_metrics(citation_network, NetworkType.CITATION)
    
    print(f"Network Structure:")
    print(f"  • Nodes: {metrics.num_nodes}")
    print(f"  • Edges: {metrics.num_edges}")
    print(f"  • Density: {metrics.density:.4f}")
    print(f"  • Connected: {metrics.is_connected}")
    print(f"  • Components: {metrics.num_components}")
    
    print(f"\nClustering Metrics:")
    print(f"  • Average Clustering: {metrics.average_clustering:.4f}")
    print(f"  • Global Clustering: {metrics.global_clustering:.4f}")
    
    print(f"\nCitation-Specific Metrics:")
    print(f"  • Average Citations per Paper: {metrics.average_citations_per_paper:.2f}")
    print(f"  • Most Cited Papers: {len(metrics.most_cited_papers)}")
    
    if metrics.network_age:
        print(f"\nTemporal Metrics:")
        print(f"  • Network Age: {metrics.network_age} years")
        print(f"  • Citation Velocity: {metrics.citation_velocity:.2f} citations/year")
    
    print("\n2. CENTRALITY METRICS")
    print("-" * 50)
    
    # Calculate centrality metrics
    centrality_metrics = [
        CentralityMetric.DEGREE,
        CentralityMetric.BETWEENNESS,
        CentralityMetric.CLOSENESS,
        CentralityMetric.PAGERANK
    ]
    
    centrality = analyzer.calculate_centrality_metrics(citation_network, centrality_metrics)
    
    print(f"Centrality Analysis:")
    for metric_name, scores in centrality.items():
        if scores:
            max_node = max(scores.items(), key=lambda x: x[1])
            avg_score = sum(scores.values()) / len(scores)
            print(f"  • {metric_name.title()}:")
            print(f"    - Average: {avg_score:.4f}")
            print(f"    - Highest: {max_node[1]:.4f} ({max_node[0][:30]}...)")
    
    return metrics, centrality

def demonstrate_author_analysis(analyzer, papers):
    """Demonstrate author-specific analysis"""
    print("\n" + "=" * 80)
    print("AUTHOR ANALYSIS DEMO")
    print("=" * 80)
    
    print("\n1. AUTHOR METRICS CALCULATION")
    print("-" * 50)
    
    # Analyze author metrics
    author_metrics = analyzer.analyze_author_metrics(papers)
    
    print(f"Author Analysis Results:")
    print(f"  • Total Authors: {len(author_metrics)}")
    
    # Sort authors by various metrics
    print(f"\nTop Authors by Paper Count:")
    authors_by_papers = sorted(author_metrics.items(), key=lambda x: x[1].paper_count, reverse=True)
    for i, (author, metrics) in enumerate(authors_by_papers[:5], 1):
        print(f"  {i}. {author}")
        print(f"     Papers: {metrics.paper_count}, Citations: {metrics.total_citations}")
        print(f"     H-index: {metrics.h_index}, Collaborators: {metrics.collaboration_count}")
        if metrics.research_areas:
            print(f"     Research Areas: {', '.join(metrics.research_areas[:3])}")
    
    print(f"\nTop Authors by H-index:")
    authors_by_h_index = sorted(author_metrics.items(), key=lambda x: x[1].h_index, reverse=True)
    for i, (author, metrics) in enumerate(authors_by_h_index[:5], 1):
        print(f"  {i}. {author} (H-index: {metrics.h_index})")
        print(f"     Avg Citations per Paper: {metrics.average_citations_per_paper:.2f}")
    
    print(f"\nCollaboration Analysis:")
    total_collaborations = sum(m.collaboration_count for m in author_metrics.values())
    avg_collaborations = total_collaborations / len(author_metrics) if author_metrics else 0
    print(f"  • Average Collaborations per Author: {avg_collaborations:.2f}")
    
    # Find most collaborative authors
    most_collaborative = max(author_metrics.items(), key=lambda x: x[1].collaboration_count)
    print(f"  • Most Collaborative: {most_collaborative[0]} ({most_collaborative[1].collaboration_count} collaborators)")
    
    return author_metrics

def demonstrate_citation_influence(analyzer):
    """Demonstrate citation influence analysis"""
    print("\n" + "=" * 80)
    print("CITATION INFLUENCE ANALYSIS DEMO")
    print("=" * 80)
    
    citation_network = analyzer.networks[NetworkType.CITATION]
    
    print("\n1. INFLUENCE CALCULATION")
    print("-" * 50)
    
    # Analyze citation influence
    influence_data = analyzer.analyze_citation_influence(citation_network)
    
    print(f"Citation Influence Analysis:")
    print(f"  • Papers Analyzed: {len(influence_data)}")
    
    # Sort by influence score
    papers_by_influence = sorted(influence_data.items(), key=lambda x: x[1].influence_score, reverse=True)
    
    print(f"\nMost Influential Papers:")
    for i, (paper_id, influence) in enumerate(papers_by_influence[:5], 1):
        paper_data = analyzer.metadata_cache.get(paper_id, {})
        title = paper_data.get('title', 'Unknown Title')[:50]
        
        print(f"  {i}. {title}...")
        print(f"     Direct Citations: {influence.direct_citations}")
        print(f"     Influence Score: {influence.influence_score:.2f}")
        if influence.citation_generations:
            total_generations = len(influence.citation_generations)
            print(f"     Citation Generations: {total_generations}")
    
    # Analyze temporal influence
    print(f"\nTemporal Influence Analysis:")
    total_temporal_citations = sum(
        sum(influence.temporal_influence.values())
        for influence in influence_data.values()
    )
    print(f"  • Total Temporal Citations Tracked: {total_temporal_citations}")
    
    return influence_data

def demonstrate_network_export(analyzer):
    """Demonstrate network export capabilities"""
    print("\n" + "=" * 80)
    print("NETWORK EXPORT DEMO")
    print("=" * 80)
    
    print("\n1. EXPORT FORMATS")
    print("-" * 50)
    
    # Test different export formats
    formats_to_test = ['json', 'csv_nodes', 'csv_edges']
    
    for format_name in formats_to_test:
        with tempfile.NamedTemporaryFile(suffix=f'.{format_name.split("_")[0]}', delete=False) as f:
            export_path = f.name
        
        try:
            success = analyzer.export_network(NetworkType.CITATION, export_path, format_name)
            if success:
                file_size = os.path.getsize(export_path)
                print(f"  ✓ {format_name.upper()} export: {export_path} ({file_size} bytes)")
                
                # Show sample content for JSON
                if format_name == 'json':
                    with open(export_path, 'r') as f:
                        data = json.load(f)
                        print(f"    Structure: {list(data.keys())}")
                        print(f"    Nodes: {len(data.get('nodes', []))}")
                        print(f"    Links: {len(data.get('links', []))}")
            else:
                print(f"  ✗ {format_name.upper()} export failed")
        
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)

def demonstrate_comprehensive_analysis():
    """Demonstrate comprehensive network analysis using global function"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE ANALYSIS DEMO")
    print("=" * 80)
    
    papers = create_sample_papers_dataset()
    
    print("\n1. GLOBAL ANALYSIS FUNCTION")
    print("-" * 50)
    
    # Use global analysis function
    results = analyze_citation_networks(papers)
    
    print(f"Comprehensive Analysis Results:")
    print(f"  • Papers Analyzed: {results['total_papers_analyzed']}")
    print(f"  • Analysis Timestamp: {results['analysis_timestamp']}")
    
    print(f"\nNetwork Types Built:")
    networks = results.get('networks', {})
    for network_name, network_data in networks.items():
        if 'basic_metrics' in network_data:
            metrics = network_data['basic_metrics']
            print(f"  • {network_name.title()}:")
            print(f"    - Nodes: {metrics.get('num_nodes', 0)}")
            print(f"    - Edges: {metrics.get('num_edges', 0)}")
            print(f"    - Density: {metrics.get('density', 0):.4f}")
    
    print(f"\nAuthor Analysis:")
    author_analysis = results.get('author_analysis', {})
    print(f"  • Authors Found: {len(author_analysis)}")
    
    if author_analysis:
        # Find most productive author
        most_productive = max(
            author_analysis.items(),
            key=lambda x: x[1].get('paper_count', 0)
        )
        print(f"  • Most Productive: {most_productive[0]} ({most_productive[1].get('paper_count', 0)} papers)")
    
    print(f"\nInfluence Analysis:")
    influence_analysis = results.get('influence_analysis', {})
    print(f"  • Papers with Influence Data: {len(influence_analysis)}")
    
    if influence_analysis:
        # Find most influential paper
        most_influential = max(
            influence_analysis.items(),
            key=lambda x: x[1].get('influence_score', 0)
        )
        print(f"  • Most Influential: {most_influential[0][:30]}... (Score: {most_influential[1].get('influence_score', 0):.2f})")
    
    return results

def demonstrate_advanced_features(analyzer):
    """Demonstrate advanced analysis features"""
    print("\n" + "=" * 80)
    print("ADVANCED FEATURES DEMO")
    print("=" * 80)
    
    print("\n1. NETWORK SUMMARY GENERATION")
    print("-" * 50)
    
    # Generate network summaries
    network_types = [NetworkType.CITATION, NetworkType.AUTHOR_COLLABORATION, NetworkType.KEYWORD_COOCCURRENCE]
    
    for network_type in network_types:
        if network_type in analyzer.networks:
            summary = analyzer.generate_network_summary(network_type)
            
            print(f"\n{network_type.value.title()} Network Summary:")
            print(f"  • Network Type: {summary['network_type']}")
            
            if 'basic_metrics' in summary:
                metrics = summary['basic_metrics']
                print(f"  • Nodes: {metrics.get('num_nodes', 0)}")
                print(f"  • Edges: {metrics.get('num_edges', 0)}")
                print(f"  • Density: {metrics.get('density', 0):.4f}")
                print(f"  • Connected: {metrics.get('is_connected', False)}")
            
            if 'recommendations' in summary and summary['recommendations']:
                print(f"  • Recommendations:")
                for rec in summary['recommendations'][:3]:
                    print(f"    - {rec}")
    
    print("\n2. CONFIGURABLE THRESHOLDS")
    print("-" * 50)
    
    print(f"Current Configuration:")
    print(f"  • Co-citation Threshold: {analyzer.cocitation_threshold}")
    print(f"  • Coupling Threshold: {analyzer.coupling_threshold}")
    print(f"  • Collaboration Threshold: {analyzer.collaboration_threshold}")
    
    # Test threshold adjustment
    print(f"\nTesting Threshold Adjustment:")
    original_cocitation = analyzer.cocitation_threshold
    analyzer.cocitation_threshold = 1  # Lower threshold
    
    citation_network = analyzer.networks[NetworkType.CITATION]
    new_cocitation_network = analyzer.build_cocitation_network(citation_network)
    
    print(f"  • Lower Co-citation Threshold (1):")
    print(f"    - Edges: {new_cocitation_network.number_of_edges()}")
    
    # Restore original threshold
    analyzer.cocitation_threshold = original_cocitation

def demonstrate_integration_examples():
    """Demonstrate integration with other Paper2Data components"""
    print("\n" + "=" * 80)
    print("INTEGRATION EXAMPLES")
    print("=" * 80)
    
    print("\n1. GLOBAL FUNCTION USAGE")
    print("-" * 50)
    print("# Build citation network from papers metadata")
    print("from paper2data import build_citation_network")
    print("network = build_citation_network(papers_metadata)")
    print("print(f'Network: {network.number_of_nodes()} nodes, {network.number_of_edges()} edges')")
    
    print("\n2. COMPREHENSIVE ANALYSIS")
    print("-" * 50)
    print("# Analyze all network types")
    print("from paper2data import analyze_citation_networks")
    print("results = analyze_citation_networks(papers_metadata)")
    print("print(f'Networks built: {len(results[\"networks\"])}')")
    
    print("\n3. NETWORK METRICS FILTERING")
    print("-" * 50)
    print("# Filter networks by metrics")
    print("for network_name, network_data in results['networks'].items():")
    print("    metrics = network_data['basic_metrics']")
    print("    if metrics['density'] > 0.1:")
    print("        print(f'Dense network: {network_name}')")
    
    print("\n4. AUTHOR COLLABORATION ANALYSIS")
    print("-" * 50)
    print("# Analyze author collaborations")
    print("author_analysis = results['author_analysis']")
    print("highly_collaborative = {name: data for name, data in author_analysis.items()")
    print("                      if data['collaboration_count'] > 3}")
    print("print(f'Highly collaborative authors: {len(highly_collaborative)}')")
    
    print("\n5. CITATION INFLUENCE RANKING")
    print("-" * 50)
    print("# Rank papers by influence")
    print("influence_analysis = results['influence_analysis']")
    print("ranked_papers = sorted(influence_analysis.items(),")
    print("                      key=lambda x: x[1]['influence_score'], reverse=True)")
    print("print(f'Most influential: {ranked_papers[0][0]}')")

def main():
    """Main demo function"""
    print("Paper2Data Citation Network Analysis Demo")
    print("=" * 80)
    print("This demo showcases the comprehensive citation network analysis")
    print("capabilities including network construction, metrics calculation,")
    print("bibliometric analysis, and citation influence measurement.")
    print()
    
    try:
        # Run demonstrations
        analyzer, papers = demonstrate_basic_network_construction()
        demonstrate_multiple_network_types(analyzer, papers)
        metrics, centrality = demonstrate_network_metrics(analyzer)
        author_metrics = demonstrate_author_analysis(analyzer, papers)
        influence_data = demonstrate_citation_influence(analyzer)
        demonstrate_network_export(analyzer)
        comprehensive_results = demonstrate_comprehensive_analysis()
        demonstrate_advanced_features(analyzer)
        demonstrate_integration_examples()
        
        print("\n" + "=" * 80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("✓ Citation network construction demonstrated")
        print("✓ Multiple network types built and analyzed")
        print("✓ Comprehensive metrics calculated")
        print("✓ Author and influence analysis completed")
        print("✓ Export capabilities showcased")
        print("✓ Advanced features demonstrated")
        print("✓ Integration examples provided")
        print("\nThe Citation Network Analysis system is ready for academic research!")
        
        # Final statistics
        print(f"\nFinal Statistics:")
        print(f"  • Papers Processed: {len(papers)}")
        print(f"  • Networks Built: {len(analyzer.networks)}")
        print(f"  • Authors Analyzed: {len(author_metrics)}")
        print(f"  • Influence Scores Calculated: {len(influence_data)}")
        print(f"  • Network Types: {[nt.value for nt in analyzer.networks.keys()]}")
        
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 