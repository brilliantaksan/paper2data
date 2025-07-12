/**
 * Paper2Data CLI - Convert Command
 * 
 * Main conversion command for processing academic papers.
 */

const { Command } = require('commander')
const chalk = require('chalk')
const ora = require('ora')
const path = require('path')
const { spawn } = require('child_process')
const fs = require('fs-extra')

// Helper functions
async function validateInput (input) {
  // Basic client-side validation
  if (!input || input.trim() === '') {
    throw new Error('Input cannot be empty')
  }
  
  // Check if it's a local file
  if (!input.startsWith('http') && !input.startsWith('doi:') && !input.startsWith('arxiv:')) {
    const exists = await fs.pathExists(input)
    if (!exists) {
      throw new Error(`File not found: ${input}`)
    }
  }
  
  return true
}

function detectInputType (input) {
  if (input.startsWith('http://') || input.startsWith('https://')) {
    if (input.includes('arxiv.org')) {
      return 'arXiv URL'
    }
    return 'URL'
  }
  
  if (input.startsWith('doi:') || input.startsWith('10.')) {
    return 'DOI'
  }
  
  if (input.startsWith('arxiv:')) {
    return 'arXiv ID'
  }
  
  if (input.endsWith('.pdf')) {
    return 'PDF file'
  }
  
  return 'Unknown'
}

async function callPythonParser (input, options) {
  return new Promise((resolve, reject) => {
    // Prepare Python command
    const pythonArgs = ['-m', 'paper2data', 'convert', input]
    
    // Add options
    if (options.output) {
      pythonArgs.push('--output', options.output)
    }
    
    if (options.format) {
      pythonArgs.push('--format', options.format)
    }
    
    if (options.config) {
      pythonArgs.push('--config', options.config)
    }
    
    if (options.verbose) {
      pythonArgs.push('--log-level', 'DEBUG')
    } else if (options.quiet) {
      pythonArgs.push('--log-level', 'ERROR')
    }
    
    if (options.dryRun) {
      pythonArgs.push('--dry-run')
    }
    
    if (!options.extractFigures) {
      pythonArgs.push('--no-figures')
    }
    
    if (!options.extractTables) {
      pythonArgs.push('--no-tables')
    }
    
    // Always use JSON output for programmatic processing
    pythonArgs.push('--json-output')
    
    // Spawn Python process
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
          // Filter out MuPDF errors and find the JSON response
          const lines = stdout.split('\n')
          const cleanLines = lines.filter(line => !line.startsWith('MuPDF error:'))
          const cleanOutput = cleanLines.join('\n').trim()
          
          // Look for the JSON object that starts with "success" field
          const jsonMatch = cleanOutput.match(/\{\s*"success"[\s\S]*\}(?=\s*$)/m)
          
          if (jsonMatch) {
            const jsonString = jsonMatch[0]
            const result = JSON.parse(jsonString)
            resolve(result)
          } else {
            // Fallback: find any valid JSON object at the end
            const jsonStart = cleanOutput.lastIndexOf('{\n  "success"')
            if (jsonStart >= 0) {
              const jsonEnd = cleanOutput.lastIndexOf('}')
              const jsonString = cleanOutput.substring(jsonStart, jsonEnd + 1)
              const result = JSON.parse(jsonString)
              resolve(result)
            } else {
              reject(new Error('No valid JSON response found in Python output'))
            }
          }
        } catch (e) {
          reject(new Error(`Failed to parse Python output: ${e.message}`))
        }
      } else {
        // Try to parse error output
        let errorMessage = `Python process exited with code ${code}`
        if (stderr) {
          errorMessage += `\nError output: ${stderr}`
        }
        if (stdout) {
          try {
            const errorResult = JSON.parse(stdout)
            if (errorResult.error) {
              errorMessage = errorResult.error
            }
          } catch (e) {
            // Ignore JSON parse errors for error output
          }
        }
        reject(new Error(errorMessage))
      }
    })
    
    pythonProcess.on('error', (err) => {
      if (err.code === 'ENOENT') {
        reject(new Error('Python 3 not found. Please ensure Python 3 is installed and in your PATH.'))
      } else {
        reject(new Error(`Failed to start Python process: ${err.message}`))
      }
    })
  })
}

function generateOutputPath (input) {
  const inputType = detectInputType(input)
  const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
  
  if (inputType === 'PDF file') {
    const basename = path.basename(input, '.pdf')
    return `./paper2data_output/${basename}_${timestamp}`
  } else if (inputType.includes('arXiv')) {
    // Extract arXiv ID
    let arxivId = input
    if (input.includes('arxiv.org')) {
      arxivId = input.split('/').pop().replace('.pdf', '')
    } else if (input.startsWith('arxiv:')) {
      arxivId = input.slice(6)
    }
    return `./paper2data_output/arxiv_${arxivId}_${timestamp}`
  } else {
    return `./paper2data_output/paper_${timestamp}`
  }
}

// Create convert command
const convertCommand = new Command('convert')
  .description('Convert academic paper to structured data repository')
  .argument('<input>', 'Input source: PDF file, arXiv URL, or DOI')
  .option('-o, --output <directory>', 'Output directory')
  .option('-f, --format <format>', 'Output format for metadata', 'json')
  .option('--extract-figures', 'Extract figures (default: true)', true)
  .option('--no-extract-figures', 'Skip figure extraction')
  .option('--extract-tables', 'Extract tables (default: true)', true) 
  .option('--no-extract-tables', 'Skip table extraction')
  .option('--config <file>', 'Configuration file path')
  .action(async (input, options) => {
    console.log(chalk.blue('📄 Paper2Data Converter'))
    console.log(chalk.gray('Input:'), input)
    console.log(chalk.gray('Output:'), options.output || 'auto-generated')
    console.log(chalk.gray('Format:'), options.format)
    console.log()

    const spinner = ora('Initializing conversion...').start()

    try {
      // Validate input
      spinner.text = 'Validating input source...'
      await validateInput(input)
      
      // Detect input type
      const inputType = detectInputType(input)
      spinner.text = `Detected input type: ${inputType}`
      await new Promise(resolve => setTimeout(resolve, 300))

      // Call Python parser
      spinner.text = 'Starting paper processing...'
      const result = await callPythonParser(input, options)

      if (result.success) {
        spinner.succeed('Conversion completed successfully!')

        // Display results
        console.log(chalk.green('\n✅ Conversion Complete!'))
        console.log(chalk.cyan('\nExtraction Summary:'))
        
        if (result.summary) {
          const summary = result.summary
          console.log(chalk.gray('  📄 Pages:'), summary.total_pages || 'Unknown')
          console.log(chalk.gray('  📝 Words:'), summary.total_words || 'Unknown')
          console.log(chalk.gray('  📋 Sections:'), summary.sections_found || 0)
          console.log(chalk.gray('  🖼️  Figures:'), summary.figures_found || 0)
          console.log(chalk.gray('  📊 Tables:'), summary.tables_found || 0)
          console.log(chalk.gray('  📚 References:'), summary.references_found || 0)
        }
        
        console.log(chalk.cyan('\nOutput Directory:'))
        console.log(chalk.gray('  📂'), result.output_directory)
        
        if (result.files_created) {
          console.log(chalk.cyan('\nFiles Created:'))
          const files = result.files_created
          if (files.sections > 0) {
            console.log(chalk.gray('  📄'), `${files.sections} section files`)
          }
          if (files.figures > 0) {
            console.log(chalk.gray('  🖼️ '), `${files.figures} figure files`)
          }
          if (files.tables > 0) {
            console.log(chalk.gray('  📊'), `${files.tables} table files`)
          }
          console.log(chalk.gray('  📋'), `${files.metadata_files} metadata files`)
          console.log(chalk.gray('  📖'), '1 README file')
        }
        
        console.log(chalk.yellow('\n💡 Next steps:'))
        console.log(chalk.gray('  • Review extracted content in the output directory'))
        console.log(chalk.gray('  • Check the README.md for an overview'))
        console.log(chalk.gray('  • Validate figures and tables for accuracy'))
        
      } else {
        spinner.fail('Conversion failed')
        console.error(chalk.red('\n❌ Conversion Failed'))
        if (result.error) {
          console.error(chalk.red('Error:'), result.error)
        }
        process.exit(1)
      }

    } catch (error) {
      spinner.fail('Conversion failed')
      console.error(chalk.red('\n❌ Conversion Failed'))
      console.error(chalk.red('Error:'), error.message)
      
      // Provide helpful error messages
      if (error.message.includes('Python 3 not found')) {
        console.log(chalk.yellow('\n💡 Installation Help:'))
        console.log(chalk.gray('  • Install Python 3: https://python.org/downloads'))
        console.log(chalk.gray('  • Ensure Python is in your PATH'))
        console.log(chalk.gray('  • Try running: python3 --version'))
      } else if (error.message.includes('File not found')) {
        console.log(chalk.yellow('\n💡 Input Help:'))
        console.log(chalk.gray('  • Check that the file path is correct'))
        console.log(chalk.gray('  • Use absolute paths for files outside current directory'))
        console.log(chalk.gray('  • Supported formats: PDF files, arXiv URLs, DOIs'))
      } else if (error.message.includes('Invalid') || error.message.includes('validation')) {
        console.log(chalk.yellow('\n💡 Input Help:'))
        console.log(chalk.gray('  • Ensure PDF is not corrupted or password-protected'))
        console.log(chalk.gray('  • Check that URLs are accessible'))
        console.log(chalk.gray('  • Verify DOI format (e.g., 10.1000/182)'))
      }
      
      process.exit(1)
    }
  })

// Add validation subcommand
const validateCommand = new Command('validate')
  .description('Validate input without processing')
  .argument('<input>', 'Input source to validate')
  .action(async (input) => {
    console.log(chalk.blue('🔍 Input Validation'))
    console.log(chalk.gray('Input:'), input)
    console.log()

    const spinner = ora('Validating input...').start()

    try {
      // Call Python validator
      const result = await new Promise((resolve, reject) => {
        const pythonArgs = ['-m', 'paper2data', 'validate', input, '--json-output']
        
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
          try {
            const result = JSON.parse(stdout)
            resolve(result)
          } catch (e) {
            reject(new Error(`Failed to parse validation result: ${e.message}`))
          }
        })
        
        pythonProcess.on('error', (err) => {
          reject(new Error(`Validation failed: ${err.message}`))
        })
      })

      if (result.valid) {
        spinner.succeed('Input validation successful!')
        console.log(chalk.green('\n✅ Input is valid'))
        
        if (result.metadata) {
          console.log(chalk.cyan('\nInput Information:'))
          const meta = result.metadata
          if (meta.page_count) {
            console.log(chalk.gray('  📄 Pages:'), meta.page_count)
          }
          if (meta.title) {
            console.log(chalk.gray('  📝 Title:'), meta.title)
          }
          if (meta.author) {
            console.log(chalk.gray('  👤 Author:'), meta.author)
          }
          if (meta.file_size) {
            console.log(chalk.gray('  💾 Size:'), `${(meta.file_size / 1024).toFixed(1)} KB`)
          }
        }
      } else {
        spinner.fail('Input validation failed')
        console.error(chalk.red('\n❌ Input is invalid'))
        if (result.error) {
          console.error(chalk.red('Error:'), result.error)
        }
        process.exit(1)
      }

    } catch (error) {
      spinner.fail('Validation failed')
      console.error(chalk.red('\n❌ Validation failed'))
      console.error(chalk.red('Error:'), error.message)
      process.exit(1)
    }
  })

// Add subcommands
convertCommand.addCommand(validateCommand)

module.exports = convertCommand 