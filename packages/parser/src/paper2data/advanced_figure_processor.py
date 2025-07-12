"""
Advanced Figure Processing Module

This module implements sophisticated figure processing capabilities for Stage 5:
- Enhanced figure detection and extraction
- Caption extraction and association
- Image analysis (size, format, quality assessment)
- Figure classification (charts, diagrams, photos, plots, etc.)
- Text extraction from figures (OCR)
- Metadata extraction and analysis
- Enhanced export formats
- Figure relationship analysis
"""

import re
import io
import json
import base64
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import logging

import fitz  # PyMuPDF
from PIL import Image, ImageStat, ImageFilter
from .utils import get_logger, ProcessingError, clean_text

logger = get_logger(__name__)

class FigureType(Enum):
    """Types of figures detected in academic papers."""
    CHART = "chart"
    DIAGRAM = "diagram"
    PHOTOGRAPH = "photograph"
    PLOT = "plot"
    GRAPH = "graph"
    FLOWCHART = "flowchart"
    SCHEMATIC = "schematic"
    SCREENSHOT = "screenshot"
    MAP = "map"
    ILLUSTRATION = "illustration"
    TABLE_IMAGE = "table_image"
    EQUATION_IMAGE = "equation_image"
    UNKNOWN = "unknown"

class ImageQuality(Enum):
    """Image quality assessment levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    VERY_POOR = "very_poor"

class CaptionPosition(Enum):
    """Position of caption relative to figure."""
    ABOVE = "above"
    BELOW = "below"
    LEFT = "left"
    RIGHT = "right"
    EMBEDDED = "embedded"
    UNKNOWN = "unknown"

@dataclass
class FigureCaption:
    """Represents a figure caption."""
    caption_id: str
    text: str
    position: CaptionPosition
    page_number: int
    confidence: float
    raw_text: str
    cleaned_text: str
    figure_number: Optional[str] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['position'] = self.position.value
        return data

@dataclass
class ImageAnalysis:
    """Results of image analysis."""
    width: int
    height: int
    format: str
    mode: str
    file_size: int
    quality: ImageQuality
    brightness: float
    contrast: float
    sharpness: float
    color_complexity: int
    has_transparency: bool
    dominant_colors: List[Tuple[int, int, int]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['quality'] = self.quality.value
        return data

@dataclass
class AdvancedFigure:
    """Enhanced figure representation with advanced analysis."""
    figure_id: str
    figure_type: FigureType
    page_number: int
    position: Dict[str, float]  # x, y, width, height
    image_data: bytes
    image_analysis: ImageAnalysis
    caption: Optional[FigureCaption]
    extracted_text: List[str]
    confidence: float
    metadata: Dict[str, Any]
    related_figures: List[str] = None
    
    def __post_init__(self):
        if self.related_figures is None:
            self.related_figures = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['figure_type'] = self.figure_type.value
        data['image_analysis'] = self.image_analysis.to_dict()
        if self.caption:
            data['caption'] = self.caption.to_dict()
        # Convert image data to base64 for JSON serialization
        data['image_data_base64'] = base64.b64encode(self.image_data).decode('utf-8')
        del data['image_data']  # Remove binary data
        return data

class CaptionDetector:
    """Detects and extracts figure captions from text."""
    
    def __init__(self):
        self.caption_patterns = self._compile_caption_patterns()
        self.figure_keywords = self._load_figure_keywords()
    
    def _compile_caption_patterns(self) -> List[Tuple[re.Pattern, CaptionPosition]]:
        """Compile regex patterns for caption detection."""
        patterns = [
            # Standard figure captions
            (re.compile(r'^(?:Figure|Fig\.?|FIG\.?)\s*(\d+)[\.:]\s*(.+)$', re.MULTILINE | re.IGNORECASE), CaptionPosition.BELOW),
            
            # Image/picture captions
            (re.compile(r'^(?:Image|Picture|Photo)\s*(\d+)[\.:]\s*(.+)$', re.MULTILINE | re.IGNORECASE), CaptionPosition.BELOW),
            
            # Chart/graph captions
            (re.compile(r'^(?:Chart|Graph|Plot)\s*(\d+)[\.:]\s*(.+)$', re.MULTILINE | re.IGNORECASE), CaptionPosition.BELOW),
            
            # Diagram captions
            (re.compile(r'^(?:Diagram|Schematic)\s*(\d+)[\.:]\s*(.+)$', re.MULTILINE | re.IGNORECASE), CaptionPosition.BELOW),
            
            # Caption without figure number
            (re.compile(r'^(?:Figure|Fig\.?)\s*[\.:]\s*(.+)$', re.MULTILINE | re.IGNORECASE), CaptionPosition.BELOW),
            
            # Embedded captions (text within parentheses after figure references)
            (re.compile(r'\(([^)]*(?:shows?|depicts?|illustrates?|demonstrates?)[^)]*)\)', re.IGNORECASE), CaptionPosition.EMBEDDED),
        ]
        return patterns
    
    def _load_figure_keywords(self) -> List[str]:
        """Load keywords commonly found in figure captions."""
        return [
            'shows', 'depicts', 'illustrates', 'demonstrates', 'displays',
            'presents', 'represents', 'contains', 'includes', 'features',
            'comparison', 'analysis', 'distribution', 'relationship',
            'structure', 'process', 'workflow', 'architecture', 'design',
            'results', 'data', 'trends', 'patterns', 'correlation',
            'before', 'after', 'example', 'case', 'study', 'model'
        ]
    
    def detect_captions(self, text: str, page_number: int) -> List[FigureCaption]:
        """Detect figure captions in text."""
        captions = []
        caption_id = 0
        
        lines = text.split('\n')
        
        for line_idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check each pattern
            for pattern, position in self.caption_patterns:
                matches = pattern.finditer(line)
                
                for match in matches:
                    caption_id += 1
                    
                    # Extract caption text and figure number
                    if len(match.groups()) >= 2:
                        figure_number = match.group(1)
                        caption_text = match.group(2)
                    elif len(match.groups()) == 1:
                        figure_number = None
                        caption_text = match.group(1)
                    else:
                        figure_number = None
                        caption_text = match.group(0)
                    
                    # Clean caption text
                    cleaned_text = self._clean_caption_text(caption_text)
                    
                    # Extract keywords
                    keywords = self._extract_keywords(cleaned_text)
                    
                    # Calculate confidence
                    confidence = self._calculate_caption_confidence(cleaned_text, keywords)
                    
                    # Create caption object
                    caption = FigureCaption(
                        caption_id=f"caption_{caption_id}",
                        text=caption_text,
                        position=position,
                        page_number=page_number,
                        confidence=confidence,
                        raw_text=line,
                        cleaned_text=cleaned_text,
                        figure_number=figure_number,
                        keywords=keywords
                    )
                    
                    captions.append(caption)
        
        return captions
    
    def _clean_caption_text(self, text: str) -> str:
        """Clean caption text by removing extra whitespace and formatting."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common formatting artifacts
        cleaned = re.sub(r'[\u2000-\u206f\u2e00-\u2e7f]', ' ', cleaned)  # Remove various spaces and punctuation
        cleaned = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\'\/]', '', cleaned)  # Keep only basic punctuation
        
        return cleaned.strip()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from caption text."""
        keywords = []
        text_lower = text.lower()
        
        for keyword in self.figure_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return keywords
    
    def _calculate_caption_confidence(self, text: str, keywords: List[str]) -> float:
        """Calculate confidence score for caption detection."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on length
        if len(text) > 20:
            confidence += 0.1
        if len(text) > 50:
            confidence += 0.1
        
        # Increase confidence based on keywords
        confidence += len(keywords) * 0.05
        
        # Increase confidence if it mentions specific figure elements
        text_lower = text.lower()
        if any(word in text_lower for word in ['figure', 'graph', 'chart', 'diagram']):
            confidence += 0.1
        
        return min(confidence, 1.0)

class ImageAnalyzer:
    """Analyzes image properties and quality."""
    
    def analyze_image(self, image_data: bytes) -> ImageAnalysis:
        """Perform comprehensive image analysis."""
        try:
            # Load image with PIL
            image = Image.open(io.BytesIO(image_data))
            
            # Basic properties
            width, height = image.size
            format_type = image.format or "Unknown"
            mode = image.mode
            file_size = len(image_data)
            
            # Quality assessment
            quality = self._assess_image_quality(image)
            
            # Statistical analysis
            brightness = self._calculate_brightness(image)
            contrast = self._calculate_contrast(image)
            sharpness = self._calculate_sharpness(image)
            color_complexity = self._calculate_color_complexity(image)
            
            # Transparency check
            has_transparency = self._has_transparency(image)
            
            # Dominant colors
            dominant_colors = self._extract_dominant_colors(image)
            
            return ImageAnalysis(
                width=width,
                height=height,
                format=format_type,
                mode=mode,
                file_size=file_size,
                quality=quality,
                brightness=brightness,
                contrast=contrast,
                sharpness=sharpness,
                color_complexity=color_complexity,
                has_transparency=has_transparency,
                dominant_colors=dominant_colors
            )
            
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            # Return default analysis
            return ImageAnalysis(
                width=0, height=0, format="Unknown", mode="Unknown",
                file_size=len(image_data), quality=ImageQuality.POOR,
                brightness=0.0, contrast=0.0, sharpness=0.0,
                color_complexity=0, has_transparency=False,
                dominant_colors=[]
            )
    
    def _assess_image_quality(self, image: Image.Image) -> ImageQuality:
        """Assess overall image quality."""
        width, height = image.size
        
        # Resolution-based assessment
        pixel_count = width * height
        
        if pixel_count >= 1000000:  # >= 1MP
            base_quality = ImageQuality.EXCELLENT
        elif pixel_count >= 500000:  # >= 0.5MP
            base_quality = ImageQuality.GOOD
        elif pixel_count >= 100000:  # >= 0.1MP
            base_quality = ImageQuality.FAIR
        elif pixel_count >= 10000:   # >= 0.01MP
            base_quality = ImageQuality.POOR
        else:
            base_quality = ImageQuality.VERY_POOR
        
        return base_quality
    
    def _calculate_brightness(self, image: Image.Image) -> float:
        """Calculate average brightness of image."""
        try:
            if image.mode != 'L':
                grayscale = image.convert('L')
            else:
                grayscale = image
            
            stat = ImageStat.Stat(grayscale)
            return stat.mean[0] / 255.0
        except Exception:
            return 0.5  # Default middle brightness
    
    def _calculate_contrast(self, image: Image.Image) -> float:
        """Calculate contrast measure of image."""
        try:
            if image.mode != 'L':
                grayscale = image.convert('L')
            else:
                grayscale = image
            
            stat = ImageStat.Stat(grayscale)
            return stat.stddev[0] / 255.0
        except Exception:
            return 0.0  # Default low contrast
    
    def _calculate_sharpness(self, image: Image.Image) -> float:
        """Calculate sharpness measure using edge detection."""
        try:
            if image.mode != 'L':
                grayscale = image.convert('L')
            else:
                grayscale = image
            
            # Apply edge detection filter
            edges = grayscale.filter(ImageFilter.FIND_EDGES)
            stat = ImageStat.Stat(edges)
            return stat.mean[0] / 255.0
        except Exception:
            return 0.0  # Default low sharpness
    
    def _calculate_color_complexity(self, image: Image.Image) -> int:
        """Calculate color complexity (number of unique colors)."""
        try:
            # Convert to palette mode to count colors
            if image.mode != 'P':
                # Quantize to reduce computation
                palette_image = image.quantize(colors=256)
            else:
                palette_image = image
            
            colors = palette_image.getcolors()
            return len(colors) if colors else 0
        except Exception:
            return 0
    
    def _has_transparency(self, image: Image.Image) -> bool:
        """Check if image has transparency."""
        return image.mode in ('RGBA', 'LA') or 'transparency' in image.info
    
    def _extract_dominant_colors(self, image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image."""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                rgb_image = image.convert('RGB')
            else:
                rgb_image = image
            
            # Quantize to reduce colors
            quantized = rgb_image.quantize(colors=num_colors)
            
            # Get color palette
            palette = quantized.getpalette()
            colors = []
            
            for i in range(0, min(len(palette), num_colors * 3), 3):
                color = (palette[i], palette[i+1], palette[i+2])
                colors.append(color)
            
            return colors[:num_colors]
            
        except Exception:
            return []

class FigureClassifier:
    """Classifies figures into different types."""
    
    def __init__(self):
        self.classification_keywords = self._load_classification_keywords()
    
    def _load_classification_keywords(self) -> Dict[FigureType, List[str]]:
        """Load keywords for figure type classification."""
        return {
            FigureType.CHART: ['chart', 'bar', 'pie', 'histogram', 'distribution'],
            FigureType.DIAGRAM: ['diagram', 'schematic', 'block', 'flow', 'structure'],
            FigureType.PHOTOGRAPH: ['photo', 'image', 'picture', 'microscopy', 'micrograph'],
            FigureType.PLOT: ['plot', 'curve', 'line', 'scatter', 'regression', 'data'],
            FigureType.GRAPH: ['graph', 'network', 'node', 'edge', 'tree', 'hierarchy'],
            FigureType.FLOWCHART: ['flowchart', 'flow', 'process', 'workflow', 'algorithm'],
            FigureType.SCHEMATIC: ['schematic', 'circuit', 'wiring', 'blueprint', 'layout'],
            FigureType.SCREENSHOT: ['screenshot', 'screen', 'interface', 'gui', 'application'],
            FigureType.MAP: ['map', 'geographic', 'spatial', 'location', 'region'],
            FigureType.ILLUSTRATION: ['illustration', 'drawing', 'sketch', 'artwork'],
            FigureType.TABLE_IMAGE: ['table', 'matrix', 'grid', 'data'],
            FigureType.EQUATION_IMAGE: ['equation', 'formula', 'mathematical', 'expression'],
            FigureType.UNKNOWN: []  # No keywords for unknown type
        }
    
    def classify_figure(self, image_analysis: ImageAnalysis, 
                       caption: Optional[FigureCaption] = None) -> FigureType:
        """Classify figure type based on analysis and caption."""
        
        # Initialize scores for each type
        type_scores = {fig_type: 0.0 for fig_type in FigureType}
        
        # Caption-based classification
        if caption:
            caption_text = caption.cleaned_text.lower()
            for fig_type, keywords in self.classification_keywords.items():
                for keyword in keywords:
                    if keyword in caption_text:
                        type_scores[fig_type] += 1.0
        
        # Image analysis-based classification
        self._classify_by_image_properties(image_analysis, type_scores)
        
        # Find the type with highest score
        best_type = max(type_scores, key=type_scores.get)
        
        # If no strong classification, return unknown
        if type_scores[best_type] < 0.5:
            return FigureType.UNKNOWN
        
        return best_type
    
    def _classify_by_image_properties(self, image_analysis: ImageAnalysis, 
                                    type_scores: Dict[FigureType, float]):
        """Classify based on image properties."""
        
        # High contrast and low color complexity suggests charts/graphs
        if image_analysis.contrast > 0.3 and image_analysis.color_complexity < 50:
            type_scores[FigureType.CHART] += 0.5
            type_scores[FigureType.GRAPH] += 0.5
        
        # High color complexity suggests photographs
        if image_analysis.color_complexity > 100:
            type_scores[FigureType.PHOTOGRAPH] += 0.5
        
        # Low color complexity and simple structure suggests diagrams
        if image_analysis.color_complexity < 20:
            type_scores[FigureType.DIAGRAM] += 0.3
            type_scores[FigureType.FLOWCHART] += 0.3
        
        # Aspect ratio analysis
        if image_analysis.width > 0 and image_analysis.height > 0:
            aspect_ratio = image_analysis.width / image_analysis.height
            
            # Wide images often charts or graphs
            if aspect_ratio > 1.5:
                type_scores[FigureType.CHART] += 0.2
                type_scores[FigureType.GRAPH] += 0.2
            
            # Square images often diagrams or photos
            elif 0.8 <= aspect_ratio <= 1.2:
                type_scores[FigureType.DIAGRAM] += 0.1
                type_scores[FigureType.PHOTOGRAPH] += 0.1

class AdvancedFigureProcessor:
    """Main processor for advanced figure analysis."""
    
    def __init__(self):
        self.caption_detector = CaptionDetector()
        self.image_analyzer = ImageAnalyzer()
        self.figure_classifier = FigureClassifier()
    
    def process_figures(self, pdf_content: bytes) -> Dict[str, Any]:
        """Process figures with advanced analysis."""
        logger.info("Starting advanced figure processing")
        
        try:
            # Open PDF document
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            
            all_figures = []
            all_captions = []
            
            # Extract figures and captions from each page
            for page_num in range(doc.page_count):
                page = doc[page_num]
                
                # Extract captions from text
                page_text = page.get_text()
                page_captions = self.caption_detector.detect_captions(page_text, page_num + 1)
                all_captions.extend(page_captions)
                
                # Extract images from page
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    try:
                        # Extract image data
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_data = base_image["image"]
                        
                        # Perform image analysis
                        image_analysis = self.image_analyzer.analyze_image(image_data)
                        
                        # Find associated caption
                        associated_caption = self._find_associated_caption(
                            page_captions, img_index, page_num + 1
                        )
                        
                        # Classify figure
                        figure_type = self.figure_classifier.classify_figure(
                            image_analysis, associated_caption
                        )
                        
                        # Extract text from image (basic implementation)
                        extracted_text = self._extract_text_from_image(image_data)
                        
                        # Calculate confidence
                        confidence = self._calculate_figure_confidence(
                            image_analysis, associated_caption, extracted_text
                        )
                        
                        # Get image position (approximate)
                        image_rect = page.get_image_bbox(img)
                        position = {
                            "x": image_rect.x0,
                            "y": image_rect.y0,
                            "width": image_rect.width,
                            "height": image_rect.height
                        }
                        
                        # Create advanced figure object
                        figure = AdvancedFigure(
                            figure_id=f"figure_{page_num+1}_{img_index+1}",
                            figure_type=figure_type,
                            page_number=page_num + 1,
                            position=position,
                            image_data=image_data,
                            image_analysis=image_analysis,
                            caption=associated_caption,
                            extracted_text=extracted_text,
                            confidence=confidence,
                            metadata=self._generate_figure_metadata(
                                image_analysis, associated_caption, figure_type
                            )
                        )
                        
                        all_figures.append(figure)
                        
                    except Exception as e:
                        logger.error(f"Failed to process image {img_index} on page {page_num + 1}: {str(e)}")
                        continue
            
            # Analyze figure relationships
            self._analyze_figure_relationships(all_figures)
            
            # Generate statistics
            stats = self._generate_figure_statistics(all_figures, all_captions)
            
            doc.close()
            
            return {
                "total_figures": len(all_figures),
                "figures": [fig.to_dict() for fig in all_figures],
                "total_captions": len(all_captions),
                "captions": [cap.to_dict() for cap in all_captions],
                "statistics": stats,
                "processing_status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Advanced figure processing failed: {str(e)}")
            return {
                "total_figures": 0,
                "figures": [],
                "total_captions": 0,
                "captions": [],
                "statistics": {},
                "processing_status": "failed",
                "error": str(e)
            }
    
    def _find_associated_caption(self, captions: List[FigureCaption], 
                               img_index: int, page_number: int) -> Optional[FigureCaption]:
        """Find caption associated with a figure."""
        # Simple heuristic: find caption with matching figure number
        # More sophisticated matching could use position analysis
        
        for caption in captions:
            if caption.figure_number:
                try:
                    fig_num = int(caption.figure_number)
                    if fig_num == img_index + 1:  # Assuming sequential numbering
                        return caption
                except ValueError:
                    continue
        
        # If no numbered match, return the first caption on the same page
        page_captions = [cap for cap in captions if cap.page_number == page_number]
        return page_captions[0] if page_captions else None
    
    def _extract_text_from_image(self, image_data: bytes) -> List[str]:
        """Extract text from image (placeholder for OCR functionality)."""
        # This is a placeholder - in a full implementation, this would use OCR
        # libraries like pytesseract or easyocr
        
        # For now, return empty list
        # In the future, implement:
        # try:
        #     import pytesseract
        #     image = Image.open(io.BytesIO(image_data))
        #     text = pytesseract.image_to_string(image)
        #     return [line.strip() for line in text.split('\n') if line.strip()]
        # except Exception:
        #     return []
        
        return []
    
    def _calculate_figure_confidence(self, image_analysis: ImageAnalysis,
                                   caption: Optional[FigureCaption],
                                   extracted_text: List[str]) -> float:
        """Calculate confidence score for figure extraction."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on image quality
        if image_analysis.quality == ImageQuality.EXCELLENT:
            confidence += 0.2
        elif image_analysis.quality == ImageQuality.GOOD:
            confidence += 0.1
        
        # Increase confidence if caption is present
        if caption:
            confidence += 0.2
            confidence += caption.confidence * 0.1
        
        # Increase confidence if text was extracted
        if extracted_text:
            confidence += 0.1
        
        # Increase confidence based on image size
        if image_analysis.width * image_analysis.height > 50000:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _generate_figure_metadata(self, image_analysis: ImageAnalysis,
                                caption: Optional[FigureCaption],
                                figure_type: FigureType) -> Dict[str, Any]:
        """Generate metadata for figure."""
        metadata = {
            "file_size_kb": image_analysis.file_size / 1024,
            "resolution": f"{image_analysis.width}x{image_analysis.height}",
            "aspect_ratio": image_analysis.width / image_analysis.height if image_analysis.height > 0 else 0,
            "color_mode": image_analysis.mode,
            "has_transparency": image_analysis.has_transparency,
            "estimated_type": figure_type.value
        }
        
        if caption:
            metadata["caption_length"] = len(caption.cleaned_text)
            metadata["caption_keywords"] = caption.keywords
        
        return metadata
    
    def _analyze_figure_relationships(self, figures: List[AdvancedFigure]):
        """Analyze relationships between figures."""
        # Simple relationship analysis based on similarity
        
        for i, fig1 in enumerate(figures):
            for j, fig2 in enumerate(figures):
                if i != j and self._are_figures_related(fig1, fig2):
                    fig1.related_figures.append(fig2.figure_id)
    
    def _are_figures_related(self, fig1: AdvancedFigure, fig2: AdvancedFigure) -> bool:
        """Determine if two figures are related."""
        # Figures are related if they:
        # 1. Are the same type
        # 2. Have similar dimensions
        # 3. Are on adjacent pages
        
        if fig1.figure_type == fig2.figure_type:
            return True
        
        # Check page proximity
        if abs(fig1.page_number - fig2.page_number) <= 1:
            return True
        
        # Check size similarity
        size1 = fig1.image_analysis.width * fig1.image_analysis.height
        size2 = fig2.image_analysis.width * fig2.image_analysis.height
        if size1 > 0 and size2 > 0:
            ratio = min(size1, size2) / max(size1, size2)
            if ratio > 0.8:  # Similar sizes
                return True
        
        return False
    
    def _generate_figure_statistics(self, figures: List[AdvancedFigure],
                                  captions: List[FigureCaption]) -> Dict[str, Any]:
        """Generate comprehensive figure statistics."""
        if not figures:
            return {}
        
        # Count by type
        type_counts = {}
        for fig in figures:
            fig_type = fig.figure_type.value
            type_counts[fig_type] = type_counts.get(fig_type, 0) + 1
        
        # Count by quality
        quality_counts = {}
        for fig in figures:
            quality = fig.image_analysis.quality.value
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        
        # Calculate average confidence
        avg_confidence = sum(fig.confidence for fig in figures) / len(figures)
        
        # Caption statistics
        captioned_figures = len([fig for fig in figures if fig.caption])
        avg_caption_length = 0
        if captions:
            avg_caption_length = sum(len(cap.cleaned_text) for cap in captions) / len(captions)
        
        # Size statistics
        avg_width = sum(fig.image_analysis.width for fig in figures) / len(figures)
        avg_height = sum(fig.image_analysis.height for fig in figures) / len(figures)
        avg_file_size = sum(fig.image_analysis.file_size for fig in figures) / len(figures)
        
        return {
            "total_figures": len(figures),
            "total_captions": len(captions),
            "figures_by_type": type_counts,
            "figures_by_quality": quality_counts,
            "average_confidence": round(avg_confidence, 3),
            "captioned_figures": captioned_figures,
            "caption_coverage": round(captioned_figures / len(figures), 3) if figures else 0,
            "average_caption_length": round(avg_caption_length, 1),
            "average_width": round(avg_width, 1),
            "average_height": round(avg_height, 1),
            "average_file_size_kb": round(avg_file_size / 1024, 1),
            "figures_with_relationships": len([fig for fig in figures if fig.related_figures])
        }

# Global advanced figure processor instance
_global_advanced_figure_processor = None

def get_advanced_figure_processor() -> AdvancedFigureProcessor:
    """Get global advanced figure processor instance."""
    global _global_advanced_figure_processor
    if _global_advanced_figure_processor is None:
        _global_advanced_figure_processor = AdvancedFigureProcessor()
    return _global_advanced_figure_processor

def process_advanced_figures(pdf_content: bytes) -> Dict[str, Any]:
    """Process figures with advanced analysis using global processor."""
    processor = get_advanced_figure_processor()
    return processor.process_figures(pdf_content) 