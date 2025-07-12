#!/usr/bin/env node

/**
 * Paper2Data CLI - Main entry point
 * 
 * Command-line interface for converting academic papers to structured data repositories.
 */

const { Command } = require('commander')
const chalk = require('chalk')
const packageJson = require('../package.json')

const program = new Command()

// Global CLI setup
program
  .name('paper2data')
  .description('Convert academic papers (PDF, arXiv, DOI) into structured data repositories')
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
  
  program.addCommand(initCommand)
  program.addCommand(convertCommand)
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
  program.outputHelp()
} 