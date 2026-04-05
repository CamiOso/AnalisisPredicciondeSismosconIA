"""
Sistema de Autenticación OAuth 2.0
Permite login seguro con Google, GitHub, etc.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
import hashlib
import secrets
from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)


@dataclass
class User:
    """Modelo de usuario"""
    user_id: str
    email: str
    name: str
    provider: str  # google, github, local
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    roles: list = None
    
    def __post_init__(self):
        if self.roles is None:
            self.roles = ["user"]


class AuthenticationManager:
    """Gestor de autenticación OAuth 2.0"""
    
    def __init__(self, secret_key: str = "dev-secret-key-change-in-production"):
        self.secret_key = secret_key
        self.users: Dict[str, User] = {}
        self.tokens: Dict[str, Dict] = {}
        self.access_token_ttl = 3600  # 1 hora
        self.refresh_token_ttl = 604800  # 7 días
    
    def generate_tokens(
        self,
        user_id: str,
        email: str
    ) -> Dict[str, str]:
        """Genera tokens de acceso y refresh"""
        now = datetime.utcnow()
        
        # Token de acceso (JWT)
        access_payload = {
            "user_id": user_id,
            "email": email,
            "iat": now,
            "exp": now + timedelta(seconds=self.access_token_ttl),
            "type": "access"
        }
        
        access_token = jwt.encode(
            access_payload,
            self.secret_key,
            algorithm="HS256"
        )
        
        # Token de refresco
        refresh_token = secrets.token_urlsafe(32)
        self.tokens[refresh_token] = {
            "user_id": user_id,
            "email": email,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(seconds=self.refresh_token_ttl)).isoformat()
        }
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": self.access_token_ttl
        }
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verifica y decodifica un token JWT"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Token inválido")
            return None
    
    def register_user(
        self,
        email: str,
        name: str,
        provider: str = "local",
        password: Optional[str] = None
    ) -> Optional[User]:
        """Registra un nuevo usuario"""
        user_id = hashlib.sha256(email.encode()).hexdigest()[:16]
        
        if user_id in self.users:
            logger.warning(f"Usuario ya existe: {email}")
            return None
        
        user = User(
            user_id=user_id,
            email=email,
            name=name,
            provider=provider,
            created_at=datetime.now()
        )
        
        self.users[user_id] = user
        logger.info(f"Usuario registrado: {email}")
        return user
    
    def authenticate_oauth(
        self,
        email: str,
        name: str,
        provider: str,
        profile_data: Optional[Dict] = None
    ) -> Dict:
        """
        Autentica usuario con OAuth
        Args:
            email: Email del usuario
            name: Nombre del usuario
            provider: Proveedor (google, github, etc.)
            profile_data: Datos adicionales del perfil
        Returns:
            Diccionario con tokens
        """
        user_id = hashlib.sha256(email.encode()).hexdigest()[:16]
        
        # Si no existe, crear usuario
        if user_id not in self.users:
            self.register_user(email, name, provider)
        else:
            # Actualizar último login
            self.users[user_id].last_login = datetime.now()
        
        tokens = self.generate_tokens(user_id, email)
        logger.info(f"Login exitoso: {email} ({provider})")
        
        return tokens
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict]:
        """Genera nuevo access token utilizando refresh token"""
        if refresh_token not in self.tokens:
            logger.warning("Refresh token inválido")
            return None
        
        token_data = self.tokens[refresh_token]
        
        # Verificar expiración
        expires_at = datetime.fromisoformat(token_data["expires_at"])
        if datetime.utcnow() > expires_at:
            del self.tokens[refresh_token]
            logger.warning("Refresh token expirado")
            return None
        
        return self.generate_tokens(
            token_data["user_id"],
            token_data["email"]
        )
    
    def logout(self, refresh_token: str) -> bool:
        """Cierra sesión invalidando tokens"""
        if refresh_token in self.tokens:
            del self.tokens[refresh_token]
            return True
        return False
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Obtiene información del usuario"""
        return self.users.get(user_id)
    
    def add_user_role(self, user_id: str, role: str) -> bool:
        """Agrega rol a usuario"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        if role not in user.roles:
            user.roles.append(role)
            return True
        return False


class GoogleOAuthConfig:
    """Configuración para OAuth con Google"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = "http://localhost:8000/auth/callback/google"
        self.auth_uri = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_uri = "https://oauth2.googleapis.com/token"
        self.userinfo_uri = "https://www.googleapis.com/oauth2/v1/userinfo"
    
    def get_authorization_url(self, state: str) -> str:
        """Genera URL de autorización"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state
        }
        return f"{self.auth_uri}?{'&'.join(f'{k}={v}' for k, v in params.items())}"


class GitHubOAuthConfig:
    """Configuración para OAuth con GitHub"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = "http://localhost:8000/auth/callback/github"
        self.auth_uri = "https://github.com/login/oauth/authorize"
        self.token_uri = "https://github.com/login/oauth/access_token"
        self.userinfo_uri = "https://api.github.com/user"
    
    def get_authorization_url(self, state: str) -> str:
        """Genera URL de autorización"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "user:email",
            "state": state
        }
        return f"{self.auth_uri}?{'&'.join(f'{k}={v}' for k, v in params.items())}"


# Instancia global
auth_manager = AuthenticationManager()
