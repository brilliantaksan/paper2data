#!/usr/bin/env node

/**
 * Paper2Data CLI v1.1 - Main entry point
 * 
 * Enhanced command-line interface for converting academic papers to structured data repositories.
 * Includes v1.1 features: plugin system, multi-format export, mathematical processing, and advanced figure processing.
 */

const { Command } = require('commander')
const chalk = require('chalk')
const packageJson = require('../package.json')

const program = new Command()

// Global CLI setup
program
  .name('paper2data')
  .description('Convert academic papers (PDF, arXiv, DOI) into structured data repositories with v1.1 enhanced features')
  .version(packageJson.version, '-v, --version', 'display version number')
  .helpOption('-h, --help', 'display help for command')

// Global options
program
  .option('--verbose', 'enable verbose output')
  .option('--quiet', 'suppress non-essential output')
  .option('-c, --config <file>', 'use custom configuration file')
  .option('--dry-run', 'show what would be done without executing')

// Import and register commands
try {
  const initCommand = require('./commands/init')
  const convertCommand = require('./commands/convert')
  const pluginsCommand = require('./commands/plugins')
  const exportCommand = require('./commands/export')
  
  program.addCommand(initCommand)
  program.addCommand(convertCommand)
  program.addCommand(pluginsCommand)
  program.addCommand(exportCommand)
} catch (error) {
  console.error(chalk.red('Error loading commands:'), error.message)
  process.exit(1)
}

// Error handling
program.exitOverride()

try {
  program.parse()
} catch (error) {
  console.error(chalk.red('CLI Error:'), error.message)
  process.exit(1)
}

// Handle no command case
if (!process.argv.slice(2).length) {
  console.log(chalk.blue('📄 Paper2Data CLI v1.1'))
  console.log(chalk.gray('Enterprise-grade academic paper processing with enhanced plugin system'))
  console.log()
  program.outputHelp()
  
  console.log(chalk.yellow('\n💡 Quick Start Examples:'))
  console.log(chalk.gray('  • paper2data convert paper.pdf --format all --template academic'))
  console.log(chalk.gray('  • paper2data convert arxiv:2103.15522 --metadata enhanced'))
  console.log(chalk.gray('  • paper2data plugins list'))
  console.log(chalk.gray('  • paper2data export batch ./paper_output --formats html,latex,word'))
  console.log()
} 