"""
Análisis de Sentimiento en Redes Sociales
Monitorea menciones de volcanes y eventos sísmicos en redes sociales
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from collections import defaultdict


logger = logging.getLogger(__name__)


@dataclass
class SocialMediaPost:
    """Representa un post en redes sociales"""
    post_id: str
    platform: str  # twitter, facebook, instagram, reddit
    username: str
    content: str
    timestamp: datetime
    volcano_mentions: List[str]
    sentiment_score: float  # -1 a 1
    sentiment_label: str  # negative, neutral, positive
    engagement: int  # likes, retweets, etc.
    location: Optional[str] = None
    language: str = "es"


class SocialSentimentAnalyzer:
    """Analiza sentimiento en redes sociales sobre volcanes"""
    
    # Palabras clave por sentimiento
    NEGATIVE_KEYWORDS = {
        "temblor", "terremoto", "sismo", "epicentro",
        "peligro", "alerta", "evacuar", "peligroso",
        "miedo", "pánico", "desastre", "tragedia",
        "víctimas", "daños", "destrucción", "calamidad"
    }
    
    POSITIVE_KEYWORDS = {
        "monitoreo", "investigación", "ciencia",
        "prevención", "seguro", "preparado",
        "control", "sistema", "eficiente", "éxito"
    }
    
    VOLCANO_KEYWORDS = {
        "deception": ["deception island", "deception", "volcán deception"],
        "cotopaxi": ["cotopaxi", "volcán cotopaxi"],
        "villarrica": ["villarrica", "volcán villarrica"],
        "sakurajima": ["sakurajima", "volcán sakurajima"],
        "etna": ["etna", "monte etna"],
        "vesuvio": ["vesuvio", "monte vesuvio"],
    }
    
    def __init__(self):
        self.posts: List[SocialMediaPost] = []
        self.sentiment_trends: Dict[str, List[Tuple]] = defaultdict(list)
    
    def analyze_post(
        self,
        post_id: str,
        platform: str,
        username: str,
        content: str,
        timestamp: datetime,
        engagement: int = 0,
        location: Optional[str] = None
    ) -> SocialMediaPost:
        """
        Analiza sentimiento de un post
        
        Args:
            post_id: ID único del post
            platform: Plataforma (twitter, facebook, instagram, reddit)
            username: Usuario que publicó
            content: Contenido del post
            timestamp: Fecha del post
            engagement: Métrica de engagement (likes, retweets, etc.)
            location: Ubicación del usuario
        
        Returns:
            SocialMediaPost con análisis
        """
        content_lower = content.lower()
        
        # Detectar menciones de volcanes
        volcano_mentions = []
        for volcano_id, keywords in self.VOLCANO_KEYWORDS.items():
            if any(kw in content_lower for kw in keywords):
                volcano_mentions.append(volcano_id)
        
        # Calcular sentimiento
        sentiment_score = self._calculate_sentiment(content_lower)
        
        # Clasificar sentimiento
        if sentiment_score < -0.1:
            sentiment_label = "negative"
        elif sentiment_score > 0.1:
            sentiment_label = "positive"
        else:
            sentiment_label = "neutral"
        
        post = SocialMediaPost(
            post_id=post_id,
            platform=platform,
            username=username,
            content=content,
            timestamp=timestamp,
            volcano_mentions=volcano_mentions,
            sentiment_score=round(sentiment_score, 3),
            sentiment_label=sentiment_label,
            engagement=engagement,
            location=location
        )
        
        self.posts.append(post)
        
        # Registrar en tendencias
        for volcano_id in volcano_mentions:
            self.sentiment_trends[volcano_id].append(
                (timestamp, sentiment_score)
            )
        
        return post
    
    def _calculate_sentiment(self, text: str) -> float:
        """
        Calcula puntuación de sentimiento (-1 a 1)
        Usando análisis simple basado en palabras clave
        """
        negative_count = sum(1 for word in self.NEGATIVE_KEYWORDS if word in text)
        positive_count = sum(1 for word in self.POSITIVE_KEYWORDS if word in text)
        
        total = negative_count + positive_count
        
        if total == 0:
            return 0.0
        
        # Calcular ratio
        sentiment = (positive_count - negative_count) / total
        
        return max(-1.0, min(1.0, sentiment))
    
    def get_volcano_sentiment(
        self,
        volcano_id: str,
        days: int = 7
    ) -> Dict:
        """
        Obtiene análisis de sentimiento para un volcán
        
        Args:
            volcano_id: ID del volcán
            days: Número de días a analizar
        
        Returns:
            Diccionario con estadísticas de sentimiento
        """
        cutoff_time = datetime.now() - timedelta(days=days)
        
        posts = [
            p for p in self.posts
            if volcano_id in p.volcano_mentions and p.timestamp >= cutoff_time
        ]
        
        if not posts:
            return {
                "volcano_id": volcano_id,
                "posts_count": 0,
                "avg_sentiment": 0.0
            }
        
        sentiments = [p.sentiment_score for p in posts]
        sentiment_labels = [p.sentiment_label for p in posts]
        
        return {
            "volcano_id": volcano_id,
            "posts_count": len(posts),
            "avg_sentiment": round(sum(sentiments) / len(sentiments), 3),
            "positive_percent": round(
                sentiment_labels.count("positive") / len(posts) * 100, 1
            ),
            "neutral_percent": round(
                sentiment_labels.count("neutral") / len(posts) * 100, 1
            ),
            "negative_percent": round(
                sentiment_labels.count("negative") / len(posts) * 100, 1
            ),
            "top_platforms": self._get_top_platforms(posts),
            "trending": self._is_trending(volcano_id)
        }
    
    def _get_top_platforms(self, posts: List[SocialMediaPost]) -> Dict:
        """Obtiene plataformas más mencionadas"""
        platforms = defaultdict(int)
        for post in posts:
            platforms[post.platform] += 1
        return dict(platforms)
    
    def _is_trending(self, volcano_id: str, threshold: int = 5) -> bool:
        """Verifica si volcán está en tendencia (últimas 24h)"""
        cutoff = datetime.now() - timedelta(hours=24)
        recent_posts = [
            p for p in self.posts
            if volcano_id in p.volcano_mentions and p.timestamp >= cutoff
        ]
        return len(recent_posts) >= threshold
    
    def get_trending_volcanoes(self) -> List[Dict]:
        """Retorna volcanes en tendencia"""
        volcano_ids = set()
        for post in self.posts:
            volcano_ids.update(post.volcano_mentions)
        
        trending = []
        for v_id in volcano_ids:
            sentiment_data = self.get_volcano_sentiment(v_id, days=1)
            if sentiment_data["posts_count"] >= 3:
                trending.append({
                    "volcano_id": v_id,
                    "mentions": sentiment_data["posts_count"],
                    "sentiment": sentiment_data["avg_sentiment"],
                    "engagement_total": sum(
                        p.engagement for p in self.posts
                        if v_id in p.volcano_mentions
                    )
                })
        
        return sorted(trending, key=lambda x: x["mentions"], reverse=True)
    
    def get_alert_posts(self, volcano_id: str, days: int = 3) -> List[Dict]:
        """
        Retorna posts alarmistas sobre un volcán
        (sentimiento muy negativo)
        """
        cutoff = datetime.now() - timedelta(days=days)
        
        alert_posts = [
            p for p in self.posts
            if volcano_id in p.volcano_mentions and
            p.sentiment_score < -0.5 and
            p.timestamp >= cutoff
        ]
        
        return [
            {
                "content": p.content,
                "platform": p.platform,
                "username": p.username,
                "sentiment": p.sentiment_score,
                "engagement": p.engagement,
                "timestamp": p.timestamp.isoformat()
            }
            for p in sorted(alert_posts, key=lambda x: x.engagement, reverse=True)
        ]
    
    def get_social_sentiment_summary(self) -> Dict:
        """Retorna resumen general de sentimiento social"""
        if not self.posts:
            return {
                "total_posts": 0,
                "avg_sentiment": 0.0,
                "platforms": {}
            }
        
        sentiments = [p.sentiment_score for p in self.posts]
        platforms = defaultdict(int)
        for post in self.posts:
            platforms[post.platform] += 1
        
        return {
            "total_posts": len(self.posts),
            "avg_sentiment": round(sum(sentiments) / len(sentiments), 3),
            "positive_posts": sum(1 for s in sentiments if s > 0.1),
            "neutral_posts": sum(1 for s in sentiments if -0.1 <= s <= 0.1),
            "negative_posts": sum(1 for s in sentiments if s < -0.1),
            "platforms": dict(platforms),
            "trending_volcanoes": [v["volcano_id"] for v in self.get_trending_volcanoes()],
            "high_engagement_total": sum(p.engagement for p in self.posts)
        }


# Instancia global
sentiment_analyzer = SocialSentimentAnalyzer()
