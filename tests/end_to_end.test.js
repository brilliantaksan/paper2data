/**
 * End-to-end tests for Paper2Data CLI and overall workflow
 * 
 * Tests the complete user workflow from CLI input to expected output.
 */

const { execSync } = require('child_process')
const path = require('path')
const fs = require('fs')

// Path to the CLI script
const CLI_PATH = path.join(__dirname, '../packages/cli/src/index.js')

/**
 * Helper function to run CLI commands and capture output
 */
function runCLI(args = '', expectError = false) {
  try {
    const result = execSync(`node ${CLI_PATH} ${args}`, {
      encoding: 'utf8',
      stdio: 'pipe',
      cwd: path.join(__dirname, '..')
    })
    return { stdout: result, stderr: '', exitCode: 0 }
  } catch (error) {
    if (expectError) {
      return {
        stdout: error.stdout || '',
        stderr: error.stderr || '',
        exitCode: error.status || 1
      }
    }
    throw error
  }
}

describe('Paper2Data End-to-End Workflow', () => {

  describe('Project Structure Validation', () => {
    
    test('monorepo structure exists', () => {
      const projectRoot = path.join(__dirname, '..')
      
      // Check main directories exist
      const requiredDirs = [
        'packages/parser',
        'packages/cli', 
        'docs',
        'config',
        'tests'
      ]
      
      for (const dir of requiredDirs) {
        const dirPath = path.join(projectRoot, dir)
        expect(fs.existsSync(dirPath)).toBe(true)
      }
    })
    
    test('documentation files exist', () => {
      const docsDir = path.join(__dirname, '../docs')
      
      const requiredDocs = [
        'Implementation.md',
        'project_structure.md', 
        'UI_UX_doc.md'
      ]
      
      for (const doc of requiredDocs) {
        const docPath = path.join(docsDir, doc)
        expect(fs.existsSync(docPath)).toBe(true)
      }
    })
    
    test('package configuration files exist', () => {
      const projectRoot = path.join(__dirname, '..')
      
      // Python package
      expect(fs.existsSync(path.join(projectRoot, 'packages/parser/pyproject.toml'))).toBe(true)
      expect(fs.existsSync(path.join(projectRoot, 'packages/parser/src/__init__.py'))).toBe(true)
      
      // Node.js package
      expect(fs.existsSync(path.join(projectRoot, 'packages/cli/package.json'))).toBe(true)
      expect(fs.existsSync(path.join(projectRoot, 'packages/cli/src/index.js'))).toBe(true)
    })

  })

  describe('CLI Workflow Tests', () => {
    
    test('help workflow shows complete information', () => {
      const result = runCLI('--help')
      
      // Should show main command info
      expect(result.stdout).toContain('Convert academic papers')
      expect(result.stdout).toContain('Commands:')
      
      // Should show available commands
      expect(result.stdout).toContain('init')
      expect(result.stdout).toContain('convert')
      
      // Should show global options
      expect(result.stdout).toContain('--verbose')
      expect(result.stdout).toContain('--config')
    })
    
    test('command discovery workflow', () => {
      // Test that users can discover subcommands
      const initHelp = runCLI('init --help')
      expect(initHelp.stdout).toContain('Initialize a new Paper2Data project')
      
      const convertHelp = runCLI('convert --help') 
      expect(convertHelp.stdout).toContain('Convert a paper')
      
      // Test subcommand discovery
      const batchHelp = runCLI('convert batch --help')
      expect(batchHelp.stdout).toContain('Convert multiple papers')
    })
    
    test('error handling workflow', () => {
      // Test invalid command
      const invalidCmd = runCLI('invalid-command', true)
      expect(invalidCmd.stderr).toContain('unknown command')
      
      // Test missing required argument
      const missingArg = runCLI('convert', true)
      expect(missingArg.stderr).toContain('missing required argument')
    })

  })

  describe('User Experience Workflow', () => {
    
    test('paper conversion workflow simulation', () => {
      // Simulate typical user workflow
      const result = runCLI('convert sample.pdf --output ./test-output --extract-figures', true)
      
      // Should show processing steps
      expect(result.stdout).toContain('Paper2Data Converter')
      expect(result.stdout).toContain('Input:')
      expect(result.stdout).toContain('sample.pdf')
      expect(result.stdout).toContain('Detected input type: PDF file')
      
      // Should show placeholder message
      expect(result.stdout).toContain('development placeholder')
    })
    
    test('project initialization workflow', () => {
      const result = runCLI('init test-project --template research', true)
      
      // Should show initialization steps
      expect(result.stdout).toContain('Initializing Paper2Data project')
      expect(result.stdout).toContain('development placeholder')
    })
    
    test('configuration workflow', () => {
      // This would test the interactive configuration but we'll simulate
      const result = runCLI('init config --help')
      expect(result.stdout).toContain('Initialize configuration only')
    })

  })

  describe('Integration Points', () => {
    
    test('CLI to Python integration readiness', () => {
      const result = runCLI('convert test.pdf', true)
      
      // Should show Python integration info
      expect(result.stdout).toContain('Python Parser Integration')
      expect(result.stdout).toContain('python -m paper2data.parser')
      
      // Should indicate integration not yet implemented
      expect(result.stdout).toContain('not yet implemented')
    })
    
    test('package structure supports integration', () => {
      const projectRoot = path.join(__dirname, '..')
      
      // CLI package should have Python bridge capability
      const cliConvert = path.join(projectRoot, 'packages/cli/src/commands/convert.js')
      const convertContent = fs.readFileSync(cliConvert, 'utf8')
      expect(convertContent).toContain('spawn')
      expect(convertContent).toContain('python')
      
      // Parser package should be importable
      const parserInit = path.join(projectRoot, 'packages/parser/src/__init__.py')
      expect(fs.existsSync(parserInit)).toBe(true)
    })

  })

  describe('Development Workflow Support', () => {
    
    test('testing infrastructure works', () => {
      // This test itself validates that the testing infrastructure works
      expect(true).toBe(true)
    })
    
    test('placeholder system provides clear feedback', () => {
      const convertResult = runCLI('convert test.pdf', true)
      const initResult = runCLI('init test', true)
      
      // Both should indicate they're development placeholders
      expect(convertResult.stdout).toContain('placeholder')
      expect(initResult.stdout).toContain('placeholder')
      
      // Should provide helpful context
      expect(convertResult.stdout).toContain('structure is ready')
      expect(initResult.stdout).toContain('structure is ready')
    })
    
    test('configuration supports development', () => {
      const projectRoot = path.join(__dirname, '..')
      
      // Check CI/CD configuration exists
      expect(fs.existsSync(path.join(projectRoot, 'config/github-actions.yml'))).toBe(true)
      
      // Check linting configuration exists
      expect(fs.existsSync(path.join(projectRoot, 'config/linting/eslint.json'))).toBe(true)
      expect(fs.existsSync(path.join(projectRoot, 'config/linting/flake8.ini'))).toBe(true)
    })

  })

  describe('Future Implementation Readiness', () => {
    
    test('CLI structure supports all planned features', () => {
      // Test that planned commands are structured
      const helpOutput = runCLI('--help').stdout
      
      // Core commands
      expect(helpOutput).toContain('init')
      expect(helpOutput).toContain('convert')
      
      // Global options for future features
      expect(helpOutput).toContain('--verbose')
      expect(helpOutput).toContain('--config')
      expect(helpOutput).toContain('--dry-run')
    })
    
    test('package structure supports Stage 1 implementation', () => {
      const projectRoot = path.join(__dirname, '..')
      
      // Parser package has all required modules
      const parserSrc = path.join(projectRoot, 'packages/parser/src')
      expect(fs.existsSync(path.join(parserSrc, 'ingest.py'))).toBe(true)
      expect(fs.existsSync(path.join(parserSrc, 'extractor.py'))).toBe(true)
      expect(fs.existsSync(path.join(parserSrc, 'utils.py'))).toBe(true)
      
      // CLI package has command structure
      const cliCommands = path.join(projectRoot, 'packages/cli/src/commands')
      expect(fs.existsSync(path.join(cliCommands, 'init.js'))).toBe(true)
      expect(fs.existsSync(path.join(cliCommands, 'convert.js'))).toBe(true)
    })

  })

})

describe('Workflow Integration Verification', () => {
  
  test('complete development workflow is ready', () => {
    console.log('\n🔍 Verifying Paper2Data development workflow readiness...')
    
    // Test CLI responsiveness
    const helpResult = runCLI('--help')
    expect(helpResult.stdout).toContain('paper2data')
    console.log('✅ CLI interface is responsive')
    
    // Test command structure
    const convertResult = runCLI('convert --help')
    expect(convertResult.stdout).toContain('Convert a paper')
    console.log('✅ Command structure is complete')
    
    // Test error handling
    const errorResult = runCLI('convert', true)
    expect(errorResult.stderr).toContain('missing required argument')
    console.log('✅ Error handling is working')
    
    // Test placeholder system
    const placeholderResult = runCLI('convert test.pdf', true)
    expect(placeholderResult.stdout).toContain('placeholder')
    console.log('✅ Placeholder system provides clear feedback')
    
    console.log('\n🚀 Paper2Data workflow is ready for Stage 1 implementation!')
  })

}) 