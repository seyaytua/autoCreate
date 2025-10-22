"""HTML解析モジュール（修正版）"""
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any

class HTMLParser:
    def __init__(self):
        # LaTeX数式パターン
        # $$...$$（ディスプレイ数式）
        self.display_math_pattern = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
        # $...$ または \(...\)（インライン数式）
        self.inline_math_pattern = re.compile(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)|\\\((.+?)\\\)', re.DOTALL)
    
    def parse(self, html_content: str) -> List[Dict[str, Any]]:
        """HTMLを解析して問題データを抽出"""
        soup = BeautifulSoup(html_content, 'html.parser')
        problems = []
        
        # 問題ブロックを探す
        problem_divs = soup.find_all('div', class_='problem')
        
        if not problem_divs:
            # class指定がない場合、h2タグで区切る
            problem_divs = self._split_by_headers(soup)
        
        for problem_div in problem_divs:
            problem_data = {
                'title': self._extract_title(problem_div),
                'text': self._extract_text(problem_div),
                'equations': self._extract_equations(problem_div),
                'choices': self._extract_choices(problem_div),
                'raw_html': str(problem_div)
            }
            problems.append(problem_data)
        
        return problems
    
    def _split_by_headers(self, soup):
        """h2タグで問題を分割"""
        problems = []
        current_problem = None
        
        for element in soup.find_all(['h2', 'p', 'div', 'ol', 'ul']):
            if element.name == 'h2':
                if current_problem:
                    problems.append(current_problem)
                current_problem = BeautifulSoup('<div class="problem"></div>', 'html.parser').div
                current_problem.append(element)
            elif current_problem is not None:
                current_problem.append(element)
        
        if current_problem:
            problems.append(current_problem)
        
        return problems
    
    def _extract_title(self, problem_div) -> str:
        """タイトルを抽出"""
        title_elem = problem_div.find(['h1', 'h2', 'h3'], class_='problem-title')
        if not title_elem:
            title_elem = problem_div.find(['h1', 'h2', 'h3'])
        
        return title_elem.get_text(strip=True) if title_elem else ""
    
    def _extract_text(self, problem_div) -> List[Dict[str, Any]]:
        """問題文を抽出（テキストと数式を分離）"""
        text_elements = []
        
        # 問題文パラグラフを探す
        text_paras = problem_div.find_all('p', class_='problem-text')
        if not text_paras:
            text_paras = problem_div.find_all('p')
        
        for para in text_paras:
            # パラグラフ内のテキストと数式を分離
            content = para.get_text()
            parts = self._split_text_and_math(content)
            
            for part in parts:
                text_elements.append(part)
        
        return text_elements
    
    def _split_text_and_math(self, text: str) -> List[Dict[str, Any]]:
        """テキスト内の数式を分離"""
        parts = []
        last_end = 0
        
        # まずディスプレイ数式を処理（$$...$$）
        display_matches = list(self.display_math_pattern.finditer(text))
        
        # 次にインライン数式を処理（$...$ または \(...\)）
        inline_matches = list(self.inline_math_pattern.finditer(text))
        
        # すべてのマッチを位置順にソート
        all_matches = sorted(
            display_matches + inline_matches,
            key=lambda m: m.start()
        )
        
        for match in all_matches:
            # 数式の前のテキスト
            if match.start() > last_end:
                plain_text = text[last_end:match.start()].strip()
                if plain_text:
                    parts.append({'type': 'text', 'content': plain_text})
            
            # 数式部分
            # ディスプレイ数式の場合
            if match in display_matches:
                latex_str = match.group(1).strip()
            # インライン数式の場合
            else:
                latex_str = (match.group(1) or match.group(2)).strip()
            
            if latex_str:
                parts.append({'type': 'math', 'content': latex_str})
            
            last_end = match.end()
        
        # 残りのテキスト
        if last_end < len(text):
            plain_text = text[last_end:].strip()
            if plain_text:
                parts.append({'type': 'text', 'content': plain_text})
        
        # 数式が見つからなかった場合は全体をテキストとして返す
        if not parts and text.strip():
            parts.append({'type': 'text', 'content': text.strip()})
        
        return parts
    
    def _extract_equations(self, problem_div) -> List[str]:
        """独立した数式ブロックを抽出"""
        equations = []
        
        # mathクラスのdivを探す
        math_divs = problem_div.find_all('div', class_='math')
        
        for math_div in math_divs:
            content = math_div.get_text(strip=True)
            # $$...$$を除去
            content = re.sub(r'^\$\$|\$\$$', '', content).strip()
            if content:
                equations.append(content)
        
        return equations
    
    def _extract_choices(self, problem_div) -> List[str]:
        """選択肢を抽出"""
        choices = []
        
        # olまたはulタグを探す
        choice_list = problem_div.find(['ol', 'ul'], class_='choices')
        if not choice_list:
            choice_list = problem_div.find(['ol', 'ul'])
        
        if choice_list:
            for li in choice_list.find_all('li'):
                choice_text = li.get_text(strip=True)
                choices.append(choice_text)
        
        return choices
