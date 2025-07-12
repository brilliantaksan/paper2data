# Paper2Data Enhanced Plugin System v1.1

## Overview

The Enhanced Plugin System v1.1 provides a comprehensive plugin architecture for Paper2Data with advanced dependency management, marketplace integration, and lifecycle management capabilities. This system builds upon the existing plugin foundation to provide enterprise-grade plugin management.

## 🚀 Key Features

### Core Capabilities
- **Dynamic Plugin Loading**: Automatic discovery and loading of plugins from directories
- **Dependency Resolution**: Sophisticated dependency management with version constraints
- **Marketplace Integration**: Plugin discovery, installation, and updates from community marketplace
- **Health Monitoring**: Real-time monitoring of plugin health and performance
- **Automatic Updates**: Background monitoring for plugin updates with automatic installation
- **Version Management**: Semantic versioning support with conflict resolution
- **Security Validation**: Security scanning and validation of plugins before installation

### Advanced Features
- **Plugin Lifecycle Management**: Complete install/update/uninstall workflow
- **Performance Monitoring**: Real-time metrics and performance tracking
- **Configuration Management**: Dynamic plugin configuration with validation
- **Community Features**: Rating, reviews, and plugin recommendations
- **System Integration**: Seamless integration with existing Paper2Data components

## 🏗️ Architecture

### System Components

```
Enhanced Plugin System
├── Plugin Manager (Core)
├── Dependency Manager (New)
├── Plugin Marketplace (New)
├── Health Monitor (New)
├── Auto-Update System (New)
└── Configuration Manager
```

### Component Responsibilities

1. **Plugin Manager**: Core plugin loading, execution, and hook management
2. **Dependency Manager**: Resolves plugin dependencies and version conflicts
3. **Plugin Marketplace**: Handles plugin discovery, installation, and community features
4. **Health Monitor**: Monitors plugin health and performance metrics
5. **Auto-Update System**: Manages automatic plugin updates
6. **Configuration Manager**: Handles plugin configuration and validation

## 📦 Installation

### Prerequisites

```bash
# Install required dependencies
pip install semver networkx packaging schedule aiohttp
```

### Basic Setup

```python
from paper2data import initialize_enhanced_plugin_system

# Initialize with default configuration
plugin_system = initialize_enhanced_plugin_system()

# Or with custom configuration
config = {
    "plugin_dirs": ["./plugins", "./community_plugins"],
    "health_monitoring_enabled": True,
    "auto_update_enabled": True,
    "marketplace_config": {
        "marketplace_url": "https://marketplace.paper2data.dev",
        "api_key": "your_api_key_here"
    }
}
plugin_system = initialize_enhanced_plugin_system(config)
```

## 🔧 Usage Guide

### Basic Plugin Management

```python
from paper2data import get_enhanced_plugin_system
import asyncio

# Get the plugin system instance
system = get_enhanced_plugin_system()

# Search for plugins
results = system.search_plugins("latex", min_rating=4.0)
for plugin in results:
    print(f"Found: {plugin.name} v{plugin.version} - {plugin.description}")

# Install a plugin
await system.install_plugin("latex-processor", version="1.2.0")

# Update a plugin
await system.update_plugin("latex-processor")

# Uninstall a plugin
await system.uninstall_plugin("latex-processor")
```

### Advanced Plugin Management

```python
# Get comprehensive plugin status
status = system.get_plugin_status("latex-processor")
print(f"Plugin health: {status['health']['status']}")
print(f"Performance score: {status['health']['performance_score']}")

# Get system metrics
metrics = system.get_system_metrics()
print(f"Total plugins: {metrics.total_plugins}")
print(f"Active plugins: {metrics.active_plugins}")
print(f"Average response time: {metrics.avg_response_time}ms")

# Get plugin recommendations
recommendations = system.get_plugin_recommendations("extraction")
for plugin in recommendations:
    print(f"Recommended: {plugin.name} - {plugin.stats.average_rating}⭐")
```

### Dependency Management

```python
from paper2data import DependencyManager, VersionConstraint

# Initialize dependency manager
dep_manager = DependencyManager()

# Add a package with dependencies
deps = [
    VersionConstraint("numpy", ">=1.20.0"),
    VersionConstraint("pandas", ">=1.3.0")
]
dep_manager.add_package("data-processor", "1.0.0", dependencies=deps)

# Resolve dependencies
resolution = dep_manager.resolve_dependencies(["data-processor"])
if resolution.success:
    print("Install order:", resolution.install_order)
else:
    print("Conflicts:", resolution.conflicts)
```

### Marketplace Integration

```python
from paper2data import get_marketplace
import asyncio

# Get marketplace instance
marketplace = get_marketplace()

# Refresh plugin list from marketplace
await marketplace.refresh_plugin_list()

# Search for plugins
results = marketplace.search_plugins("pdf processing")

# Get plugin details
plugin = marketplace.get_plugin_details("pdf-extractor")
print(f"Downloads: {plugin.stats.downloads}")
print(f"Rating: {plugin.stats.average_rating}⭐")

# Submit a rating
await marketplace.submit_rating("pdf-extractor", 5, "Excellent plugin!")
```

## 🔌 Plugin Development

### Creating a Plugin

```python
from paper2data import BasePlugin, PluginMetadata, plugin_hook, HookPriority

class MyPlugin(BasePlugin):
    """Example plugin implementation"""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my-plugin",
            version="1.0.0",
            description="My awesome plugin",
            author="Your Name",
            license="MIT",
            dependencies=["numpy>=1.20.0"],
            hooks=["process_text", "analyze_content"]
        )
    
    def setup(self) -> bool:
        """Initialize plugin resources"""
        self.logger.info("Plugin setup complete")
        return True
    
    def cleanup(self) -> bool:
        """Clean up plugin resources"""
        self.logger.info("Plugin cleanup complete")
        return True
    
    @plugin_hook("process_text", HookPriority.HIGH)
    def process_text_hook(self, text: str, config: dict) -> str:
        """Process text content"""
        # Your processing logic here
        return text.upper()
    
    @plugin_hook("analyze_content", HookPriority.NORMAL)
    def analyze_content_hook(self, content: dict) -> dict:
        """Analyze content"""
        # Your analysis logic here
        return {"word_count": len(content.get("text", "").split())}
```

### Plugin Configuration

```python
def get_config_schema(self) -> dict:
    """Define plugin configuration schema"""
    return {
        "type": "object",
        "properties": {
            "processing_mode": {
                "type": "string",
                "enum": ["fast", "thorough"],
                "default": "fast"
            },
            "max_file_size": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000,
                "default": 100
            }
        },
        "required": ["processing_mode"]
    }

def validate_config(self, config: dict) -> bool:
    """Validate plugin configuration"""
    if "processing_mode" not in config:
        return False
    return config["processing_mode"] in ["fast", "thorough"]
```

## 🔒 Security Features

### Security Scanning

The marketplace automatically scans plugins for security issues:

```python
# Check plugin security status
plugin = marketplace.get_plugin_details("some-plugin")
security = plugin.security_scan

if security.status == SecurityStatus.DANGER:
    print("⚠️ Security issues found:")
    for issue in security.issues:
        print(f"  - {issue}")
else:
    print(f"✅ Security score: {security.score}/100")
```

### Safe Installation

```python
# Install with security validation
await system.install_plugin("plugin-name", force=False)  # Will fail if security issues

# Force install (bypass security - not recommended)
await system.install_plugin("plugin-name", force=True)
```

## 📊 Monitoring and Analytics

### Health Monitoring

```python
# Get plugin health information
health = system.plugin_health.get("plugin-name")
if health:
    print(f"Status: {health.status}")
    print(f"Performance score: {health.performance_score}")
    print(f"Last check: {health.last_check}")
    if health.errors:
        print("Errors:", health.errors)
```

### Performance Metrics

```python
# Get system-wide metrics
metrics = system.get_system_metrics()

print(f"System uptime: {metrics.uptime}")
print(f"Total plugins: {metrics.total_plugins}")
print(f"Active plugins: {metrics.active_plugins}")
print(f"Failed plugins: {metrics.failed_plugins}")
print(f"Average response time: {metrics.avg_response_time}ms")
```

### Export System State

```python
# Export complete system state for debugging
system.export_system_state("system_state.json")

# The exported JSON includes:
# - System configuration
# - Plugin status and health
# - Performance metrics
# - Dependency information
```

## 🎯 Configuration Options

### System Configuration

```python
config = {
    # Plugin directories
    "plugin_dirs": ["./plugins", "./community_plugins"],
    
    # Health monitoring
    "health_monitoring_enabled": True,
    "health_check_interval": 300,  # 5 minutes
    
    # Auto-update settings
    "auto_update_enabled": True,
    "update_check_interval": 3600,  # 1 hour
    
    # Performance settings
    "max_metrics_history": 1000,
    
    # Dependency management
    "dependency_config": {
        "conflict_resolution": "latest",  # latest, conservative, strict
        "installed_packages_file": "installed_packages.json",
        "package_registry_file": "package_registry.json"
    },
    
    # Marketplace settings
    "marketplace_config": {
        "marketplace_url": "https://marketplace.paper2data.dev",
        "api_key": "your_api_key",
        "cache_dir": "./plugin_cache",
        "security_enabled": True
    }
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Plugin Not Loading**
   ```python
   # Check plugin health
   health = system.plugin_health.get("plugin-name")
   if health and health.errors:
       print("Plugin errors:", health.errors)
   ```

2. **Dependency Conflicts**
   ```python
   # Resolve dependencies manually
   resolution = dep_manager.resolve_dependencies(["plugin-name"])
   if resolution.conflicts:
       print("Conflicts found:", resolution.conflicts)
   ```

3. **Marketplace Connection Issues**
   ```python
   # Test marketplace connection
   success = await marketplace.refresh_plugin_list()
   if not success:
       print("Cannot connect to marketplace")
   ```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Export system state for analysis
system.export_system_state("debug_state.json")
```

## 🔄 Migration Guide

### From Basic Plugin System

```python
# Old way
from paper2data import PluginManager
manager = PluginManager()
manager.load_plugins_from_directory("./plugins")

# New way
from paper2data import initialize_enhanced_plugin_system
system = initialize_enhanced_plugin_system({
    "plugin_dirs": ["./plugins"]
})
```

### Updating Existing Plugins

Existing plugins are compatible with the enhanced system. To take advantage of new features:

1. Add dependency information to plugin metadata
2. Implement health check methods
3. Add configuration validation
4. Update to use new hook system

## 📚 API Reference

### Core Classes

- `EnhancedPluginSystem`: Main system coordinator
- `DependencyManager`: Dependency resolution and management
- `PluginMarketplace`: Marketplace integration
- `PluginHealth`: Health monitoring data
- `SystemMetrics`: System-wide metrics

### Key Methods

- `install_plugin(name, version=None)`: Install plugin from marketplace
- `uninstall_plugin(name, force=False)`: Uninstall plugin
- `update_plugin(name)`: Update plugin to latest version
- `search_plugins(query, **filters)`: Search marketplace
- `get_plugin_status(name)`: Get comprehensive plugin status
- `get_system_metrics()`: Get system metrics

## 🎉 Examples

### Example 1: Plugin Discovery and Installation

```python
import asyncio
from paper2data import initialize_enhanced_plugin_system

async def main():
    system = initialize_enhanced_plugin_system()
    
    # Search for PDF processing plugins
    results = system.search_plugins("pdf", min_rating=4.0)
    
    for plugin in results[:3]:  # Top 3 results
        print(f"Installing {plugin.name} v{plugin.version}")
        await system.install_plugin(plugin.name)
        print(f"✅ Installed successfully")

asyncio.run(main())
```

### Example 2: Health Monitoring

```python
from paper2data import get_enhanced_plugin_system
import time

system = get_enhanced_plugin_system()

# Monitor plugin health
while True:
    for plugin_name, health in system.plugin_health.items():
        if health.status != "healthy":
            print(f"⚠️ {plugin_name}: {health.status}")
            print(f"   Errors: {health.errors}")
        else:
            print(f"✅ {plugin_name}: OK (score: {health.performance_score:.2f})")
    
    time.sleep(60)  # Check every minute
```

### Example 3: Automated Plugin Management

```python
import asyncio
from paper2data import initialize_enhanced_plugin_system

async def auto_manage_plugins():
    config = {
        "auto_update_enabled": True,
        "health_monitoring_enabled": True,
        "marketplace_config": {
            "api_key": "your_api_key"
        }
    }
    
    system = initialize_enhanced_plugin_system(config)
    
    # System will automatically:
    # - Check for updates hourly
    # - Monitor plugin health
    # - Install security updates
    # - Generate health reports
    
    print("🚀 Automated plugin management started")
    
    # Keep system running
    while True:
        await asyncio.sleep(3600)  # Check every hour

asyncio.run(auto_manage_plugins())
```

## 🤝 Contributing

To contribute to the Enhanced Plugin System:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Development Setup

```bash
# Clone repository
git clone https://github.com/paper2data/paper2data.git
cd paper2data/packages/parser

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest src/paper2data/test_plugin_system_enhanced.py -v
```

## 📝 License

The Enhanced Plugin System is part of Paper2Data and is licensed under the MIT License.

## 🔗 Links

- [Paper2Data Documentation](https://paper2data.readthedocs.io)
- [Plugin Marketplace](https://marketplace.paper2data.dev)
- [GitHub Repository](https://github.com/paper2data/paper2data)
- [Issue Tracker](https://github.com/paper2data/paper2data/issues)

---

*Enhanced Plugin System v1.1 - Powering the next generation of Paper2Data extensibility* 