#!/usr/bin/env python3
"""
Пример программного использования AI Marketing
(без CLI, через импорт модулей)
"""
from parsers import WebsiteParser
from ai import AIGenerator
from fab import FABMethodology
from exporters import ExcelExporter
from config import settings


def example_full_analysis():
    """Пример полного анализа сайта"""
    
    print("=" * 60)
    print("AI Marketing - Пример использования")
    print("=" * 60)
    
    # URL для анализа
    url = "https://www.example.com"
    
    # 1. Парсинг сайта
    print("\n1. Парсинг контента сайта...")
    parser = WebsiteParser()
    website_data = parser.parse_url(url)
    print(f"   ✓ Заголовок: {website_data['title']}")
    print(f"   ✓ Домен: {website_data['domain']}")
    
    # 2. FAB анализ
    print("\n2. Анализ по методологии FAB...")
    ai_generator = AIGenerator()
    fab_analysis = ai_generator.analyze_with_fab(website_data)
    print(f"   ✓ Продукт: {fab_analysis.get('product_name', 'N/A')}")
    print(f"   ✓ Целевая аудитория: {fab_analysis.get('target_audience', 'N/A')}")
    print(f"   ✓ FAB утверждений: {len(fab_analysis.get('fab_statements', []))}")
    
    # 3. Генерация ключевых слов
    print("\n3. Генерация ключевых слов...")
    keywords_data = ai_generator.generate_keywords(fab_analysis)
    print(f"   ✓ Ключевых слов: {len(keywords_data.get('keywords', []))}")
    
    # 4. Генерация объявлений
    print("\n4. Генерация объявлений Google Ads...")
    keywords_list = [kw.get('keyword', kw) if isinstance(kw, dict) else kw 
                    for kw in keywords_data.get('keywords', [])][:20]
    ads_data = ai_generator.generate_google_ads(fab_analysis, keywords_list)
    print(f"   ✓ Объявлений: {len(ads_data.get('ads', []))}")
    
    # 5. Экспорт в Excel
    print("\n5. Экспорт в Excel...")
    exporter = ExcelExporter(settings.output_dir)
    filepath = exporter.export_complete_report(
        website_data, fab_analysis, keywords_data, ads_data
    )
    print(f"   ✓ Файл сохранен: {filepath}")
    
    print("\n" + "=" * 60)
    print("✓ Анализ завершен успешно!")
    print("=" * 60)
    
    return {
        'website_data': website_data,
        'fab_analysis': fab_analysis,
        'keywords_data': keywords_data,
        'ads_data': ads_data,
        'output_file': filepath
    }


def example_custom_fab():
    """Пример создания собственных FAB утверждений"""
    
    from fab import FABStatement
    
    # Создаем FAB утверждение
    fab = FABStatement(
        feature="Онлайн-курс по Python из 10 модулей",
        advantage="Обучение в удобном темпе с доступом 24/7",
        benefit="Освойте программирование не отрываясь от основной работы"
    )
    
    print("\nFAB Утверждение:")
    print(f"Feature: {fab.feature}")
    print(f"Advantage: {fab.advantage}")
    print(f"Benefit: {fab.benefit}")
    
    print("\nBAB формат (для рекламы):")
    print(fab.to_baf())


def example_keywords_only():
    """Пример генерации только ключевых слов"""
    
    print("\n" + "=" * 60)
    print("Генерация ключевых слов")
    print("=" * 60)
    
    # Создаем упрощенный FAB анализ
    fab_analysis = {
        'product_name': 'Облачное хранилище для бизнеса',
        'target_audience': 'Малый и средний бизнес, удаленные команды',
        'unique_value_proposition': 'Безопасное хранение и совместная работа над документами',
        'fab_statements': [
            {
                'feature': '256-битное шифрование',
                'advantage': 'Максимальная защита данных',
                'benefit': 'Ваши документы в полной безопасности'
            }
        ]
    }
    
    ai_generator = AIGenerator()
    keywords_data = ai_generator.generate_keywords(fab_analysis)
    
    # Экспорт
    exporter = ExcelExporter(settings.output_dir)
    filepath = exporter.export_keywords(keywords_data, 'keywords_example.xlsx')
    
    print(f"✓ Ключевые слова сохранены: {filepath}")


def example_multiple_sites():
    """Пример парсинга нескольких сайтов"""
    
    urls = [
        "https://www.example1.com",
        "https://www.example2.com",
        "https://www.example3.com"
    ]
    
    parser = WebsiteParser()
    results = parser.parse_multiple_pages(urls)
    
    print(f"\n✓ Спарсено сайтов: {len(results)}")
    
    for result in results:
        print(f"\n- {result['domain']}")
        print(f"  Заголовок: {result['title'][:50]}...")


if __name__ == '__main__':
    # Раскомментируйте нужный пример:
    
    # example_full_analysis()
    example_custom_fab()
    # example_keywords_only()
    # example_multiple_sites()

