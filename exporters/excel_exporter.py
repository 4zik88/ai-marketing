"""
Модуль для экспорта данных в Excel и CSV
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ExcelExporter:
    """Класс для экспорта данных в Excel"""
    
    def __init__(self, output_dir: Path):
        """
        Инициализация экспортера
        
        Args:
            output_dir: Директория для сохранения файлов
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_google_ads(self, ads_data: Dict, filename: Optional[str] = None) -> str:
        """
        Экспортирует объявления Google Ads в Excel
        
        Args:
            ads_data: Данные объявлений
            filename: Имя файла (опционально)
            
        Returns:
            Путь к сохраненному файлу
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"google_ads_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        # Создаем DataFrame для каждого листа
        ads_list = ads_data.get('ads', [])
        
        # Лист 1: Все объявления
        all_ads = []
        for idx, ad in enumerate(ads_list, 1):
            for headline in ad.get('headlines', []):
                for description in ad.get('descriptions', []):
                    all_ads.append({
                        'Ad Group': f"Ad Group {idx}",
                        'Type': ad.get('type', ''),
                        'Headline': headline,
                        'Description': description,
                        'Path 1': ad.get('paths', [''])[0] if ad.get('paths') else '',
                        'Path 2': ad.get('paths', ['', ''])[1] if len(ad.get('paths', [])) > 1 else '',
                        'Keywords': ', '.join(ad.get('keywords', [])[:5]),
                        'Notes': ad.get('notes', '')
                    })
        
        df_ads = pd.DataFrame(all_ads)
        
        # Лист 2: Только заголовки
        headlines_data = []
        for idx, ad in enumerate(ads_list, 1):
            for headline in ad.get('headlines', []):
                headlines_data.append({
                    'Ad Group': f"Ad Group {idx}",
                    'Type': ad.get('type', ''),
                    'Headline': headline,
                    'Length': len(headline),
                    'Status': 'OK' if len(headline) <= 30 else 'TOO LONG'
                })
        
        df_headlines = pd.DataFrame(headlines_data)
        
        # Лист 3: Только описания
        descriptions_data = []
        for idx, ad in enumerate(ads_list, 1):
            for description in ad.get('descriptions', []):
                descriptions_data.append({
                    'Ad Group': f"Ad Group {idx}",
                    'Type': ad.get('type', ''),
                    'Description': description,
                    'Length': len(description),
                    'Status': 'OK' if len(description) <= 90 else 'TOO LONG'
                })
        
        df_descriptions = pd.DataFrame(descriptions_data)
        
        # Лист 4: Ключевые слова
        keywords_data = []
        for idx, ad in enumerate(ads_list, 1):
            for keyword in ad.get('keywords', []):
                keywords_data.append({
                    'Ad Group': f"Ad Group {idx}",
                    'Type': ad.get('type', ''),
                    'Keyword': keyword
                })
        
        df_keywords = pd.DataFrame(keywords_data)
        
        # Сохраняем в Excel с несколькими листами
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df_ads.to_excel(writer, sheet_name='All Ads', index=False)
            df_headlines.to_excel(writer, sheet_name='Headlines', index=False)
            df_descriptions.to_excel(writer, sheet_name='Descriptions', index=False)
            df_keywords.to_excel(writer, sheet_name='Keywords', index=False)
            
            # Форматирование
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        logger.info(f"Объявления экспортированы в: {filepath}")
        return str(filepath)
    
    def export_keywords(self, keywords_data: Dict, filename: Optional[str] = None) -> str:
        """
        Экспортирует ключевые слова в Excel
        
        Args:
            keywords_data: Данные ключевых слов
            filename: Имя файла (опционально)
            
        Returns:
            Путь к сохраненному файлу
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"keywords_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        # Подготавливаем данные
        keywords_list = []
        
        # Если keywords_data содержит различные типы соответствия
        if isinstance(keywords_data, dict) and 'keywords' in keywords_data:
            for kw_item in keywords_data['keywords']:
                keywords_list.append({
                    'Keyword': kw_item.get('keyword', ''),
                    'Match Type': kw_item.get('match_type', 'broad'),
                    'Search Volume': kw_item.get('search_volume', 'medium'),
                    'Commercial Intent': kw_item.get('commercial_intent', 'medium'),
                        'Category': kw_item.get('category', 'transactional')
                })
        elif isinstance(keywords_data, list):
            for kw in keywords_data:
                if isinstance(kw, str):
                    keywords_list.append({
                        'Keyword': kw,
                        'Match Type': 'broad',
                        'Search Volume': 'medium',
                        'Commercial Intent': 'medium',
                        'Category': 'транзакционный'
                    })
                elif isinstance(kw, dict):
                    keywords_list.append({
                        'Keyword': kw.get('keyword', ''),
                        'Match Type': kw.get('match_type', 'broad'),
                        'Search Volume': kw.get('search_volume', 'medium'),
                        'Commercial Intent': kw.get('commercial_intent', 'medium'),
                        'Category': kw.get('category', 'transactional')
                    })
        
        # Если нет ключевых слов, создаем базовые
        if not keywords_list:
            keywords_list = [
                {'Keyword': 'buy', 'Match Type': 'phrase', 'Search Volume': 'high', 'Commercial Intent': 'high', 'Category': 'transactional'},
                {'Keyword': 'price', 'Match Type': 'phrase', 'Search Volume': 'high', 'Commercial Intent': 'high', 'Category': 'transactional'},
                {'Keyword': 'order', 'Match Type': 'phrase', 'Search Volume': 'medium', 'Commercial Intent': 'high', 'Category': 'transactional'},
                {'Keyword': 'services', 'Match Type': 'broad', 'Search Volume': 'high', 'Commercial Intent': 'medium', 'Category': 'informational'},
            ]
        
        df = pd.DataFrame(keywords_list)
        
        # Сохраняем
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        logger.info(f"Ключевые слова экспортированы в: {filepath}")
        return str(filepath)
    
    def export_fab_analysis(self, fab_data: Dict, filename: Optional[str] = None) -> str:
        """
        Экспортирует FAB анализ в Excel
        
        Args:
            fab_data: Данные FAB анализа
            filename: Имя файла (опционально)
            
        Returns:
            Путь к сохраненному файлу
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fab_analysis_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        # Лист 1: Общая информация
        general_info = pd.DataFrame([{
            'Product Name': fab_data.get('product_name', ''),
            'Target Audience': fab_data.get('target_audience', ''),
            'Unique Value Proposition': fab_data.get('unique_value_proposition', '')
        }])
        
        # Лист 2: FAB утверждения
        fab_statements = []
        for statement in fab_data.get('fab_statements', []):
            fab_statements.append({
                'Feature': statement.get('feature', ''),
                'Advantage': statement.get('advantage', ''),
                'Benefit': statement.get('benefit', ''),
                'BAB Format': statement.get('bab_format', '')
            })
        
        df_fab = pd.DataFrame(fab_statements)
        
        # Сохраняем
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            general_info.to_excel(writer, sheet_name='General Info', index=False)
            df_fab.to_excel(writer, sheet_name='FAB Statements', index=False)
            
            # Форматирование
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 120)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        logger.info(f"FAB анализ экспортирован в: {filepath}")
        return str(filepath)
    
    def export_complete_report(self, website_data: Dict, fab_data: Dict, 
                              keywords_data: Dict, ads_data: Dict,
                              filename: Optional[str] = None) -> str:
        """
        Экспортирует полный отчет со всеми данными
        
        Args:
            website_data: Данные сайта
            fab_data: FAB анализ
            keywords_data: Ключевые слова
            ads_data: Объявления
            filename: Имя файла (опционально)
            
        Returns:
            Путь к сохраненному файлу
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"complete_report_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Лист 1: Информация о сайте
            site_info = pd.DataFrame([{
                'URL': website_data.get('url', ''),
                'Title': website_data.get('title', ''),
                'Description': website_data.get('description', ''),
                'Domain': website_data.get('domain', '')
            }])
            site_info.to_excel(writer, sheet_name='Website Info', index=False)
            
            # Get the worksheet to format it properly
            worksheet = writer.sheets['Website Info']
            
            # Set specific column widths for better readability (openpyxl method)
            worksheet.column_dimensions['A'].width = 20  # URL
            worksheet.column_dimensions['B'].width = 50  # Title
            worksheet.column_dimensions['C'].width = 100  # Description (much wider)
            worksheet.column_dimensions['D'].width = 20  # Domain
            
            # Enable text wrapping for description column
            from openpyxl.styles import Alignment
            for row in range(2, worksheet.max_row + 1):  # Skip header row
                worksheet.cell(row=row, column=3).alignment = Alignment(wrap_text=True, vertical='top')
            
            # Лист 2: FAB анализ
            fab_statements = []
            for statement in fab_data.get('fab_statements', []):
                fab_statements.append({
                    'Feature': statement.get('feature', ''),
                    'Advantage': statement.get('advantage', ''),
                    'Benefit': statement.get('benefit', ''),
                    'BAB Format': statement.get('bab_format', '')
                })
            df_fab = pd.DataFrame(fab_statements)
            df_fab.to_excel(writer, sheet_name='FAB Analysis', index=False)
            
            # Лист 3: Объявления
            all_ads = []
            for idx, ad in enumerate(ads_data.get('ads', []), 1):
                for headline in ad.get('headlines', []):
                    for description in ad.get('descriptions', []):
                        all_ads.append({
                            'Ad Group': f"Ad Group {idx}",
                            'Type': ad.get('type', ''),
                            'Headline': headline,
                            'Description': description,
                            'Path 1': ad.get('paths', [''])[0] if ad.get('paths') else '',
                            'Keywords': ', '.join(ad.get('keywords', [])[:3])
                        })
            df_ads = pd.DataFrame(all_ads)
            df_ads.to_excel(writer, sheet_name='Google Ads', index=False)
            
            # Лист 4: Ключевые слова
            keywords_list = []
            if isinstance(keywords_data, dict) and 'keywords' in keywords_data:
                for kw_item in keywords_data['keywords']:
                    keywords_list.append({
                        'Keyword': kw_item.get('keyword', ''),
                        'Match Type': kw_item.get('match_type', 'broad'),
                        'Search Volume': kw_item.get('search_volume', 'medium'),
                        'Commercial Intent': kw_item.get('commercial_intent', 'medium'),
                        'Category': kw_item.get('category', 'transactional')
                    })
            elif isinstance(keywords_data, list):
                for kw in keywords_data:
                    if isinstance(kw, str):
                        keywords_list.append({
                            'Keyword': kw,
                            'Match Type': 'broad',
                            'Search Volume': 'medium',
                            'Commercial Intent': 'medium',
                            'Category': 'transactional'
                        })
                    elif isinstance(kw, dict):
                        keywords_list.append({
                            'Keyword': kw.get('keyword', ''),
                            'Match Type': kw.get('match_type', 'broad'),
                            'Search Volume': kw.get('search_volume', 'medium'),
                            'Commercial Intent': kw.get('commercial_intent', 'medium'),
                            'Category': kw.get('category', 'transactional')
                        })
            
            df_keywords = pd.DataFrame(keywords_list)
            df_keywords.to_excel(writer, sheet_name='Keywords', index=False)
            
            # Автоматическое форматирование (openpyxl method)
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 120)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        logger.info(f"Полный отчет экспортирован в: {filepath}")
        return str(filepath)

