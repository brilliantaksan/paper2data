/**
 * Tests for Paper2Data CLI commands
 * 
 * Tests basic command structure, help output, and placeholder functionality.
 */

const { execSync } = require('child_process')
const path = require('path')

// Path to the CLI script
const CLI_PATH = path.join(__dirname, '../src/index.js')

/**
 * Helper function to run CLI commands and capture output
 */
function runCLI(args = '', expectError = false) {
  try {
    const result = execSync(`node ${CLI_PATH} ${args}`, {
      encoding: 'utf8',
      stdio: 'pipe'
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

describe('Paper2Data CLI', () => {
  
  describe('Basic CLI Structure', () => {
    
    test('shows help when no arguments provided', () => {
      const result = runCLI('', true)
      expect(result.stdout).toContain('Convert academic papers')
      expect(result.stdout).toContain('Commands:')
      expect(result.stdout).toContain('init')
      expect(result.stdout).toContain('convert')
    })
    
    test('shows version with --version flag', () => {
      const result = runCLI('--version')
      expect(result.stdout).toMatch(/\d+\.\d+\.\d+/)
    })
    
    test('shows version with -v flag', () => {
      const result = runCLI('-v')
      expect(result.stdout).toMatch(/\d+\.\d+\.\d+/)
    })
    
    test('shows help with --help flag', () => {
      const result = runCLI('--help')
      expect(result.stdout).toContain('Usage:')
      expect(result.stdout).toContain('paper2data')
      expect(result.stdout).toContain('Options:')
    })
    
  })
  
  describe('Init Command', () => {
    
    test('init command exists and shows help', () => {
      const result = runCLI('init --help')
      expect(result.stdout).toContain('Initialize a new Paper2Data project')
      expect(result.stdout).toContain('Arguments:')
      expect(result.stdout).toContain('directory')
      expect(result.stdout).toContain('Options:')
      expect(result.stdout).toContain('--template')
    })
    
    test('init command shows placeholder message', () => {
      const result = runCLI('init test-project', true)
      expect(result.stdout).toContain('development placeholder')
    })
    
    test('init config subcommand exists', () => {
      const result = runCLI('init config --help')
      expect(result.stdout).toContain('Initialize configuration only')
    })
    
  })
  
  describe('Convert Command', () => {
    
    test('convert command exists and shows help', () => {
      const result = runCLI('convert --help')
      expect(result.stdout).toContain('Convert a paper')
      expect(result.stdout).toContain('Arguments:')
      expect(result.stdout).toContain('input')
      expect(result.stdout).toContain('Options:')
      expect(result.stdout).toContain('--output')
      expect(result.stdout).toContain('--format')
    })
    
    test('convert command requires input argument', () => {
      const result = runCLI('convert', true)
      expect(result.stderr).toContain('error: missing required argument')
    })
    
    test('convert command shows placeholder message with valid input', () => {
      const result = runCLI('convert test.pdf', true)
      expect(result.stdout).toContain('Paper2Data Converter')
      expect(result.stdout).toContain('development placeholder')
    })
    
    test('convert batch subcommand exists', () => {
      const result = runCLI('convert batch --help')
      expect(result.stdout).toContain('Convert multiple papers')
    })
    
  })
  
  describe('Global Options', () => {
    
    test('global options are recognized', () => {
      const result = runCLI('--help')
      expect(result.stdout).toContain('--verbose')
      expect(result.stdout).toContain('--quiet')
      expect(result.stdout).toContain('--config')
      expect(result.stdout).toContain('--dry-run')
    })
    
  })
  
  describe('Input Type Detection', () => {
    
    test('detects PDF files', () => {
      const result = runCLI('convert sample.pdf', true)
      expect(result.stdout).toContain('PDF file')
    })
    
    test('detects arXiv URLs', () => {
      const result = runCLI('convert https://arxiv.org/abs/1234.5678', true)
      expect(result.stdout).toContain('arXiv URL')
    })
    
    test('detects DOI format', () => {
      const result = runCLI('convert 10.1038/nature12373', true)
      expect(result.stdout).toContain('DOI')
    })
    
  })
  
  describe('Error Handling', () => {
    
    test('handles invalid commands gracefully', () => {
      const result = runCLI('invalid-command', true)
      expect(result.stderr).toContain('error: unknown command')
    })
    
    test('shows helpful error messages', () => {
      const result = runCLI('convert --invalid-option', true)
      expect(result.stderr).toContain('error: unknown option')
    })
    
  })

})

describe('CLI Package Structure', () => {
  
  test('can require main CLI file', () => {
    expect(() => {
      require('../src/index.js')
    }).not.toThrow()
  })
  
  test('can require command modules', () => {
    expect(() => {
      require('../src/commands/init.js')
      require('../src/commands/convert.js')
    }).not.toThrow()
  })
  
  test('package.json has correct structure', () => {
    const packageJson = require('../package.json')
    
    expect(packageJson.name).toBe('paper2data-cli')
    expect(packageJson.bin).toHaveProperty('paper2data')
    expect(packageJson.main).toBe('src/index.js')
    expect(packageJson.dependencies).toHaveProperty('commander')
    expect(packageJson.dependencies).toHaveProperty('chalk')
    expect(packageJson.dependencies).toHaveProperty('ora')
  })

})

describe('Development Readiness', () => {
  
  test('CLI structure supports future implementation', () => {
    // Test that the CLI has the basic structure needed for development
    const result = runCLI('--help')
    
    // Should have main commands
    expect(result.stdout).toContain('init')
    expect(result.stdout).toContain('convert')
    
    // Should have global options
    expect(result.stdout).toContain('--verbose')
    expect(result.stdout).toContain('--config')
  })
  
  test('placeholder messages indicate development status', () => {
    const initResult = runCLI('init test', true)
    const convertResult = runCLI('convert test.pdf', true)
    
    expect(initResult.stdout).toContain('placeholder')
    expect(convertResult.stdout).toContain('placeholder')
  })

}) 