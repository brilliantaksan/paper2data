#!/usr/bin/env python3
"""
Paper2Data Plugin System Demo

This script demonstrates the comprehensive plugin architecture capabilities
of Paper2Data, including:

1. Plugin Management
   - Loading plugins from directories
   - Plugin lifecycle management
   - Configuration and validation

2. Hook System
   - Hook registration and execution
   - Plugin priority handling
   - Error handling and recovery

3. Integration
   - Integration with main processing pipeline
   - Custom plugin development
   - Performance monitoring

4. Example Plugins
   - LaTeX processor plugin
   - NLP analysis plugin
   - Custom processing extensions

Usage:
    python demo_plugin_system.py

Author: Paper2Data Team
Version: 1.0.0
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the package to the path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from paper2data.plugin_manager import (
    PluginManager, BasePlugin, PluginMetadata, PluginStatus,
    HookPriority, plugin_hook, initialize_plugin_system, get_plugin_manager
)
from paper2data.plugin_hooks import (
    execute_hook, execute_hook_until_success, get_hook_documentation,
    get_all_hook_names, list_hooks_by_category, HookCategory
)

def print_section(title: str, content: str = ""):
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    if content:
        print(content)
    print()

def print_subsection(title: str):
    """Print a formatted subsection header"""
    print(f"\n--- {title} ---")

def demo_plugin_system_overview():
    """Demonstrate plugin system overview"""
    print_section("PAPER2DATA PLUGIN SYSTEM DEMO", 
                  "Comprehensive demonstration of the extensible plugin architecture")
    
    print("The Paper2Data plugin system provides:")
    print("• Dynamic plugin loading and management")
    print("• Hook-based extension points")
    print("• Configuration and validation")
    print("• Performance monitoring")
    print("• Error handling and recovery")
    print("• Integration with main processing pipeline")

def demo_hook_system():
    """Demonstrate the hook system"""
    print_section("HOOK SYSTEM DEMONSTRATION")
    
    print_subsection("Available Hook Categories")
    for category in HookCategory:
        hooks = list_hooks_by_category(category)
        print(f"• {category.value.title()}: {len(hooks)} hooks")
        for hook_name in list(hooks.keys())[:3]:  # Show first 3
            print(f"  - {hook_name}")
        if len(hooks) > 3:
            print(f"  ... and {len(hooks) - 3} more")
    
    print_subsection("Hook Documentation Sample")
    hook_doc = get_hook_documentation()
    
    # Show document processing hooks
    if 'document' in hook_doc:
        print("Document Processing Hooks:")
        for hook_name, hook_info in list(hook_doc['document']['hooks'].items())[:2]:
            print(f"  • {hook_name}")
            print(f"    Description: {hook_info['description']}")
            print(f"    Parameters: {list(hook_info['parameters'].keys())}")
            print(f"    Return Type: {hook_info['return_type']}")
            print()

def demo_plugin_creation():
    """Demonstrate plugin creation"""
    print_section("PLUGIN CREATION DEMONSTRATION")
    
    print_subsection("Creating a Custom Plugin")
    
    # Create a demo plugin class
    class DemoPlugin(BasePlugin):
        """Demo plugin for showcase"""
        
        def get_metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="demo_plugin",
                version="1.0.0",
                description="Demonstration plugin for Paper2Data",
                author="Paper2Data Team",
                license="MIT",
                dependencies=["json", "logging"],
                hooks=["process_equations", "enhance_metadata", "validate_output"],
                config_schema={
                    "type": "object",
                    "properties": {
                        "enhancement_level": {
                            "type": "string",
                            "enum": ["basic", "advanced", "expert"],
                            "default": "basic"
                        },
                        "confidence_threshold": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "default": 0.5
                        }
                    }
                },
                tags=["demo", "showcase", "example"]
            )
        
        def setup(self) -> bool:
            print(f"    ✓ Demo plugin setup complete")
            return True
        
        def cleanup(self) -> bool:
            print(f"    ✓ Demo plugin cleanup complete")
            return True
        
        @plugin_hook("process_equations", HookPriority.HIGH, 
                    "Demo equation processing with enhanced analysis")
        def process_equations_hook(self, equations: List[Dict[str, Any]], 
                                  config: Dict[str, Any]) -> List[Dict[str, Any]]:
            """Process equations with demo enhancements"""
            print(f"    → Processing {len(equations)} equations with demo plugin")
            
            enhanced_equations = []
            for eq in equations:
                enhanced = eq.copy()
                enhanced["demo_enhancement"] = True
                enhanced["processing_level"] = self.config.get("enhancement_level", "basic")
                enhanced["demo_confidence"] = min(
                    enhanced.get("confidence", 0.5) + 0.1, 1.0
                )
                enhanced_equations.append(enhanced)
            
            print(f"    ✓ Enhanced {len(enhanced_equations)} equations")
            return enhanced_equations
        
        @plugin_hook("enhance_metadata", HookPriority.NORMAL, 
                    "Demo metadata enhancement")
        def enhance_metadata_hook(self, metadata: Dict[str, Any], 
                                 config: Dict[str, Any]) -> Dict[str, Any]:
            """Enhance metadata with demo features"""
            print(f"    → Enhancing metadata with demo plugin")
            
            enhanced = metadata.copy()
            enhanced["demo_processed"] = True
            enhanced["enhancement_timestamp"] = "2024-01-15T10:30:00Z"
            enhanced["demo_tags"] = ["processed", "enhanced", "demo"]
            
            print(f"    ✓ Metadata enhanced with demo features")
            return enhanced
        
        @plugin_hook("validate_output", HookPriority.LOW, 
                    "Demo output validation")
        def validate_output_hook(self, output_path: str, data: Dict[str, Any], 
                                config: Dict[str, Any]) -> Dict[str, Any]:
            """Validate output with demo checks"""
            print(f"    → Validating output with demo plugin")
            
            validation_result = {
                "plugin": "demo_plugin",
                "validation_passed": True,
                "checks_performed": [
                    "structure_validation",
                    "content_integrity",
                    "demo_quality_check"
                ],
                "demo_score": 0.95,
                "recommendations": [
                    "Output structure is well-formed",
                    "Content integrity verified",
                    "Demo validation successful"
                ]
            }
            
            print(f"    ✓ Output validation complete (score: {validation_result['demo_score']})")
            return validation_result
    
    # Demonstrate plugin instantiation
    print("Creating demo plugin instance...")
    demo_plugin = DemoPlugin({
        "enhancement_level": "advanced",
        "confidence_threshold": 0.7
    })
    
    print(f"✓ Plugin created: {demo_plugin.get_metadata().name}")
    print(f"  Version: {demo_plugin.get_metadata().version}")
    print(f"  Description: {demo_plugin.get_metadata().description}")
    print(f"  Hooks: {demo_plugin.get_metadata().hooks}")
    print(f"  Configuration: {demo_plugin.config}")
    
    return demo_plugin

def demo_plugin_management():
    """Demonstrate plugin management"""
    print_section("PLUGIN MANAGEMENT DEMONSTRATION")
    
    print_subsection("Initializing Plugin Manager")
    
    # Initialize plugin system
    manager = initialize_plugin_system()
    print(f"✓ Plugin manager initialized")
    print(f"  Plugin directories: {manager.plugin_dirs}")
    print(f"  Loaded plugins: {len(manager.plugins)}")
    
    # Create demo plugin
    demo_plugin = demo_plugin_creation()
    
    print_subsection("Manual Plugin Registration")
    
    # Manually register the demo plugin
    from paper2data.plugin_manager import PluginInfo
    
    plugin_info = PluginInfo(
        metadata=demo_plugin.get_metadata(),
        status=PluginStatus.LOADED,
        file_path="demo_plugin.py",
        instance=demo_plugin
    )
    
    manager.plugins["demo_plugin"] = plugin_info
    manager._register_plugin_hooks(plugin_info)
    
    print(f"✓ Demo plugin registered manually")
    print(f"  Plugin name: {plugin_info.metadata.name}")
    print(f"  Status: {plugin_info.status.value}")
    print(f"  Hooks registered: {len(plugin_info.metadata.hooks)}")
    
    print_subsection("Plugin Lifecycle Management")
    
    # Test plugin enabling/disabling
    print("Testing plugin enable/disable...")
    manager.enable_plugin("demo_plugin")
    print(f"  ✓ Plugin enabled: {manager.plugins['demo_plugin'].status.value}")
    
    manager.disable_plugin("demo_plugin")
    print(f"  ✓ Plugin disabled: {manager.plugins['demo_plugin'].status.value}")
    
    manager.enable_plugin("demo_plugin")
    print(f"  ✓ Plugin re-enabled: {manager.plugins['demo_plugin'].status.value}")
    
    print_subsection("Plugin Configuration")
    
    # Test configuration
    new_config = {
        "enhancement_level": "expert",
        "confidence_threshold": 0.8
    }
    
    result = manager.configure_plugin("demo_plugin", new_config)
    print(f"✓ Plugin configuration updated: {result}")
    print(f"  New config: {manager.plugins['demo_plugin'].config}")
    
    return manager

def demo_hook_execution(manager: PluginManager):
    """Demonstrate hook execution"""
    print_section("HOOK EXECUTION DEMONSTRATION")
    
    print_subsection("Sample Data Preparation")
    
    # Prepare sample data
    sample_equations = [
        {
            "content": "E = mc^2",
            "type": "inline",
            "page_number": 1,
            "confidence": 0.9
        },
        {
            "content": "\\frac{d}{dx}[f(x)] = f'(x)",
            "type": "display",
            "page_number": 2,
            "confidence": 0.8
        }
    ]
    
    sample_metadata = {
        "title": "Demo Paper",
        "authors": ["Dr. Demo", "Prof. Example"],
        "abstract": "This is a demo paper for plugin system testing.",
        "keywords": ["demo", "plugin", "system"]
    }
    
    print(f"✓ Sample equations prepared: {len(sample_equations)}")
    print(f"✓ Sample metadata prepared: {list(sample_metadata.keys())}")
    
    print_subsection("Hook Execution - Process Equations")
    
    # Execute equation processing hook
    results = manager.execute_hook("process_equations", sample_equations, {"method": "demo"})
    
    print(f"✓ Hook execution completed")
    print(f"  Results count: {len(results)}")
    if results:
        enhanced_equations = results[0]
        print(f"  Enhanced equations: {len(enhanced_equations)}")
        print(f"  Sample enhancement: {enhanced_equations[0].get('demo_enhancement', False)}")
    
    print_subsection("Hook Execution - Enhance Metadata")
    
    # Execute metadata enhancement hook
    metadata_results = manager.execute_hook("enhance_metadata", sample_metadata, {"method": "demo"})
    
    print(f"✓ Metadata enhancement completed")
    print(f"  Results count: {len(metadata_results)}")
    if metadata_results:
        enhanced_metadata = metadata_results[0]
        print(f"  Demo processed: {enhanced_metadata.get('demo_processed', False)}")
        print(f"  Demo tags: {enhanced_metadata.get('demo_tags', [])}")
    
    print_subsection("Hook Execution - Validate Output")
    
    # Execute output validation hook
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"demo": "output"}, f)
        temp_output = f.name
    
    try:
        validation_results = manager.execute_hook(
            "validate_output", 
            temp_output, 
            {"demo": "data"}, 
            {"format": "json"}
        )
        
        print(f"✓ Output validation completed")
        print(f"  Results count: {len(validation_results)}")
        if validation_results:
            validation = validation_results[0]
            print(f"  Validation passed: {validation.get('validation_passed', False)}")
            print(f"  Demo score: {validation.get('demo_score', 0.0)}")
            print(f"  Checks performed: {len(validation.get('checks_performed', []))}")
    
    finally:
        if os.path.exists(temp_output):
            os.unlink(temp_output)

def demo_plugin_statistics(manager: PluginManager):
    """Demonstrate plugin statistics"""
    print_section("PLUGIN STATISTICS DEMONSTRATION")
    
    print_subsection("Plugin Performance Statistics")
    
    # Get plugin statistics
    stats = manager.get_plugin_statistics()
    
    print(f"✓ Statistics retrieved for {len(stats)} plugins")
    
    for plugin_name, plugin_stats in stats.items():
        print(f"\n  Plugin: {plugin_name}")
        print(f"    Status: {plugin_stats['status']}")
        print(f"    Load time: {plugin_stats.get('load_time', 'N/A')}")
        print(f"    Execution count: {plugin_stats['execution_count']}")
        print(f"    Total execution time: {plugin_stats['total_execution_time']:.3f}s")
        print(f"    Average execution time: {plugin_stats['average_execution_time']:.3f}s")
        print(f"    Hooks registered: {plugin_stats['hooks_registered']}")
    
    print_subsection("Plugin Configuration Export")
    
    # Export configuration
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        export_file = f.name
    
    try:
        manager.export_configuration(export_file)
        print(f"✓ Configuration exported to: {export_file}")
        
        # Read and display sample
        with open(export_file, 'r') as f:
            config_data = json.load(f)
        
        print(f"  Export sections: {list(config_data.keys())}")
        print(f"  Plugins exported: {len(config_data.get('plugin_info', {}))}")
        
    finally:
        if os.path.exists(export_file):
            os.unlink(export_file)

def demo_error_handling():
    """Demonstrate error handling"""
    print_section("ERROR HANDLING DEMONSTRATION")
    
    print_subsection("Plugin Error Simulation")
    
    # Create a plugin that will cause errors
    class ErrorPlugin(BasePlugin):
        def get_metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="error_plugin",
                version="1.0.0",
                description="Plugin that demonstrates error handling",
                author="Demo",
                hooks=["test_hook"]
            )
        
        def setup(self) -> bool:
            print("    ✓ Error plugin setup (will cause hook errors)")
            return True
        
        def cleanup(self) -> bool:
            return True
        
        @plugin_hook("process_equations", HookPriority.LOW, "Error-prone processing")
        def error_hook(self, equations: List[Dict[str, Any]], 
                      config: Dict[str, Any]) -> List[Dict[str, Any]]:
            raise ValueError("Simulated plugin error for demonstration")
    
    # Test error handling
    manager = PluginManager()
    error_plugin = ErrorPlugin()
    
    from paper2data.plugin_manager import PluginInfo
    plugin_info = PluginInfo(
        metadata=error_plugin.get_metadata(),
        status=PluginStatus.LOADED,
        file_path="error_plugin.py",
        instance=error_plugin
    )
    
    manager.plugins["error_plugin"] = plugin_info
    manager._register_plugin_hooks(plugin_info)
    
    print("Testing error handling...")
    
    # Execute hook that will fail
    results = manager.execute_hook("process_equations", [], {})
    
    print(f"✓ Error handling completed")
    print(f"  Results (should be empty): {len(results)}")
    print(f"  Plugin status: {plugin_info.status.value}")
    print(f"  Error message: {plugin_info.error_message}")

def demo_integration_example():
    """Demonstrate integration with main processing"""
    print_section("INTEGRATION EXAMPLE")
    
    print_subsection("Simulated Document Processing")
    
    # Simulate document processing with plugins
    sample_document_data = {
        "content": {
            "full_text": "This is a sample academic paper with equations E=mc^2 and complex analysis.",
            "pages": [{"text": "Page 1 content"}, {"text": "Page 2 content"}]
        },
        "equations": [
            {"content": "E = mc^2", "type": "inline", "confidence": 0.9},
            {"content": "\\int_{0}^{1} x dx", "type": "display", "confidence": 0.8}
        ],
        "metadata": {
            "title": "Sample Paper",
            "authors": ["Dr. Sample"],
            "abstract": "This is a sample paper for demonstration."
        }
    }
    
    print(f"✓ Sample document prepared")
    print(f"  Content pages: {len(sample_document_data['content']['pages'])}")
    print(f"  Equations: {len(sample_document_data['equations'])}")
    print(f"  Metadata fields: {len(sample_document_data['metadata'])}")
    
    print_subsection("Plugin-Enhanced Processing")
    
    # Initialize plugin system and load demo plugin
    manager = get_plugin_manager()
    
    # Create and register demo plugin
    demo_plugin = DemoPlugin({"enhancement_level": "advanced"})
    from paper2data.plugin_manager import PluginInfo
    
    plugin_info = PluginInfo(
        metadata=demo_plugin.get_metadata(),
        status=PluginStatus.ENABLED,
        file_path="demo_plugin.py",
        instance=demo_plugin
    )
    
    manager.plugins["demo_plugin"] = plugin_info
    manager._register_plugin_hooks(plugin_info)
    
    # Process through plugin hooks
    print("Processing equations through plugins...")
    enhanced_equations = execute_hook(
        "process_equations", 
        sample_document_data["equations"], 
        {"method": "enhanced"}
    )
    
    if enhanced_equations:
        sample_document_data["equations"] = enhanced_equations[0]
        print(f"  ✓ Equations enhanced: {len(enhanced_equations[0])}")
    
    print("Processing metadata through plugins...")
    enhanced_metadata = execute_hook(
        "enhance_metadata", 
        sample_document_data["metadata"], 
        {"method": "enhanced"}
    )
    
    if enhanced_metadata:
        sample_document_data["metadata"] = enhanced_metadata[0]
        print(f"  ✓ Metadata enhanced with demo features")
    
    print_subsection("Results Summary")
    
    # Display enhanced results
    print("Enhanced processing results:")
    print(f"  • Original equations: 2")
    print(f"  • Enhanced equations: {len(sample_document_data['equations'])}")
    print(f"  • Demo enhancements: {sum(1 for eq in sample_document_data['equations'] if eq.get('demo_enhancement'))}")
    print(f"  • Metadata demo processed: {sample_document_data['metadata'].get('demo_processed', False)}")
    print(f"  • Demo tags added: {len(sample_document_data['metadata'].get('demo_tags', []))}")

def demo_plugin_development_guide():
    """Demonstrate plugin development guide"""
    print_section("PLUGIN DEVELOPMENT GUIDE")
    
    print_subsection("Plugin Structure")
    
    plugin_template = '''
from paper2data.plugin_manager import BasePlugin, PluginMetadata, plugin_hook, HookPriority

class MyCustomPlugin(BasePlugin):
    """My custom plugin for Paper2Data"""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_custom_plugin",
            version="1.0.0",
            description="My custom plugin description",
            author="Your Name",
            license="MIT",
            hooks=["process_equations", "enhance_metadata"],
            config_schema={
                "type": "object",
                "properties": {
                    "my_parameter": {
                        "type": "string",
                        "default": "default_value"
                    }
                }
            }
        )
    
    def setup(self) -> bool:
        # Initialize plugin resources
        return True
    
    def cleanup(self) -> bool:
        # Clean up plugin resources
        return True
    
    @plugin_hook("process_equations", HookPriority.HIGH)
    def my_equation_processor(self, equations, config):
        # Process equations
        return equations
    
    @plugin_hook("enhance_metadata", HookPriority.NORMAL)
    def my_metadata_enhancer(self, metadata, config):
        # Enhance metadata
        return metadata

# Required: plugin instance
plugin_instance = MyCustomPlugin
'''
    
    print("Plugin Template:")
    print(plugin_template)
    
    print_subsection("Available Hooks")
    
    hook_names = get_all_hook_names()
    print(f"Available hooks ({len(hook_names)}):")
    
    for category in HookCategory:
        category_hooks = list_hooks_by_category(category)
        if category_hooks:
            print(f"\n  {category.value.title()} Hooks:")
            for hook_name in category_hooks:
                print(f"    • {hook_name}")
    
    print_subsection("Development Best Practices")
    
    best_practices = [
        "Always inherit from BasePlugin",
        "Implement all required methods (get_metadata, setup, cleanup)",
        "Use appropriate hook priorities",
        "Handle errors gracefully",
        "Validate configuration parameters",
        "Provide comprehensive metadata",
        "Use descriptive hook descriptions",
        "Test plugin thoroughly",
        "Document plugin functionality",
        "Follow naming conventions (*_plugin.py)"
    ]
    
    print("Plugin Development Best Practices:")
    for i, practice in enumerate(best_practices, 1):
        print(f"  {i:2d}. {practice}")

def main():
    """Main demo function"""
    print("🚀 Starting Paper2Data Plugin System Demo")
    
    try:
        # Run all demonstrations
        demo_plugin_system_overview()
        demo_hook_system()
        demo_plugin_creation()
        manager = demo_plugin_management()
        demo_hook_execution(manager)
        demo_plugin_statistics(manager)
        demo_error_handling()
        demo_integration_example()
        demo_plugin_development_guide()
        
        print_section("DEMO COMPLETED SUCCESSFULLY! 🎉")
        print("The Paper2Data plugin system provides comprehensive extensibility")
        print("for academic paper processing with:")
        print("• Dynamic plugin loading and management")
        print("• Flexible hook-based architecture")
        print("• Robust error handling")
        print("• Performance monitoring")
        print("• Easy plugin development")
        print("\nReady to extend Paper2Data with your own plugins!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 