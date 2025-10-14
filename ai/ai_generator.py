"""
Модуль для работы с AI API (OpenAI, Anthropic, Google, Ollama, Groq)
Поддерживает как платные, так и бесплатные провайдеры
"""
import json
import logging
from typing import Dict, Optional, List
from config import settings

logger = logging.getLogger(__name__)


class AIGenerator:
    """Класс для генерации контента с помощью AI"""
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Инициализация генератора
        
        Args:
            provider: AI провайдер ('openai', 'anthropic', 'google', 'ollama', 'groq')
            model: Название модели
        """
        self.provider = provider or settings.ai_provider
        self.model = model or settings.ai_model
        
        # Инициализируем клиент
        if self.provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.openai_api_key)
            except ImportError:
                raise ImportError("Установите openai: pip install openai")
        
        elif self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=settings.anthropic_api_key)
            except ImportError:
                raise ImportError("Установите anthropic: pip install anthropic")
        
        elif self.provider == "google":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.google_api_key)
                self.client = genai
            except ImportError:
                raise ImportError("Установите google-generativeai: pip install google-generativeai")
        
        elif self.provider == "ollama":
            try:
                import ollama
                self.client = ollama
                logger.info(f"Используется Ollama с моделью {self.model}")
            except ImportError:
                raise ImportError("Установите ollama: pip install ollama")
        
        elif self.provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.groq_api_key)
            except ImportError:
                raise ImportError("Установите groq: pip install groq")
        
        else:
            raise ValueError(f"Неизвестный провайдер: {self.provider}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, json_mode: bool = False) -> str:
        """
        Генерирует ответ от AI
        
        Args:
            prompt: Пользовательский промпт
            system_prompt: Системный промпт
            temperature: Температура генерации (0-1)
            json_mode: Если True, ответ будет в формате JSON
            
        Returns:
            Сгенерированный текст
        """
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, system_prompt, temperature, json_mode)
            elif self.provider == "anthropic":
                return self._generate_anthropic(prompt, system_prompt, temperature, json_mode)
            elif self.provider == "google":
                return self._generate_google(prompt, system_prompt, temperature, json_mode)
            elif self.provider == "ollama":
                return self._generate_ollama(prompt, system_prompt, temperature, json_mode)
            elif self.provider == "groq":
                return self._generate_groq(prompt, system_prompt, temperature, json_mode)
        except Exception as e:
            logger.error(f"Ошибка генерации: {e}")
            raise
    
    def _generate_openai(self, prompt: str, system_prompt: Optional[str], 
                         temperature: float, json_mode: bool) -> str:
        """Генерация через OpenAI"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str, system_prompt: Optional[str], 
                           temperature: float, json_mode: bool) -> str:
        """Генерация через Anthropic"""
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
    
    def _generate_google(self, prompt: str, system_prompt: Optional[str], 
                        temperature: float, json_mode: bool) -> str:
        """Генерация через Google Gemini (БЕСПЛАТНО!)"""
        # Используем правильные модели для API v1beta
        if "flash" in self.model.lower():
            model_name = "gemini-2.0-flash"
        elif "pro" in self.model.lower():
            model_name = "gemini-2.5-pro"
        else:
            model_name = "gemini-2.0-flash"  # По умолчанию
        
        model = self.client.GenerativeModel(model_name)
        
        # Объединяем system prompt и user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        try:
            # Google Gemini doesn't support json_mode, so we handle it differently
            if json_mode:
                # Add JSON instruction to prompt for Gemini
                full_prompt += "\n\nВажно: Ответь ТОЛЬКО в формате JSON, без дополнительного текста."
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': temperature,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 8192,
                }
            )
            
            if response.text:
                return response.text
            else:
                # Если нет текста, попробуем получить части
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content:
                        return candidate.content.parts[0].text if candidate.content.parts else ""
                
                return "No response generated"
                
        except Exception as e:
            logger.error(f"Google Gemini error: {e}")
            # Попробуем альтернативную модель
            try:
                model = self.client.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(full_prompt)
                return response.text if response.text else "No response generated"
            except Exception as e2:
                logger.error(f"Google Gemini fallback error: {e2}")
                raise Exception(f"Google Gemini API error: {e}")
    
    def _generate_ollama(self, prompt: str, system_prompt: Optional[str], 
                        temperature: float, json_mode: bool) -> str:
        """Генерация через Ollama (БЕСПЛАТНО, локально!)"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                'temperature': temperature,
            }
        )
        
        return response['message']['content']
    
    def _generate_groq(self, prompt: str, system_prompt: Optional[str], 
                      temperature: float, json_mode: bool) -> str:
        """Генерация через Groq (БЕСПЛАТНО, очень быстро!)"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict:
        """
        Генерирует JSON ответ
        
        Args:
            prompt: Промпт
            system_prompt: Системный промпт
            
        Returns:
            Словарь с данными
        """
        # Добавляем инструкцию для JSON в промпт
        json_instruction = "\n\nВерни результат ТОЛЬКО в формате JSON, без дополнительного текста."
        full_prompt = prompt + json_instruction
        
        try:
            response = self.generate(full_prompt, system_prompt, temperature=0.7, json_mode=True)
        except Exception as e:
            logger.error(f"JSON mode failed, trying without: {e}")
            # Fallback: try without json_mode
            response = self.generate(full_prompt, system_prompt, temperature=0.7, json_mode=False)
        
        # Парсим JSON
        try:
            # Пытаемся найти JSON в ответе
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            
            return json.loads(response.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            logger.error(f"Ответ: {response}")
            # Пытаемся извлечь JSON более агрессивно
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            raise ValueError(f"Не удалось распарсить JSON из ответа: {response[:200]}")
    
    def analyze_with_fab(self, website_data: Dict) -> Dict:
        """
        Анализирует данные сайта с использованием FAB методологии
        
        Args:
            website_data: Данные о сайте
            
        Returns:
            FAB анализ
        """
        from fab import FABMethodology
        
        system_prompt = FABMethodology.get_fab_prompt()
        user_prompt = FABMethodology.create_fab_analysis_prompt(website_data)
        
        return self.generate_json(user_prompt, system_prompt)
    
    def generate_keywords(self, fab_analysis: Dict, additional_context: Optional[str] = None) -> Dict:
        """
        Генерирует ключевые слова на основе FAB анализа
        
        Args:
            fab_analysis: FAB анализ
            additional_context: Дополнительный контекст
            
        Returns:
            Словарь с ключевыми словами
        """
        from fab import FABMethodology
        
        prompt = FABMethodology.create_keyword_generation_prompt(fab_analysis)
        
        if additional_context:
            prompt += f"\n\n**Дополнительный контекст:**\n{additional_context}"
        
        system_prompt = """
You are an expert in SEO and Google Ads contextual advertising.
Your task is to generate high-quality keywords for advertising campaigns.
Consider commercial intent, relevance, and search volume.

IMPORTANT: Generate keywords in the same language as the website content. If the website is in Ukrainian, generate Ukrainian keywords. If in English, generate English keywords. If in Russian, generate Russian keywords.

Return result in JSON format:
{
    "keywords": [
        {
            "keyword": "keyword",
            "match_type": "broad|phrase|exact|modified_broad",
            "search_volume": "high|medium|low",
            "commercial_intent": "high|medium|low",
            "category": "informational|transactional|navigational"
        }
    ]
}
"""
        
        try:
            return self.generate_json(prompt, system_prompt)
        except Exception as e:
            logger.error(f"Keyword generation failed: {e}")
            # Fallback: generate simple keywords
            return self._generate_fallback_keywords(fab_analysis)
    
    def _generate_fallback_keywords(self, fab_analysis: Dict) -> Dict:
        """Fallback keyword generation if AI fails"""
        product_name = fab_analysis.get('product_name', '')
        target_audience = fab_analysis.get('target_audience', '')
        
        # Extract basic keywords from product name and audience
        keywords = []
        
        if product_name:
            # Split product name into words
            words = product_name.lower().split()
            for word in words:
                if len(word) > 3:  # Only meaningful words
                    keywords.append({
                        "keyword": word,
                        "match_type": "broad",
                        "search_volume": "medium",
                        "commercial_intent": "high",
                        "category": "transactional"
                    })
        
        # Add some generic keywords based on context
        generic_keywords = [
            {"keyword": "buy", "match_type": "phrase", "search_volume": "high", "commercial_intent": "high", "category": "transactional"},
            {"keyword": "price", "match_type": "phrase", "search_volume": "high", "commercial_intent": "high", "category": "transactional"},
            {"keyword": "order", "match_type": "phrase", "search_volume": "medium", "commercial_intent": "high", "category": "transactional"},
            {"keyword": "services", "match_type": "broad", "search_volume": "high", "commercial_intent": "medium", "category": "informational"},
        ]
        
        keywords.extend(generic_keywords)
        
        return {"keywords": keywords}
    
    def generate_google_ads(self, fab_analysis: Dict, keywords: List[str], 
                           additional_requirements: Optional[str] = None) -> Dict:
        """
        Генерирует объявления Google Ads
        
        Args:
            fab_analysis: FAB анализ
            keywords: Список ключевых слов
            additional_requirements: Дополнительные требования
            
        Returns:
            Словарь с объявлениями
        """
        prompt = f"""
Create Google Ads based on FAB analysis and keywords.

**Product data:**
Name: {fab_analysis.get('product_name', '')}
Target audience: {fab_analysis.get('target_audience', '')}
Unique value proposition: {fab_analysis.get('unique_value_proposition', '')}

**FAB statements:**
{json.dumps(fab_analysis.get('fab_statements', []), ensure_ascii=False, indent=2)}

**Keywords:**
{', '.join(keywords[:10])}

**Google Ads technical requirements:**
- Headlines: max {settings.headline_max_length} characters each
- Descriptions: max {settings.description_max_length} characters each
- Paths: max {settings.path_max_length} characters each

**Content requirements:**
1. Use BAB method (Benefit-Advantage-Feature) - start with benefit
2. Include emotional trigger
3. Add call-to-action (CTA)
4. Use unique value proposition
5. Consider target audience

Create at least 5-7 ad variations with different approaches:
- Emotional
- Rational
- With offer/promotion
- With social proof
- Problem-solving

For each ad create:
- 3-5 headline variations
- 2-3 description variations
- 2 path variations
- List of suitable keywords from the provided list

{additional_requirements or ''}

IMPORTANT: Generate ads in the same language as the website content. If the website is in Ukrainian, generate Ukrainian ads. If in English, generate English ads. If in Russian, generate Russian ads.

Return result in JSON format:
{{
    "ads": [
        {{
            "type": "approach_type",
            "headlines": ["headline1", "headline2", ...],
            "descriptions": ["description1", "description2"],
            "paths": ["path1", "path2"],
            "keywords": ["keyword1", ...],
            "notes": "approach notes"
        }}
    ]
}}
"""
        
        system_prompt = """
You are an expert in creating Google Ads with over 10 years of experience.
You know all technical limitations and best practices.
Your ads always convert and attract target audience.
You are a copywriting master and know buyer psychology.

IMPORTANT: Generate ads in the same language as the website content. If the website is in Ukrainian, generate Ukrainian ads. If in English, generate English ads. If in Russian, generate Russian ads.

Return result in JSON format.
"""
        
        return self.generate_json(prompt, system_prompt)

