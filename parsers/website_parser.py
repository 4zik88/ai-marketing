"""
Модуль для парсинга контента веб-сайтов
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import trafilatura
from urllib.parse import urlparse, urljoin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebsiteParser:
    """Класс для парсинга контента сайта"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse_url(self, url: str) -> Dict[str, any]:
        """
        Парсит URL и извлекает ключевую информацию
        
        Args:
            url: URL для парсинга
            
        Returns:
            Словарь с извлеченными данными
        """
        try:
            logger.info(f"Парсинг URL: {url}")
            
            # Получаем HTML
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            html = response.text
            
            # Используем trafilatura для извлечения основного контента
            extracted_text = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=True,
                favor_precision=True
            )
            
            # Используем BeautifulSoup для дополнительной информации
            soup = BeautifulSoup(html, 'lxml')
            
            # Извлекаем мета-данные
            title = self._extract_title(soup)
            description = self._extract_meta_description(soup)
            keywords = self._extract_meta_keywords(soup)
            headings = self._extract_headings(soup)
            
            # Извлекаем ссылки
            links = self._extract_links(soup, url)
            
            result = {
                'url': url,
                'title': title,
                'description': description,
                'keywords': keywords,
                'headings': headings,
                'main_content': extracted_text or '',
                'links': links,
                'domain': urlparse(url).netloc
            }
            
            logger.info(f"Успешно спарсен: {url}")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге {url}: {e}")
            raise
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Извлекает заголовок страницы"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Альтернатива: Open Graph title
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()
        
        return ''
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Извлекает мета-описание"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # Альтернатива: Open Graph description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()
        
        return ''
    
    def _extract_meta_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Извлекает мета-ключевые слова"""
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            keywords = meta_keywords['content'].split(',')
            return [k.strip() for k in keywords if k.strip()]
        return []
    
    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Извлекает заголовки H1-H6"""
        headings = {}
        for i in range(1, 7):
            tag = f'h{i}'
            tags = soup.find_all(tag)
            headings[tag] = [h.get_text().strip() for h in tags if h.get_text().strip()]
        return headings
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Извлекает все ссылки со страницы"""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Преобразуем относительные URL в абсолютные
            full_url = urljoin(base_url, href)
            if full_url.startswith('http'):
                links.append(full_url)
        return list(set(links))  # Убираем дубликаты
    
    def parse_multiple_pages(self, urls: List[str]) -> List[Dict[str, any]]:
        """
        Парсит несколько страниц
        
        Args:
            urls: Список URL для парсинга
            
        Returns:
            Список словарей с данными
        """
        results = []
        for url in urls:
            try:
                result = self.parse_url(url)
                results.append(result)
            except Exception as e:
                logger.error(f"Ошибка при парсинге {url}: {e}")
                continue
        return results

