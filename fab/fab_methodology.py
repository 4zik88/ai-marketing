"""
Модуль для работы с методологией FAB (Features, Advantages, Benefits)
"""
from typing import Dict, List
from pydantic import BaseModel


class FABStatement(BaseModel):
    """Модель FAB утверждения"""
    feature: str  # Характеристика
    advantage: str  # Преимущество
    benefit: str  # Выгода/Удобство
    
    def to_baf(self) -> str:
        """
        Преобразует в BAF (Benefit-Advantage-Feature) формат
        для эмоционального воздействия
        """
        return f"{self.benefit}. {self.advantage}. {self.feature}."
    
    def to_dict(self) -> Dict[str, str]:
        """Преобразует в словарь"""
        return {
            'feature': self.feature,
            'advantage': self.advantage,
            'benefit': self.benefit
        }


class FABMethodology:
    """Класс для работы с FAB методологией"""
    
    @staticmethod
    def get_fab_prompt() -> str:
        """
        Возвращает полное описание FAB методологии для промпта AI
        """
        return """
The FAB method (Features, Advantages, Benefits) is a key sales and marketing tool.

**Important principles:**
- People buy NOT features or advantages, they buy the FINAL BENEFIT
- People buy on EMOTIONS, then justify with logic

**FAB Components:**

1. **FEATURE:**
   - This is a special property, aspect, or specification of your product/service
   - "What you're selling" or "bare facts"
   - Often technical in nature
   - Examples: "5-module online course", "High-speed printer", "24-megapixel camera"

2. **ADVANTAGE:**
   - Positive effect or result brought by the feature
   - Explains why the product is convenient and needed
   - Bridge between feature and benefit
   - Examples: "High print speed ensures more printing volume per day", "24 megapixels mean clearer images"

3. **BENEFIT:**
   - Personal advantages, improvements, or values for the customer
   - "What benefit will your customer get"
   - Answers the question: how does this help the customer, what can it do for them
   - Speaks about what customers really want
   - Solves their problems, brings joy, convenience, or relief
   - Examples: "Less waiting time, increased productivity", "Your child will be safe", "You drink delicious coffee"

**BAB Method (Reverse FAB):**
Start with BENEFIT to emotionally attract the customer, then support with advantages and features.

Example: "Don't miss any moment of your life when there's no light (Benefit). Lens lets in more light (Advantage). F 1.2 aperture (Feature)."

**Writing rules:**
- Use simple and clear language
- Avoid overly general or complex phrases
- Focus on unique value
- Consider target audience needs
"""
    
    @staticmethod
    def create_fab_analysis_prompt(content: Dict[str, any]) -> str:
        """
        Создает промпт для анализа контента сайта по методологии FAB
        
        Args:
            content: Словарь с данными о сайте
        """
        return f"""
Analyze the following website content and apply the FAB methodology.

**Website data:**
Title: {content.get('title', 'Not specified')}
Description: {content.get('description', 'Not specified')}
Domain: {content.get('domain', 'Not specified')}

**Headings:**
{content.get('headings', {})}

**Main content:**
{content.get('main_content', '')[:2000]}  

**Task:**
1. Identify the main product or service being offered
2. Extract or determine at least 3-5 FAB statements
3. For each statement determine:
   - Feature - what is specifically offered
   - Advantage - why this is good
   - Benefit - what value the customer will get

4. Formulate each statement in BAB format (starting with benefit)

IMPORTANT: Keep the original language of the website content. If the website is in Ukrainian, respond in Ukrainian. If in English, respond in English. If in Russian, respond in Russian. Only the analysis structure should be consistent.

Return result in JSON format:
{{
    "product_name": "product/service name",
    "target_audience": "target audience description",
    "fab_statements": [
        {{
            "feature": "feature",
            "advantage": "advantage",
            "benefit": "benefit",
            "bab_format": "benefit. advantage. feature."
        }}
    ],
    "unique_value_proposition": "brief unique value proposition"
}}
"""
    
    @staticmethod
    def create_keyword_generation_prompt(fab_analysis: Dict[str, any]) -> str:
        """
        Создает промпт для генерации ключевых слов на основе FAB анализа
        """
        return f"""
Based on the FAB analysis of the product/service, generate keywords for Google Ads.

**Product data:**
Name: {fab_analysis.get('product_name', '')}
Target audience: {fab_analysis.get('target_audience', '')}
Unique value proposition: {fab_analysis.get('unique_value_proposition', '')}

**FAB statements:**
{fab_analysis.get('fab_statements', [])}

**Requirements:**
1. Create keywords for 4 match types:
   - Broad match
   - Phrase match  
   - Exact match
   - Modified broad match

2. Include:
   - Informational queries (how, what, why)
   - Transactional queries (buy, order, price)
   - Brand queries
   - Competitor queries (if applicable)
   - Long-tail keywords

3. For each keyword specify:
   - Match type
   - Approximate search volume (high/medium/low)
   - Commercial intent (high/medium/low)

IMPORTANT: Generate keywords in the same language as the website content. If the website is in Ukrainian, generate Ukrainian keywords. If in English, generate English keywords. If in Russian, generate Russian keywords.

Return result in JSON format:
{{
    "keywords": [
        {{
            "keyword": "keyword",
            "match_type": "broad|phrase|exact|modified_broad",
            "search_volume": "high|medium|low",
            "commercial_intent": "high|medium|low",
            "category": "informational|transactional|navigational"
        }}
    ]
}}
"""


class FABTemplate:
    """Шаблоны для различных индустрий"""
    
    TEMPLATES = {
        "saas": {
            "feature_examples": [
                "Облачное хранилище",
                "Автоматизация процессов",
                "Интеграция с API"
            ],
            "advantage_examples": [
                "Доступ из любого места",
                "Экономия времени",
                "Единая экосистема"
            ],
            "benefit_examples": [
                "Работайте откуда угодно",
                "Сосредоточьтесь на главном",
                "Все инструменты под рукой"
            ]
        },
        "ecommerce": {
            "feature_examples": [
                "Быстрая доставка",
                "Широкий ассортимент",
                "Гарантия возврата"
            ],
            "advantage_examples": [
                "Получение за 1-2 дня",
                "Выбор из 10000+ товаров",
                "30 дней на возврат"
            ],
            "benefit_examples": [
                "Получите заказ уже завтра",
                "Найдете именно то, что нужно",
                "Покупайте без риска"
            ]
        },
        "services": {
            "feature_examples": [
                "Команда экспертов",
                "Индивидуальный подход",
                "Гарантия результата"
            ],
            "advantage_examples": [
                "Опыт более 10 лет",
                "Решение под ваши задачи",
                "Ответственность за результат"
            ],
            "benefit_examples": [
                "Доверьтесь профессионалам",
                "Получите именно то, что нужно",
                "Достигните целей с гарантией"
            ]
        }
    }
    
    @classmethod
    def get_template(cls, industry: str) -> Dict[str, List[str]]:
        """Получить шаблон для индустрии"""
        return cls.TEMPLATES.get(industry.lower(), cls.TEMPLATES["services"])

