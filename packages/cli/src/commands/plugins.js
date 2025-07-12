/**
 * Paper2Data CLI - Plugins Command v1.1
 *
 * Plugin management command for the enhanced plugin system.
 * Includes marketplace integration, dependency management, and plugin operations.
 */

const { Command } = require('commander')
const chalk = require('chalk')
const ora = require('ora')
const { spawn } = require('child_process')

// Helper function to call Python plugin manager
async function callPythonPluginManager (command, options = {}) {
  return new Promise((resolve, reject) => {
    const pythonArgs = ['-m', 'paper2data', 'plugins', command]

    // Add options
    if (options.plugin) {
      pythonArgs.push('--plugin', options.plugin)
    }

    if (options.repository) {
      pythonArgs.push('--repository', options.repository)
    }

    if (options.version) {
      pythonArgs.push('--version', options.version)
    }

    if (options.force) {
      pythonArgs.push('--force')
    }

    if (options.verbose) {
      pythonArgs.push('--verbose')
    }

    // Always use JSON output
    pythonArgs.push('--json-output')

    const pythonProcess = spawn('python3', pythonArgs, {
      stdio: ['pipe', 'pipe', 'pipe']
    })

    let stdout = ''
    let stderr = ''

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString()
    })

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout)
          resolve(result)
        } catch (e) {
          reject(new Error(`Failed to parse plugin manager output: ${e.message}`))
        }
      } else {
        let errorMessage = `Plugin manager exited with code ${code}`
        if (stderr) {
          errorMessage += `\nError output: ${stderr}`
        }
        reject(new Error(errorMessage))
      }
    })

    pythonProcess.on('error', (err) => {
      reject(new Error(`Failed to start plugin manager: ${err.message}`))
    })
  })
}

// Create plugins command
const pluginsCommand = new Command('plugins')
  .description('Manage Paper2Data v1.1 enhanced plugin system')
  .option('--verbose', 'Enable verbose output')

// List subcommand
const listCommand = new Command('list')
  .description('List installed plugins')
  .option('--installed', 'Show only installed plugins')
  .option('--available', 'Show only available plugins from marketplace')
  .action(async (options) => {
    console.log(chalk.blue('🔌 Paper2Data Plugin Manager v1.1'))
    console.log()

    const spinner = ora('Loading plugin information...').start()

    try {
      const result = await callPythonPluginManager('list', options)

      if (result.success) {
        spinner.succeed('Plugin information loaded successfully!')

        if (result.installed_plugins && result.installed_plugins.length > 0) {
          console.log(chalk.cyan('\n📦 Installed Plugins:'))
          result.installed_plugins.forEach(plugin => {
            const status = plugin.enabled ? chalk.green('✓') : chalk.red('✗')
            console.log(chalk.gray('  '), status, plugin.name, chalk.gray(`(${plugin.version})`))
            if (plugin.description) {
              console.log(chalk.gray('      '), plugin.description)
            }
          })
        }

        if (result.available_plugins && result.available_plugins.length > 0) {
          console.log(chalk.cyan('\n🛒 Available Plugins:'))
          result.available_plugins.forEach(plugin => {
            console.log(chalk.gray('  📦'), plugin.name, chalk.gray(`(${plugin.version})`))
            if (plugin.description) {
              console.log(chalk.gray('      '), plugin.description)
            }
            if (plugin.downloads) {
              console.log(chalk.gray('      '), chalk.yellow('Downloads:'), plugin.downloads)
            }
          })
        }

        if (result.marketplace_stats) {
          console.log(chalk.cyan('\n📊 Marketplace Statistics:'))
          const stats = result.marketplace_stats
          console.log(chalk.gray('  🏪 Total Plugins:'), stats.total_plugins || 0)
          console.log(chalk.gray('  📥 Total Downloads:'), stats.total_downloads || 0)
          console.log(chalk.gray('  👥 Contributors:'), stats.contributors || 0)
        }
      } else {
        spinner.fail('Failed to load plugin information')
        console.error(chalk.red('Error:'), result.error)
        process.exit(1)
      }
    } catch (error) {
      spinner.fail('Plugin operation failed')
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Install subcommand
const installCommand = new Command('install')
  .description('Install a plugin from marketplace or local source')
  .argument('<plugin>', 'Plugin name or path to plugin file')
  .option('-v, --version <version>', 'Specific version to install')
  .option('--force', 'Force installation even if conflicts exist')
  .action(async (plugin, options) => {
    console.log(chalk.blue('🔌 Paper2Data Plugin Installer v1.1'))
    console.log(chalk.gray('Plugin:'), plugin)
    if (options.version) {
      console.log(chalk.gray('Version:'), options.version)
    }
    console.log()

    const spinner = ora('Installing plugin...').start()

    try {
      const result = await callPythonPluginManager('install', {
        plugin,
        version: options.version,
        force: options.force,
        verbose: options.verbose
      })

      if (result.success) {
        spinner.succeed('Plugin installed successfully!')

        console.log(chalk.green('\n✅ Installation Complete!'))
        console.log(chalk.cyan('\n📦 Plugin Information:'))
        console.log(chalk.gray('  📦 Name:'), result.plugin_info.name)
        console.log(chalk.gray('  📋 Version:'), result.plugin_info.version)
        console.log(chalk.gray('  👤 Author:'), result.plugin_info.author)
        console.log(chalk.gray('  📝 Description:'), result.plugin_info.description)

        if (result.dependencies_installed) {
          console.log(chalk.cyan('\n🔗 Dependencies:'))
          result.dependencies_installed.forEach(dep => {
            console.log(chalk.gray('  📦'), dep.name, chalk.gray(`(${dep.version})`))
          })
        }

        if (result.configuration_required) {
          console.log(chalk.yellow('\n⚙️  Configuration Required:'))
          console.log(chalk.gray('  • Run: paper2data plugins configure'), result.plugin_info.name)
          console.log(chalk.gray('  • Check plugin documentation for setup instructions'))
        }

        console.log(chalk.yellow('\n💡 Next steps:'))
        console.log(chalk.gray('  • Run: paper2data plugins list to see all installed plugins'))
        console.log(chalk.gray('  • Use: paper2data convert --plugins'), result.plugin_info.name, 'to use the plugin')
      } else {
        spinner.fail('Plugin installation failed')
        console.error(chalk.red('Error:'), result.error)
        process.exit(1)
      }
    } catch (error) {
      spinner.fail('Installation failed')
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Uninstall subcommand
const uninstallCommand = new Command('uninstall')
  .description('Uninstall a plugin')
  .argument('<plugin>', 'Plugin name to uninstall')
  .option('--force', 'Force uninstallation without confirmation')
  .action(async (plugin, options) => {
    console.log(chalk.blue('🔌 Paper2Data Plugin Uninstaller v1.1'))
    console.log(chalk.gray('Plugin:'), plugin)
    console.log()

    const spinner = ora('Uninstalling plugin...').start()

    try {
      const result = await callPythonPluginManager('uninstall', {
        plugin,
        force: options.force,
        verbose: options.verbose
      })

      if (result.success) {
        spinner.succeed('Plugin uninstalled successfully!')

        console.log(chalk.green('\n✅ Uninstallation Complete!'))
        console.log(chalk.cyan('\n🗑️  Removed:'))
        console.log(chalk.gray('  📦 Plugin:'), result.plugin_info.name)
        console.log(chalk.gray('  📋 Version:'), result.plugin_info.version)

        if (result.dependencies_removed) {
          console.log(chalk.cyan('\n🔗 Dependencies Removed:'))
          result.dependencies_removed.forEach(dep => {
            console.log(chalk.gray('  📦'), dep.name, chalk.gray(`(${dep.version})`))
          })
        }
      } else {
        spinner.fail('Plugin uninstallation failed')
        console.error(chalk.red('Error:'), result.error)
        process.exit(1)
      }
    } catch (error) {
      spinner.fail('Uninstallation failed')
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Update subcommand
const updateCommand = new Command('update')
  .description('Update plugins to latest versions')
  .argument('[plugin]', 'Specific plugin to update (optional)')
  .option('--all', 'Update all plugins')
  .option('--check-only', 'Check for updates without installing')
  .action(async (plugin, options) => {
    console.log(chalk.blue('🔌 Paper2Data Plugin Updater v1.1'))
    if (plugin) {
      console.log(chalk.gray('Plugin:'), plugin)
    } else {
      console.log(chalk.gray('Mode:'), options.all ? 'All plugins' : 'Check only')
    }
    console.log()

    const spinner = ora('Checking for updates...').start()

    try {
      const result = await callPythonPluginManager('update', {
        plugin,
        all: options.all,
        check_only: options.checkOnly,
        verbose: options.verbose
      })

      if (result.success) {
        if (options.checkOnly) {
          spinner.succeed('Update check completed!')

          if (result.updates_available && result.updates_available.length > 0) {
            console.log(chalk.cyan('\n📦 Updates Available:'))
            result.updates_available.forEach(update => {
              console.log(chalk.gray('  📦'), update.name, chalk.gray(`${update.current_version} → ${update.latest_version}`))
              if (update.changelog) {
                console.log(chalk.gray('      '), update.changelog)
              }
            })
          } else {
            console.log(chalk.green('\n✅ All plugins are up to date!'))
          }
        } else {
          spinner.succeed('Plugin updates completed!')

          console.log(chalk.green('\n✅ Updates Complete!'))
          if (result.plugins_updated) {
            console.log(chalk.cyan('\n📦 Updated Plugins:'))
            result.plugins_updated.forEach(update => {
              console.log(chalk.gray('  📦'), update.name, chalk.gray(`${update.old_version} → ${update.new_version}`))
            })
          }
        }
      } else {
        spinner.fail('Plugin update failed')
        console.error(chalk.red('Error:'), result.error)
        process.exit(1)
      }
    } catch (error) {
      spinner.fail('Update failed')
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Add subcommands to main command
pluginsCommand.addCommand(listCommand)
pluginsCommand.addCommand(installCommand)
pluginsCommand.addCommand(uninstallCommand)
pluginsCommand.addCommand(updateCommand)

module.exports = pluginsCommand 