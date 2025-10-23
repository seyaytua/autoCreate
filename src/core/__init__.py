"""コアモジュール"""
from .style_config import STYLE_CONFIG, TEMPLATES
from .html_parser import HTMLParser
from .math_converter import MathConverter
from .word_generator import WordGenerator
from .template_manager import TemplateManager

__all__ = [
    'STYLE_CONFIG',
    'TEMPLATES',
    'HTMLParser',
    'MathConverter',
    'WordGenerator',
    'TemplateManager'
]
