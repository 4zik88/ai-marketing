#!/usr/bin/env python3
"""
AI Marketing - Приложение для генерации рекламных материалов
на основе методологии FAB и AI
"""
import click
import logging
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from config import settings
from parsers import WebsiteParser
from ai import AIGenerator
from exporters import ExcelExporter

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_marketing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

console = Console()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    AI Marketing - Приложение для автоматической генерации
    рекламных материалов на основе методологии FAB.
    
    Использует AI для анализа сайтов и создания объявлений Google Ads.
    """
    pass


@cli.command()
@click.argument('url')
@click.option('--output', '-o', default=None, help='Имя выходного файла')
@click.option('--ai-provider', type=click.Choice(['openai', 'anthropic', 'google', 'ollama', 'groq']), 
              default=None, help='AI провайдер (ollama - бесплатно!)')
@click.option('--model', default=None, help='AI модель')
@click.option('--keywords-only', is_flag=True, help='Генерировать только ключевые слова')
def analyze(url, output, ai_provider, model, keywords_only):
    """
    Анализирует сайт и генерирует полный набор рекламных материалов.
    
    URL - адрес сайта для анализа
    
    Пример:
        python main.py analyze https://example.com
    """
    console.print(Panel.fit(
        "[bold blue]AI Marketing - Анализ сайта[/bold blue]",
        border_style="blue"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Шаг 1: Парсинг сайта
            task1 = progress.add_task("[cyan]Парсинг контента сайта...", total=None)
            parser = WebsiteParser()
            website_data = parser.parse_url(url)
            progress.update(task1, completed=True)
            console.print("✓ Контент сайта успешно спарсен", style="green")
            
            # Шаг 2: FAB анализ
            task2 = progress.add_task("[cyan]Анализ по методологии FAB...", total=None)
            ai_gen = AIGenerator(provider=ai_provider, model=model)
            fab_analysis = ai_gen.analyze_with_fab(website_data)
            progress.update(task2, completed=True)
            console.print("✓ FAB анализ завершен", style="green")
            
            # Отображаем результаты FAB анализа
            _display_fab_analysis(fab_analysis)
            
            # Шаг 3: Генерация ключевых слов
            task3 = progress.add_task("[cyan]Генерация ключевых слов...", total=None)
            keywords_data = ai_gen.generate_keywords(fab_analysis)
            progress.update(task3, completed=True)
            console.print("✓ Ключевые слова сгенерированы", style="green")
            
            if keywords_only:
                # Экспорт только ключевых слов
                exporter = ExcelExporter(settings.output_dir)
                filepath = exporter.export_keywords(keywords_data, output)
                console.print(f"\n[bold green]✓ Файл сохранен:[/bold green] {filepath}")
                return
            
            # Извлекаем список ключевых слов для объявлений
            keywords_list = []
            if isinstance(keywords_data, dict) and 'keywords' in keywords_data:
                keywords_list = [kw.get('keyword', kw) if isinstance(kw, dict) else kw 
                               for kw in keywords_data['keywords']]
            
            # Шаг 4: Генерация объявлений Google Ads
            task4 = progress.add_task("[cyan]Генерация объявлений Google Ads...", total=None)
            ads_data = ai_gen.generate_google_ads(fab_analysis, keywords_list[:20])
            progress.update(task4, completed=True)
            console.print("✓ Объявления сгенерированы", style="green")
            
            # Отображаем примеры объявлений
            _display_ads_preview(ads_data)
            
            # Шаг 5: Экспорт данных
            task5 = progress.add_task("[cyan]Экспорт данных в Excel...", total=None)
            exporter = ExcelExporter(settings.output_dir)
            filepath = exporter.export_complete_report(
                website_data, fab_analysis, keywords_data, ads_data, output
            )
            progress.update(task5, completed=True)
            console.print("✓ Данные экспортированы", style="green")
        
        console.print(f"\n[bold green]✓ Анализ завершен успешно![/bold green]")
        console.print(f"[bold]Файл сохранен:[/bold] {filepath}")
        console.print(f"[dim]Логи:[/dim] ai_marketing.log")
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Ошибка:[/bold red] {str(e)}")
        logger.exception("Ошибка при выполнении анализа")
        raise click.Abort()


@cli.command()
@click.argument('url')
@click.option('--output', '-o', default=None, help='Имя выходного файла')
def parse(url, output):
    """
    Только парсит сайт без AI анализа.
    
    URL - адрес сайта для парсинга
    """
    console.print("[cyan]Парсинг сайта...[/cyan]")
    
    try:
        parser = WebsiteParser()
        website_data = parser.parse_url(url)
        
        # Отображаем результаты
        table = Table(title="Результаты парсинга")
        table.add_column("Параметр", style="cyan")
        table.add_column("Значение", style="green")
        
        table.add_row("URL", website_data['url'])
        table.add_row("Title", website_data['title'][:100])
        table.add_row("Description", website_data['description'][:100])
        table.add_row("Domain", website_data['domain'])
        table.add_row("H1 Tags", str(len(website_data['headings'].get('h1', []))))
        
        console.print(table)
        console.print(f"\n[bold green]✓ Парсинг завершен[/bold green]")
        
        # Сохранение если требуется
        if output:
            import json
            output_path = settings.output_dir / output
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(website_data, f, ensure_ascii=False, indent=2)
            console.print(f"[bold]Данные сохранены:[/bold] {output_path}")
        
    except Exception as e:
        console.print(f"[bold red]✗ Ошибка:[/bold red] {str(e)}")
        logger.exception("Ошибка при парсинге")
        raise click.Abort()


@cli.command()
def config_info():
    """Показывает текущую конфигурацию."""
    table = Table(title="Конфигурация AI Marketing")
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="green")
    
    table.add_row("AI Provider", settings.ai_provider)
    table.add_row("AI Model", settings.ai_model)
    table.add_row("Output Directory", str(settings.output_dir))
    table.add_row("OpenAI API Key", "✓ Установлен" if settings.openai_api_key else "✗ Не установлен")
    table.add_row("Anthropic API Key", "✓ Установлен" if settings.anthropic_api_key else "✗ Не установлен")
    
    console.print(table)


def _display_fab_analysis(fab_data: dict):
    """Отображает результаты FAB анализа"""
    console.print("\n[bold]FAB Анализ:[/bold]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Параметр", style="cyan", width=20)
    table.add_column("Значение", style="white")
    
    table.add_row("Продукт", fab_data.get('product_name', 'N/A'))
    table.add_row("Целевая аудитория", fab_data.get('target_audience', 'N/A'))
    table.add_row("Уник. предложение", fab_data.get('unique_value_proposition', 'N/A'))
    
    console.print(table)
    
    # Отображаем FAB утверждения
    if fab_data.get('fab_statements'):
        console.print("\n[bold]FAB Утверждения:[/bold]")
        for idx, statement in enumerate(fab_data['fab_statements'][:3], 1):
            console.print(f"\n[yellow]{idx}. BAB формат:[/yellow]")
            console.print(f"  {statement.get('bab_format', 'N/A')}")


def _display_ads_preview(ads_data: dict):
    """Отображает превью объявлений"""
    console.print("\n[bold]Превью объявлений:[/bold]")
    
    ads = ads_data.get('ads', [])[:2]  # Показываем первые 2
    
    for idx, ad in enumerate(ads, 1):
        console.print(f"\n[bold cyan]Объявление {idx} ({ad.get('type', 'N/A')}):[/bold cyan]")
        
        headlines = ad.get('headlines', [])[:2]
        descriptions = ad.get('descriptions', [])[:1]
        
        for h in headlines:
            console.print(f"  [green]Заголовок:[/green] {h} [dim]({len(h)} символов)[/dim]")
        
        for d in descriptions:
            console.print(f"  [blue]Описание:[/blue] {d} [dim]({len(d)} символов)[/dim]")


@cli.command()
def setup():
    """Интерактивная настройка конфигурации."""
    console.print(Panel.fit(
        "[bold blue]Настройка AI Marketing[/bold blue]",
        border_style="blue"
    ))
    
    console.print("\n[yellow]Для работы приложения нужен AI провайдер.[/yellow]")
    console.print("\n[bold green]🆓 БЕСПЛАТНЫЕ варианты:[/bold green]\n")
    
    console.print("[cyan]1. Ollama (РЕКОМЕНДУЕТСЯ - 100% бесплатно, локально)[/cyan]")
    console.print("   brew install ollama  # установка")
    console.print("   ollama pull llama3.1  # скачать модель")
    console.print("   В .env: AI_PROVIDER=ollama\n")
    
    console.print("[cyan]2. Google Gemini (бесплатно, отличное качество)[/cyan]")
    console.print("   API ключ: https://makersuite.google.com/app/apikey")
    console.print("   В .env: GOOGLE_API_KEY=your_key, AI_PROVIDER=google\n")
    
    console.print("[cyan]3. Groq (бесплатно, очень быстро)[/cyan]")
    console.print("   API ключ: https://console.groq.com")
    console.print("   В .env: GROQ_API_KEY=your_key, AI_PROVIDER=groq\n")
    
    console.print("[yellow]💰 Платные варианты:[/yellow]")
    console.print("   OpenAI GPT-4 / Anthropic Claude\n")
    
    console.print(f"[green]✓ Подробная инструкция:[/green] FREE_AI_SETUP.md")
    console.print(f"[green]✓ Пример конфигурации:[/green] .env.example")


@cli.group()
def google_ads():
    """
    Команды для работы с Google Ads API (MCP Server).
    
    Требуется настройка google-ads.yaml с API credentials.
    См. GOOGLE_ADS_SETUP.md для инструкций.
    """
    pass


@google_ads.command('list-accounts')
def google_ads_list_accounts():
    """Показать все доступные аккаунты Google Ads."""
    try:
        from google_ads import GoogleAdsMCPServer
        
        console.print("[cyan]Получение списка аккаунтов...[/cyan]")
        mcp = GoogleAdsMCPServer()
        result = mcp.list_accounts()
        
        if result['success']:
            table = Table(title="Доступные аккаунты Google Ads")
            table.add_column("Customer ID", style="cyan")
            table.add_column("Resource Name", style="green")
            
            for account in result['accounts']:
                table.add_row(account['id'], account['resource_name'])
            
            console.print(table)
            console.print(f"\n[green]✓ Найдено аккаунтов: {result['count']}[/green]")
        else:
            console.print(f"[red]✗ Ошибка: {result['error']}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при получении аккаунтов")


@google_ads.command('account-summary')
@click.option('--date-range', default='LAST_30_DAYS', help='Период данных')
def google_ads_account_summary(date_range):
    """Показать сводку по аккаунту."""
    try:
        from google_ads import GoogleAdsMCPServer
        
        console.print(f"[cyan]Получение сводки за {date_range}...[/cyan]")
        mcp = GoogleAdsMCPServer()
        result = mcp.get_account_summary(date_range)
        
        if result['success'] and result['summary']:
            summary = result['summary']
            
            table = Table(title=f"Сводка по аккаунту ({date_range})")
            table.add_column("Метрика", style="cyan")
            table.add_column("Значение", style="green")
            
            if 'metrics' in summary:
                metrics = summary['metrics']
                table.add_row("Показы", f"{metrics.get('impressions', 0):,}")
                table.add_row("Клики", f"{metrics.get('clicks', 0):,}")
                table.add_row("CTR", f"{metrics.get('ctr', 0):.2%}" if 'ctr' in metrics else "N/A")
                table.add_row("Стоимость", f"${metrics.get('cost_micros', 0) / 1_000_000:.2f}")
                table.add_row("Конверсии", f"{metrics.get('conversions', 0):.1f}")
            
            console.print(table)
        else:
            console.print(f"[red]✗ Ошибка: {result.get('error', 'Нет данных')}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при получении сводки")


@google_ads.command('campaigns')
@click.option('--campaign-id', default=None, help='ID конкретной кампании')
@click.option('--date-range', default='LAST_30_DAYS', help='Период данных')
@click.option('--status', default=None, help='Фильтр по статусу (ENABLED, PAUSED, REMOVED)')
def google_ads_campaigns(campaign_id, date_range, status):
    """Показать кампании и их производительность."""
    try:
        from google_ads import GoogleAdsMCPServer
        
        console.print(f"[cyan]Получение данных кампаний...[/cyan]")
        mcp = GoogleAdsMCPServer()
        
        if campaign_id:
            result = mcp.get_campaign_performance(campaign_id, date_range)
        else:
            result = mcp.get_campaigns(date_range, status)
        
        if result['success']:
            campaigns = [result['campaign']] if campaign_id else result.get('campaigns', [])
            
            table = Table(title=f"Кампании ({date_range})")
            table.add_column("ID", style="cyan")
            table.add_column("Название", style="yellow")
            table.add_column("Статус", style="green")
            table.add_column("Показы", style="blue")
            table.add_column("Клики", style="magenta")
            table.add_column("Стоимость", style="red")
            
            for campaign in campaigns[:20]:  # Показываем первые 20
                camp_data = campaign.get('campaign', {})
                metrics = campaign.get('metrics', {})
                
                table.add_row(
                    str(camp_data.get('id', 'N/A')),
                    camp_data.get('name', 'N/A')[:30],
                    camp_data.get('status', 'N/A'),
                    f"{metrics.get('impressions', 0):,}",
                    f"{metrics.get('clicks', 0):,}",
                    f"${metrics.get('cost_micros', 0) / 1_000_000:.2f}"
                )
            
            console.print(table)
            if not campaign_id:
                console.print(f"\n[green]✓ Найдено кампаний: {result['count']}[/green]")
        else:
            console.print(f"[red]✗ Ошибка: {result['error']}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при получении кампаний")


@google_ads.command('keywords')
@click.option('--campaign-id', default=None, help='ID кампании')
@click.option('--date-range', default='LAST_30_DAYS', help='Период данных')
@click.option('--min-impressions', default=0, help='Минимум показов')
def google_ads_keywords(campaign_id, date_range, min_impressions):
    """Показать производительность ключевых слов."""
    try:
        from google_ads import GoogleAdsMCPServer
        
        console.print(f"[cyan]Получение данных по ключевым словам...[/cyan]")
        mcp = GoogleAdsMCPServer()
        result = mcp.get_keywords(campaign_id, date_range, min_impressions)
        
        if result['success']:
            keywords = result.get('keywords', [])
            
            table = Table(title=f"Ключевые слова ({date_range})")
            table.add_column("Ключевое слово", style="cyan")
            table.add_column("Тип", style="yellow")
            table.add_column("Показы", style="blue")
            table.add_column("Клики", style="magenta")
            table.add_column("CTR", style="green")
            table.add_column("Стоимость", style="red")
            
            for kw in keywords[:30]:  # Первые 30
                metrics = kw.get('metrics', {})
                ctr = metrics.get('ctr', 0) * 100 if 'ctr' in metrics else 0
                
                table.add_row(
                    kw.get('keyword', 'N/A')[:40],
                    kw.get('match_type', 'N/A'),
                    f"{metrics.get('impressions', 0):,}",
                    f"{metrics.get('clicks', 0):,}",
                    f"{ctr:.2f}%",
                    f"${metrics.get('cost_micros', 0) / 1_000_000:.2f}"
                )
            
            console.print(table)
            console.print(f"\n[green]✓ Найдено ключевых слов: {result['count']}[/green]")
        else:
            console.print(f"[red]✗ Ошибка: {result['error']}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при получении ключевых слов")


@google_ads.command('search-terms')
@click.option('--campaign-id', default=None, help='ID кампании')
@click.option('--date-range', default='LAST_7_DAYS', help='Период данных')
def google_ads_search_terms(campaign_id, date_range):
    """Показать отчет по поисковым запросам."""
    try:
        from google_ads import GoogleAdsMCPServer
        
        console.print(f"[cyan]Получение поисковых запросов...[/cyan]")
        mcp = GoogleAdsMCPServer()
        result = mcp.get_search_terms(campaign_id, date_range)
        
        if result['success']:
            terms = result.get('search_terms', [])
            
            table = Table(title=f"Поисковые запросы ({date_range})")
            table.add_column("Запрос", style="cyan")
            table.add_column("Показы", style="blue")
            table.add_column("Клики", style="magenta")
            table.add_column("CTR", style="green")
            table.add_column("Стоимость", style="red")
            
            for term in terms[:30]:
                metrics = term.get('metrics', {})
                ctr = metrics.get('ctr', 0) * 100 if 'ctr' in metrics else 0
                
                table.add_row(
                    term.get('search_term', 'N/A')[:50],
                    f"{metrics.get('impressions', 0):,}",
                    f"{metrics.get('clicks', 0):,}",
                    f"{ctr:.2f}%",
                    f"${metrics.get('cost_micros', 0) / 1_000_000:.2f}"
                )
            
            console.print(table)
            console.print(f"\n[green]✓ Найдено запросов: {result['count']}[/green]")
        else:
            console.print(f"[red]✗ Ошибка: {result['error']}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при получении поисковых запросов")


@google_ads.command('diagnose-quality')
@click.option('--min-impressions', default=100, help='Минимум показов')
def google_ads_diagnose_quality(min_impressions):
    """Диагностика: найти ключевые слова с низким показателем качества."""
    try:
        from google_ads import GoogleAdsMCPServer
        
        console.print(f"[cyan]Поиск ключевых слов с низким показателем качества...[/cyan]")
        mcp = GoogleAdsMCPServer()
        result = mcp.diagnose_low_quality_scores(min_impressions)
        
        if result['success']:
            keywords = result.get('low_quality_keywords', [])
            
            if keywords:
                table = Table(title="⚠️  Ключевые слова с низким показателем качества (< 5)")
                table.add_column("Кампания", style="yellow")
                table.add_column("Ключевое слово", style="cyan")
                table.add_column("Показатель качества", style="red")
                table.add_column("Показы", style="blue")
                table.add_column("CTR", style="green")
                
                for kw in keywords[:20]:
                    metrics = kw.get('metrics', {})
                    ctr = metrics.get('ctr', 0) * 100 if 'ctr' in metrics else 0
                    
                    table.add_row(
                        kw.get('campaign_name', 'N/A')[:30],
                        kw.get('keyword', 'N/A')[:40],
                        str(kw.get('quality_score', 'N/A')),
                        f"{metrics.get('impressions', 0):,}",
                        f"{ctr:.2f}%"
                    )
                
                console.print(table)
                console.print(f"\n[yellow]Рекомендация:[/yellow] {result.get('recommendation', '')}")
            else:
                console.print("[green]✓ Не найдено ключевых слов с низким показателем качества![/green]")
            
            console.print(f"\n[green]✓ Найдено проблем: {result['count']}[/green]")
        else:
            console.print(f"[red]✗ Ошибка: {result['error']}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при диагностике")


@google_ads.command('diagnose-cost')
def google_ads_diagnose_cost():
    """Диагностика: найти кампании с высокой стоимостью но низкими конверсиями."""
    try:
        from google_ads import GoogleAdsMCPServer
        
        console.print(f"[cyan]Поиск дорогих кампаний с низкими конверсиями...[/cyan]")
        mcp = GoogleAdsMCPServer()
        result = mcp.diagnose_high_cost_campaigns()
        
        if result['success']:
            campaigns = result.get('campaigns', [])
            
            if campaigns:
                table = Table(title="⚠️  Кампании с высокой стоимостью и низкими конверсиями")
                table.add_column("Кампания", style="yellow")
                table.add_column("Статус", style="cyan")
                table.add_column("Стоимость", style="red")
                table.add_column("Конверсии", style="green")
                table.add_column("Цена конверсии", style="magenta")
                
                for camp in campaigns:
                    metrics = camp.get('metrics', {})
                    
                    table.add_row(
                        camp.get('name', 'N/A')[:40],
                        camp.get('status', 'N/A'),
                        f"${metrics.get('cost_micros', 0) / 1_000_000:.2f}",
                        f"{metrics.get('conversions', 0):.1f}",
                        f"${metrics.get('cost_per_conversion', 0) / 1_000_000:.2f}" if metrics.get('cost_per_conversion') else "N/A"
                    )
                
                console.print(table)
                console.print(f"\n[yellow]Рекомендация:[/yellow] {result.get('recommendation', '')}")
            else:
                console.print("[green]✓ Не найдено проблемных кампаний![/green]")
            
            console.print(f"\n[green]✓ Найдено проблем: {result['count']}[/green]")
        else:
            console.print(f"[red]✗ Ошибка: {result['error']}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при диагностике")


@google_ads.command('query')
@click.argument('gaql_query')
def google_ads_custom_query(gaql_query):
    """Выполнить произвольный GAQL запрос."""
    try:
        from google_ads import GoogleAdsMCPServer
        import json
        
        console.print(f"[cyan]Выполнение запроса...[/cyan]")
        mcp = GoogleAdsMCPServer()
        result = mcp.run_custom_query(gaql_query)
        
        if result['success']:
            console.print(f"\n[green]✓ Найдено результатов: {result['count']}[/green]\n")
            # Выводим первые результаты в JSON формате
            console.print(json.dumps(result['results'][:5], indent=2, ensure_ascii=False))
            
            if result['count'] > 5:
                console.print(f"\n[dim]... и еще {result['count'] - 5} результатов[/dim]")
        else:
            console.print(f"[red]✗ Ошибка: {result['error']}[/red]")
    except ImportError:
        console.print("[red]✗ Google Ads API не установлен. Запустите: pip install google-ads[/red]")
    except Exception as e:
        console.print(f"[red]✗ Ошибка: {str(e)}[/red]")
        logger.exception("Ошибка при выполнении запроса")


if __name__ == '__main__':
    cli()

