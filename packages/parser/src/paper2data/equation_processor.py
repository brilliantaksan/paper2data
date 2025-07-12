"""
Mathematical Equation Detection and LaTeX Conversion Module

This module implements sophisticated equation detection and LaTeX conversion
capabilities for academic papers, including:
- Mathematical expression detection
- LaTeX code generation
- Equation numbering and referencing
- Formula classification and analysis
- MathML output generation
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import base64

import fitz  # PyMuPDF
from .utils import get_logger, ProcessingError, clean_text

logger = get_logger(__name__)

class EquationType(Enum):
    """Types of mathematical equations."""
    INLINE = "inline"
    DISPLAY = "display"
    NUMBERED = "numbered"
    MULTI_LINE = "multi_line"
    ARRAY = "array"
    MATRIX = "matrix"
    INTEGRAL = "integral"
    SUMMATION = "summation"
    FRACTION = "fraction"
    GREEK = "greek"
    SUBSCRIPT_SUPERSCRIPT = "subscript_superscript"

class EquationComplexity(Enum):
    """Complexity levels of mathematical equations."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

@dataclass
class MathematicalEquation:
    """Represents a detected mathematical equation."""
    equation_id: str
    equation_type: EquationType
    complexity: EquationComplexity
    raw_text: str
    latex_code: str
    mathml_code: str
    position: Dict[str, float]  # x, y, width, height
    page_number: int
    confidence: float
    context_before: str
    context_after: str
    equation_number: Optional[str] = None
    referenced_by: List[str] = None  # List of reference IDs
    variables: List[str] = None  # Detected variables
    operators: List[str] = None  # Detected operators
    
    def __post_init__(self):
        if self.referenced_by is None:
            self.referenced_by = []
        if self.variables is None:
            self.variables = []
        if self.operators is None:
            self.operators = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['equation_type'] = self.equation_type.value
        data['complexity'] = self.complexity.value
        return data

class EquationDetector:
    """Detects mathematical equations in PDF documents."""
    
    def __init__(self):
        self.equation_patterns = self._compile_equation_patterns()
        self.latex_symbols = self._load_latex_symbols()
        self.greek_letters = self._load_greek_letters()
        self.mathematical_operators = self._load_mathematical_operators()
        
    def _compile_equation_patterns(self) -> List[Tuple[re.Pattern, EquationType]]:
        """Compile regex patterns for equation detection."""
        patterns = [
            # Display equations (often on separate lines)
            (re.compile(r'^\s*([A-Za-z]\s*=\s*[^=\n]+)$', re.MULTILINE), EquationType.DISPLAY),
            
            # Numbered equations
            (re.compile(r'^\s*([^=\n]+\s*=\s*[^=\n]+)\s*\((\d+)\)$', re.MULTILINE), EquationType.NUMBERED),
            
            # Inline equations with common mathematical notation
            (re.compile(r'([α-ωΑ-Ω]+|[a-zA-Z]+_[a-zA-Z0-9]+|[a-zA-Z]+\^[a-zA-Z0-9]+|\b[a-zA-Z]\s*[=<>±∓≈≠≤≥]\s*[a-zA-Z0-9]+)', re.UNICODE), EquationType.INLINE),
            
            # Fractions
            (re.compile(r'([a-zA-Z0-9]+)\s*/\s*([a-zA-Z0-9]+)', re.MULTILINE), EquationType.FRACTION),
            
            # Integrals
            (re.compile(r'∫[^∫]*d[a-zA-Z]', re.UNICODE), EquationType.INTEGRAL),
            
            # Summations
            (re.compile(r'[∑Σ]\s*[a-zA-Z0-9_^=]+', re.UNICODE), EquationType.SUMMATION),
            
            # Greek letters
            (re.compile(r'[α-ωΑ-Ω]', re.UNICODE), EquationType.GREEK),
            
            # Subscripts and superscripts
            (re.compile(r'[a-zA-Z][_^][a-zA-Z0-9]+', re.MULTILINE), EquationType.SUBSCRIPT_SUPERSCRIPT),
            
            # Matrix notation
            (re.compile(r'\[[\s\d\.\-\+\*/]+\]', re.MULTILINE), EquationType.MATRIX),
            
            # Arrays or systems of equations
            (re.compile(r'{\s*[^}]*\s*\\\\[\s\S]*}', re.MULTILINE), EquationType.ARRAY),
        ]
        return patterns
    
    def _load_latex_symbols(self) -> Dict[str, str]:
        """Load mapping from Unicode symbols to LaTeX commands."""
        return {
            'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta',
            'ε': r'\epsilon', 'ζ': r'\zeta', 'η': r'\eta', 'θ': r'\theta',
            'ι': r'\iota', 'κ': r'\kappa', 'λ': r'\lambda', 'μ': r'\mu',
            'ν': r'\nu', 'ξ': r'\xi', 'ο': r'\omicron', 'π': r'\pi',
            'ρ': r'\rho', 'σ': r'\sigma', 'τ': r'\tau', 'υ': r'\upsilon',
            'φ': r'\phi', 'χ': r'\chi', 'ψ': r'\psi', 'ω': r'\omega',
            'Α': r'\Alpha', 'Β': r'\Beta', 'Γ': r'\Gamma', 'Δ': r'\Delta',
            'Ε': r'\Epsilon', 'Ζ': r'\Zeta', 'Η': r'\Eta', 'Θ': r'\Theta',
            'Ι': r'\Iota', 'Κ': r'\Kappa', 'Λ': r'\Lambda', 'Μ': r'\Mu',
            'Ν': r'\Nu', 'Ξ': r'\Xi', 'Ο': r'\Omicron', 'Π': r'\Pi',
            'Ρ': r'\Rho', 'Σ': r'\Sigma', 'Τ': r'\Tau', 'Υ': r'\Upsilon',
            'Φ': r'\Phi', 'Χ': r'\Chi', 'Ψ': r'\Psi', 'Ω': r'\Omega',
            '∫': r'\int', '∑': r'\sum', '∏': r'\prod', '√': r'\sqrt',
            '∞': r'\infty', '∂': r'\partial', '∇': r'\nabla', '±': r'\pm',
            '∓': r'\mp', '≈': r'\approx', '≠': r'\neq', '≤': r'\leq',
            '≥': r'\geq', '→': r'\to', '←': r'\leftarrow', '↔': r'\leftrightarrow',
            '∀': r'\forall', '∃': r'\exists', '∈': r'\in', '∉': r'\notin',
            '⊂': r'\subset', '⊃': r'\supset', '⊆': r'\subseteq', '⊇': r'\supseteq',
            '∩': r'\cap', '∪': r'\cup', '∅': r'\emptyset', '×': r'\times',
            '÷': r'\div', '·': r'\cdot', '∘': r'\circ', '⊕': r'\oplus',
            '⊗': r'\otimes', '⊥': r'\perp', '∥': r'\parallel', '∢': r'\measuredangle',
        }
    
    def _load_greek_letters(self) -> List[str]:
        """Load list of Greek letters."""
        return [
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ',
            'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω',
            'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ',
            'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω'
        ]
    
    def _load_mathematical_operators(self) -> List[str]:
        """Load list of mathematical operators."""
        return [
            '+', '-', '×', '÷', '=', '≠', '≈', '≤', '≥', '<', '>', '±', '∓',
            '∫', '∑', '∏', '√', '∞', '∂', '∇', '→', '←', '↔', '∀', '∃',
            '∈', '∉', '⊂', '⊃', '⊆', '⊇', '∩', '∪', '∅', '·', '∘', '⊕',
            '⊗', '⊥', '∥', '∢', '^', '_', '/', '*', '!', '%', '&', '|'
        ]
    
    def detect_equations(self, text: str, page_number: int) -> List[MathematicalEquation]:
        """Detect mathematical equations in text."""
        equations = []
        equation_id = 0
        
        # Split text into lines for better context
        lines = text.split('\n')
        
        for line_idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check each pattern
            for pattern, eq_type in self.equation_patterns:
                matches = pattern.finditer(line)
                
                for match in matches:
                    equation_id += 1
                    
                    # Extract equation text
                    equation_text = match.group(1) if match.groups() else match.group(0)
                    
                    # Generate LaTeX code
                    latex_code = self._generate_latex(equation_text, eq_type)
                    
                    # Generate MathML code
                    mathml_code = self._generate_mathml(equation_text, eq_type)
                    
                    # Determine complexity
                    complexity = self._assess_complexity(equation_text)
                    
                    # Extract variables and operators
                    variables = self._extract_variables(equation_text)
                    operators = self._extract_operators(equation_text)
                    
                    # Get context
                    context_before = lines[max(0, line_idx-1)] if line_idx > 0 else ""
                    context_after = lines[min(len(lines)-1, line_idx+1)] if line_idx < len(lines)-1 else ""
                    
                    # Extract equation number if present
                    equation_number = None
                    if eq_type == EquationType.NUMBERED and len(match.groups()) > 1:
                        equation_number = match.group(2)
                    
                    # Create equation object
                    equation = MathematicalEquation(
                        equation_id=f"eq_{equation_id}",
                        equation_type=eq_type,
                        complexity=complexity,
                        raw_text=equation_text,
                        latex_code=latex_code,
                        mathml_code=mathml_code,
                        position={"x": match.start(), "y": line_idx, "width": len(equation_text), "height": 1},
                        page_number=page_number,
                        confidence=self._calculate_confidence(equation_text, eq_type),
                        context_before=context_before,
                        context_after=context_after,
                        equation_number=equation_number,
                        variables=variables,
                        operators=operators
                    )
                    
                    equations.append(equation)
        
        return equations
    
    def _generate_latex(self, equation_text: str, eq_type: EquationType) -> str:
        """Generate LaTeX code for an equation."""
        # Replace Unicode symbols with LaTeX commands
        latex_text = equation_text
        
        for unicode_char, latex_command in self.latex_symbols.items():
            latex_text = latex_text.replace(unicode_char, latex_command)
        
        # Handle subscripts and superscripts
        latex_text = re.sub(r'([a-zA-Z])_([a-zA-Z0-9]+)', r'\1_{\2}', latex_text)
        latex_text = re.sub(r'([a-zA-Z])\^([a-zA-Z0-9]+)', r'\1^{\2}', latex_text)
        
        # Handle fractions
        latex_text = re.sub(r'([a-zA-Z0-9]+)\s*/\s*([a-zA-Z0-9]+)', r'\\frac{\1}{\2}', latex_text)
        
        # Wrap based on equation type
        if eq_type == EquationType.DISPLAY:
            return f"\\[\n{latex_text}\n\\]"
        elif eq_type == EquationType.NUMBERED:
            return f"\\begin{{equation}}\n{latex_text}\n\\end{{equation}}"
        elif eq_type == EquationType.INLINE:
            return f"${latex_text}$"
        elif eq_type == EquationType.ARRAY:
            return f"\\begin{{array}}\n{latex_text}\n\\end{{array}}"
        elif eq_type == EquationType.MATRIX:
            return f"\\begin{{matrix}}\n{latex_text}\n\\end{{matrix}}"
        else:
            return latex_text
    
    def _generate_mathml(self, equation_text: str, eq_type: EquationType) -> str:
        """Generate MathML code for an equation."""
        # Basic MathML structure
        mathml_content = equation_text
        
        # Replace common symbols with MathML entities
        mathml_replacements = {
            '∫': '&int;',
            '∑': '&sum;',
            '∏': '&prod;',
            '√': '&radic;',
            '∞': '&infin;',
            '∂': '&part;',
            '∇': '&nabla;',
            '±': '&plusmn;',
            '∓': '&mnplus;',
            '≈': '&asymp;',
            '≠': '&ne;',
            '≤': '&le;',
            '≥': '&ge;',
            '→': '&rarr;',
            '←': '&larr;',
            '↔': '&harr;',
            '×': '&times;',
            '÷': '&divide;',
            '·': '&middot;',
        }
        
        for symbol, entity in mathml_replacements.items():
            mathml_content = mathml_content.replace(symbol, entity)
        
        # Wrap in MathML tags
        if eq_type == EquationType.DISPLAY:
            return f'<math display="block"><mrow>{mathml_content}</mrow></math>'
        else:
            return f'<math><mrow>{mathml_content}</mrow></math>'
    
    def _assess_complexity(self, equation_text: str) -> EquationComplexity:
        """Assess the complexity of an equation."""
        complexity_score = 0
        
        # Count different types of mathematical elements
        greek_count = sum(1 for char in equation_text if char in self.greek_letters)
        operator_count = sum(1 for char in equation_text if char in self.mathematical_operators)
        subscript_superscript_count = len(re.findall(r'[_^]', equation_text))
        fraction_count = len(re.findall(r'/', equation_text))
        integral_count = len(re.findall(r'∫', equation_text))
        summation_count = len(re.findall(r'[∑Σ]', equation_text))
        
        # Calculate complexity score
        complexity_score += greek_count * 1
        complexity_score += operator_count * 0.5
        complexity_score += subscript_superscript_count * 2
        complexity_score += fraction_count * 2
        complexity_score += integral_count * 3
        complexity_score += summation_count * 3
        
        # Add length factor
        complexity_score += len(equation_text) * 0.1
        
        # Determine complexity level
        if complexity_score < 5:
            return EquationComplexity.SIMPLE
        elif complexity_score < 15:
            return EquationComplexity.MODERATE
        elif complexity_score < 30:
            return EquationComplexity.COMPLEX
        else:
            return EquationComplexity.VERY_COMPLEX
    
    def _extract_variables(self, equation_text: str) -> List[str]:
        """Extract variables from equation text."""
        variables = set()
        
        # Find single letters (common variables)
        for match in re.finditer(r'\b[a-zA-Z]\b', equation_text):
            variables.add(match.group())
        
        # Find variables with subscripts/superscripts
        for match in re.finditer(r'[a-zA-Z]+[_^][a-zA-Z0-9]+', equation_text):
            variables.add(match.group())
        
        # Find Greek letters
        for char in equation_text:
            if char in self.greek_letters:
                variables.add(char)
        
        return list(variables)
    
    def _extract_operators(self, equation_text: str) -> List[str]:
        """Extract operators from equation text."""
        operators = set()
        
        for char in equation_text:
            if char in self.mathematical_operators:
                operators.add(char)
        
        return list(operators)
    
    def _calculate_confidence(self, equation_text: str, eq_type: EquationType) -> float:
        """Calculate confidence score for equation detection."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence for specific indicators
        if any(char in self.greek_letters for char in equation_text):
            confidence += 0.2
        
        if any(char in self.mathematical_operators for char in equation_text):
            confidence += 0.2
        
        if re.search(r'[_^]', equation_text):
            confidence += 0.1
        
        if '=' in equation_text:
            confidence += 0.1
        
        if eq_type == EquationType.NUMBERED:
            confidence += 0.2
        
        return min(confidence, 1.0)

class EquationProcessor:
    """Main processor for mathematical equations in PDF documents."""
    
    def __init__(self):
        self.detector = EquationDetector()
        self.equation_refs = {}  # Track equation references
    
    def process_equations(self, pdf_content: bytes) -> Dict[str, Any]:
        """Process equations from PDF content."""
        logger.info("Starting equation processing")
        
        try:
            # Open PDF document
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            
            all_equations = []
            equation_references = []
            
            # Process each page
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_text = page.get_text()
                
                # Detect equations on this page
                page_equations = self.detector.detect_equations(page_text, page_num + 1)
                all_equations.extend(page_equations)
                
                # Find equation references
                refs = self._find_equation_references(page_text, page_num + 1)
                equation_references.extend(refs)
            
            # Link equations with their references
            self._link_equation_references(all_equations, equation_references)
            
            # Generate summary statistics
            stats = self._generate_equation_statistics(all_equations)
            
            doc.close()
            
            return {
                "total_equations": len(all_equations),
                "equations": [eq.to_dict() for eq in all_equations],
                "equation_references": equation_references,
                "statistics": stats,
                "processing_status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Equation processing failed: {str(e)}")
            return {
                "total_equations": 0,
                "equations": [],
                "equation_references": [],
                "statistics": {},
                "processing_status": "failed",
                "error": str(e)
            }
    
    def _find_equation_references(self, text: str, page_number: int) -> List[Dict[str, Any]]:
        """Find references to equations in text."""
        references = []
        
        # Common equation reference patterns
        ref_patterns = [
            r'(?:Equation|Eq\.?|equation)\s*\((\d+)\)',
            r'(?:Equation|Eq\.?|equation)\s*(\d+)',
            r'\((\d+)\)',  # Simple numbered references
        ]
        
        for pattern in ref_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                references.append({
                    "reference_text": match.group(0),
                    "equation_number": match.group(1),
                    "page_number": page_number,
                    "position": match.start()
                })
        
        return references
    
    def _link_equation_references(self, equations: List[MathematicalEquation], 
                                 references: List[Dict[str, Any]]):
        """Link equations with their references."""
        # Create mapping of equation numbers to equation IDs
        number_to_id = {}
        for eq in equations:
            if eq.equation_number:
                number_to_id[eq.equation_number] = eq.equation_id
        
        # Link references to equations
        for ref in references:
            eq_num = ref["equation_number"]
            if eq_num in number_to_id:
                # Find the equation and add reference
                for eq in equations:
                    if eq.equation_id == number_to_id[eq_num]:
                        eq.referenced_by.append(ref["reference_text"])
                        break
    
    def _generate_equation_statistics(self, equations: List[MathematicalEquation]) -> Dict[str, Any]:
        """Generate statistics about detected equations."""
        if not equations:
            return {}
        
        # Count by type
        type_counts = {}
        for eq in equations:
            eq_type = eq.equation_type.value
            type_counts[eq_type] = type_counts.get(eq_type, 0) + 1
        
        # Count by complexity
        complexity_counts = {}
        for eq in equations:
            complexity = eq.complexity.value
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
        
        # Calculate average confidence
        avg_confidence = sum(eq.confidence for eq in equations) / len(equations)
        
        # Count unique variables and operators
        all_variables = set()
        all_operators = set()
        for eq in equations:
            all_variables.update(eq.variables)
            all_operators.update(eq.operators)
        
        return {
            "total_equations": len(equations),
            "equations_by_type": type_counts,
            "equations_by_complexity": complexity_counts,
            "average_confidence": round(avg_confidence, 3),
            "unique_variables": len(all_variables),
            "unique_operators": len(all_operators),
            "most_common_variables": sorted(list(all_variables))[:10],
            "most_common_operators": sorted(list(all_operators))[:10],
            "numbered_equations": len([eq for eq in equations if eq.equation_number]),
            "referenced_equations": len([eq for eq in equations if eq.referenced_by])
        }

def export_equations_to_latex(equations: List[MathematicalEquation], 
                            output_path: Path) -> None:
    """Export equations to a LaTeX file."""
    latex_content = [
        "\\documentclass{article}",
        "\\usepackage{amsmath}",
        "\\usepackage{amssymb}",
        "\\usepackage{amsfonts}",
        "\\begin{document}",
        "\\title{Extracted Mathematical Equations}",
        "\\maketitle",
        ""
    ]
    
    for eq in equations:
        latex_content.append(f"% Equation {eq.equation_id} (Page {eq.page_number})")
        latex_content.append(f"% Type: {eq.equation_type.value}, Complexity: {eq.complexity.value}")
        latex_content.append(f"% Confidence: {eq.confidence:.3f}")
        latex_content.append("")
        latex_content.append(eq.latex_code)
        latex_content.append("")
        
        if eq.equation_number:
            latex_content.append(f"% Equation number: {eq.equation_number}")
        
        if eq.referenced_by:
            latex_content.append(f"% Referenced by: {', '.join(eq.referenced_by)}")
        
        latex_content.append("\\bigskip")
        latex_content.append("")
    
    latex_content.extend([
        "\\end{document}"
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    logger.info(f"Exported {len(equations)} equations to LaTeX file: {output_path}")

def export_equations_to_mathml(equations: List[MathematicalEquation], 
                             output_path: Path) -> None:
    """Export equations to a MathML file."""
    mathml_content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<html xmlns="http://www.w3.org/1999/xhtml">',
        '<head>',
        '<title>Extracted Mathematical Equations</title>',
        '</head>',
        '<body>',
        '<h1>Extracted Mathematical Equations</h1>',
        ''
    ]
    
    for eq in equations:
        mathml_content.append(f'<div class="equation" id="{eq.equation_id}">')
        mathml_content.append(f'<h3>Equation {eq.equation_id} (Page {eq.page_number})</h3>')
        mathml_content.append(f'<p>Type: {eq.equation_type.value}, Complexity: {eq.complexity.value}</p>')
        mathml_content.append(f'<p>Confidence: {eq.confidence:.3f}</p>')
        mathml_content.append(eq.mathml_code)
        
        if eq.equation_number:
            mathml_content.append(f'<p>Equation number: {eq.equation_number}</p>')
        
        if eq.referenced_by:
            mathml_content.append(f'<p>Referenced by: {", ".join(eq.referenced_by)}</p>')
        
        mathml_content.append('</div>')
        mathml_content.append('<hr/>')
    
    mathml_content.extend([
        '</body>',
        '</html>'
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(mathml_content))
    
    logger.info(f"Exported {len(equations)} equations to MathML file: {output_path}")

# Global equation processor instance
_global_equation_processor = None

def get_equation_processor() -> EquationProcessor:
    """Get global equation processor instance."""
    global _global_equation_processor
    if _global_equation_processor is None:
        _global_equation_processor = EquationProcessor()
    return _global_equation_processor

def process_equations_from_pdf(pdf_content: bytes) -> Dict[str, Any]:
    """Process equations from PDF content using global processor."""
    processor = get_equation_processor()
    return processor.process_equations(pdf_content) 