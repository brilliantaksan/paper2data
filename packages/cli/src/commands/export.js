/**
 * Paper2Data CLI - Export Command v1.1
 *
 * Multi-format export command for converting processed papers to various formats.
 * Includes HTML, LaTeX, Word, EPUB, and Markdown export with professional templates.
 */

const { Command } = require('commander')
const chalk = require('chalk')
const ora = require('ora')
const { spawn } = require('child_process')
const fs = require('fs-extra')
const path = require('path')

// Helper function to call Python export system
async function callPythonExporter (command, options = {}) {
  return new Promise((resolve, reject) => {
    const pythonArgs = ['-m', 'paper2data', 'export', command]

    // Add options
    if (options.input) {
      pythonArgs.push('--input', options.input)
    }

    if (options.output) {
      pythonArgs.push('--output', options.output)
    }

    if (options.format) {
      pythonArgs.push('--format', options.format)
    }

    if (options.template) {
      pythonArgs.push('--template', options.template)
    }

    if (options.theme) {
      pythonArgs.push('--theme', options.theme)
    }

    if (options.includeFigures) {
      pythonArgs.push('--include-figures')
    }

    if (options.includeTables) {
      pythonArgs.push('--include-tables')
    }

    if (options.includeEquations) {
      pythonArgs.push('--include-equations')
    }

    if (options.includeMetadata) {
      pythonArgs.push('--include-metadata')
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
          reject(new Error(`Failed to parse exporter output: ${e.message}`))
        }
      } else {
        let errorMessage = `Exporter exited with code ${code}`
        if (stderr) {
          errorMessage += `\nError output: ${stderr}`
        }
        reject(new Error(errorMessage))
      }
    })

    pythonProcess.on('error', (err) => {
      reject(new Error(`Failed to start exporter: ${err.message}`))
    })
  })
}

// Create export command
const exportCommand = new Command('export')
  .description('Export processed papers to multiple formats with v1.1 enhanced templates')
  .option('--verbose', 'Enable verbose output')

// Single format export subcommand
const singleCommand = new Command('single')
  .description('Export to a single format')
  .argument('<input>', 'Input directory (processed paper repository)')
  .argument('<format>', 'Output format: html, latex, word, epub, markdown')
  .option('-o, --output <file>', 'Output file path')
  .option('-t, --template <template>', 'Template theme: academic, modern, minimal, presentation', 'academic')
  .option('--include-figures', 'Include figures in export', true)
  .option('--no-include-figures', 'Exclude figures from export')
  .option('--include-tables', 'Include tables in export', true)
  .option('--no-include-tables', 'Exclude tables from export')
  .option('--include-equations', 'Include equations in export', true)
  .option('--no-include-equations', 'Exclude equations from export')
  .option('--include-metadata', 'Include metadata in export', true)
  .option('--no-include-metadata', 'Exclude metadata from export')
  .action(async (input, format, options) => {
    console.log(chalk.blue('📤 Paper2Data Exporter v1.1'))
    console.log(chalk.gray('Input:'), input)
    console.log(chalk.gray('Format:'), format.toUpperCase())
    console.log(chalk.gray('Template:'), options.template)
    console.log(chalk.gray('Output:'), options.output || 'auto-generated')
    console.log()

    const spinner = ora('Starting export...').start()

    try {
      // Validate input directory
      if (!await fs.pathExists(input)) {
        throw new Error(`Input directory not found: ${input}`)
      }

      const result = await callPythonExporter('single', {
        input,
        format,
        output: options.output,
        template: options.template,
        includeFigures: options.includeFigures,
        includeTables: options.includeTables,
        includeEquations: options.includeEquations,
        includeMetadata: options.includeMetadata,
        verbose: options.verbose
      })

      if (result.success) {
        spinner.succeed('Export completed successfully!')

        console.log(chalk.green('\n✅ Export Complete!'))
        console.log(chalk.cyan('\n📤 Export Information:'))
        console.log(chalk.gray('  📄 Format:'), format.toUpperCase())
        console.log(chalk.gray('  📂 Output:'), result.output_file)
        console.log(chalk.gray('  📏 Size:'), `${(result.file_size / 1024).toFixed(1)} KB`)
        console.log(chalk.gray('  🎨 Template:'), options.template)

        if (result.content_summary) {
          console.log(chalk.cyan('\n📊 Content Summary:'))
          const summary = result.content_summary
          if (summary.sections) {
            console.log(chalk.gray('  📄 Sections:'), summary.sections)
          }
          if (summary.figures) {
            console.log(chalk.gray('  🖼️  Figures:'), summary.figures)
          }
          if (summary.tables) {
            console.log(chalk.gray('  📊 Tables:'), summary.tables)
          }
          if (summary.equations) {
            console.log(chalk.gray('  🧮 Equations:'), summary.equations)
          }
        }

        console.log(chalk.yellow('\n💡 Next steps:'))
        console.log(chalk.gray('  • Open the exported file to review the formatting'))
        console.log(chalk.gray('  • Use different templates for different use cases'))
        console.log(chalk.gray('  • Try batch export for multiple formats'))
      } else {
        spinner.fail('Export failed')
        console.error(chalk.red('Error:'), result.error)
        process.exit(1)
      }
    } catch (error) {
      spinner.fail('Export failed')
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Batch export subcommand
const batchCommand = new Command('batch')
  .description('Export to multiple formats simultaneously')
  .argument('<input>', 'Input directory (processed paper repository)')
  .option('-f, --formats <formats>', 'Comma-separated formats: html,latex,word,epub,markdown', 'html,latex,markdown')
  .option('-o, --output <directory>', 'Output directory for exports')
  .option('-t, --template <template>', 'Template theme: academic, modern, minimal, presentation', 'academic')
  .option('--include-figures', 'Include figures in exports', true)
  .option('--no-include-figures', 'Exclude figures from exports')
  .option('--include-tables', 'Include tables in exports', true)
  .option('--no-include-tables', 'Exclude tables from exports')
  .option('--include-equations', 'Include equations in exports', true)
  .option('--no-include-equations', 'Exclude equations from exports')
  .option('--include-metadata', 'Include metadata in exports', true)
  .option('--no-include-metadata', 'Exclude metadata from exports')
  .action(async (input, options) => {
    console.log(chalk.blue('📤 Paper2Data Batch Exporter v1.1'))
    console.log(chalk.gray('Input:'), input)
    console.log(chalk.gray('Formats:'), options.formats)
    console.log(chalk.gray('Template:'), options.template)
    console.log(chalk.gray('Output:'), options.output || 'auto-generated')
    console.log()

    const spinner = ora('Starting batch export...').start()

    try {
      // Validate input directory
      if (!await fs.pathExists(input)) {
        throw new Error(`Input directory not found: ${input}`)
      }

      const result = await callPythonExporter('batch', {
        input,
        formats: options.formats,
        output: options.output,
        template: options.template,
        includeFigures: options.includeFigures,
        includeTables: options.includeTables,
        includeEquations: options.includeEquations,
        includeMetadata: options.includeMetadata,
        verbose: options.verbose
      })

      if (result.success) {
        spinner.succeed('Batch export completed successfully!')

        console.log(chalk.green('\n✅ Batch Export Complete!'))
        console.log(chalk.cyan('\n📤 Exports Created:'))
        
        if (result.exports) {
          result.exports.forEach(exportInfo => {
            console.log(chalk.gray('  📤'), exportInfo.format.toUpperCase(), chalk.gray('→'), exportInfo.file)
            console.log(chalk.gray('      '), chalk.gray('Size:'), `${(exportInfo.size / 1024).toFixed(1)} KB`)
          })
        }

        if (result.total_size) {
          console.log(chalk.cyan('\n📊 Total Export Size:'), `${(result.total_size / 1024 / 1024).toFixed(1)} MB`)
        }

        console.log(chalk.yellow('\n💡 Next steps:'))
        console.log(chalk.gray('  • Review all exported formats in the output directory'))
        console.log(chalk.gray('  • Use HTML for web sharing and presentations'))
        console.log(chalk.gray('  • Use LaTeX for academic submissions'))
        console.log(chalk.gray('  • Use Word/EPUB for document sharing'))
      } else {
        spinner.fail('Batch export failed')
        console.error(chalk.red('Error:'), result.error)
        process.exit(1)
      }
    } catch (error) {
      spinner.fail('Batch export failed')
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Templates subcommand
const templatesCommand = new Command('templates')
  .description('List available export templates and themes')
  .action(async () => {
    console.log(chalk.blue('🎨 Paper2Data Export Templates v1.1'))
    console.log()

    const spinner = ora('Loading template information...').start()

    try {
      const result = await callPythonExporter('templates', {
        verbose: options.verbose
      })

      if (result.success) {
        spinner.succeed('Template information loaded!')

        if (result.templates) {
          console.log(chalk.cyan('\n📋 Available Templates:'))
          result.templates.forEach(template => {
            console.log(chalk.gray('  🎨'), template.name, chalk.gray(`(${template.category})`))
            console.log(chalk.gray('      '), template.description)
            if (template.formats) {
              console.log(chalk.gray('      '), chalk.yellow('Formats:'), template.formats.join(', '))
            }
            console.log()
          })
        }

        if (result.themes) {
          console.log(chalk.cyan('\n🎨 Available Themes:'))
          result.themes.forEach(theme => {
            console.log(chalk.gray('  🎨'), theme.name, chalk.gray(`(${theme.style})`))
            console.log(chalk.gray('      '), theme.description)
            console.log()
          })
        }
      } else {
        spinner.fail('Failed to load template information')
        console.error(chalk.red('Error:'), result.error)
        process.exit(1)
      }
    } catch (error) {
      spinner.fail('Template operation failed')
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Add subcommands to main command
exportCommand.addCommand(singleCommand)
exportCommand.addCommand(batchCommand)
exportCommand.addCommand(templatesCommand)

module.exports = exportCommand 