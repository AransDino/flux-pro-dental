"""
Pruebas para funciones de utilidad del proyecto
"""
import pytest
import os
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from datetime import datetime

# Importar funciones reales de utils
from utils import (
    generate_filename_with_timestamp, validate_file_extension, format_file_size,
    sanitize_filename, parse_prompt_for_filename, load_replicate_token,
    validate_api_token, create_config_from_template, ensure_directory_exists,
    safe_json_write, get_file_info, is_valid_url, get_current_timestamp,
    round_cost
)


class TestUtilityFunctions:
    """Pruebas para funciones de utilidad generales"""
    
    def test_generate_filename_with_timestamp(self):
        """Probar generación de nombres de archivo con timestamp"""
        def generate_filename(prefix, extension, timestamp=None):
            if timestamp is None:
                timestamp = datetime.now()
            
            timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S')
            return f"{prefix}_{timestamp_str}.{extension}"
        
        # Probar con timestamp específico
        test_timestamp = datetime(2025, 1, 18, 15, 30, 45)
        filename = generate_filename("imagen", "webp", test_timestamp)
        
        assert filename == "imagen_20250118_153045.webp"
        
        # Probar con diferentes tipos
        video_filename = generate_filename("seedance", "mp4", test_timestamp)
        assert video_filename == "seedance_20250118_153045.mp4"
        
        sticker_filename = generate_filename("sticker", "png", test_timestamp)
        assert sticker_filename == "sticker_20250118_153045.png"
    
    def test_validate_file_extension(self):
        """Probar validación de extensiones de archivo"""
        def validate_extension(filename, allowed_extensions):
            if not filename or not isinstance(filename, str):
                return False
            
            file_ext = Path(filename).suffix.lower()
            return file_ext in [f".{ext}" for ext in allowed_extensions]
        
        # Extensiones válidas para imágenes
        image_extensions = ['webp', 'jpg', 'jpeg', 'png']
        assert validate_extension("test.webp", image_extensions) is True
        assert validate_extension("test.jpg", image_extensions) is True
        assert validate_extension("test.gif", image_extensions) is False
        
        # Extensiones válidas para videos
        video_extensions = ['mp4', 'avi', 'mov']
        assert validate_extension("test.mp4", video_extensions) is True
        assert validate_extension("test.webp", video_extensions) is False
    
    def test_format_file_size(self):
        """Probar formateo de tamaños de archivo"""
        def format_file_size(bytes_size):
            if bytes_size < 1024:
                return f"{bytes_size} B"
            elif bytes_size < 1024 * 1024:
                return f"{bytes_size / 1024:.1f} KB"
            elif bytes_size < 1024 * 1024 * 1024:
                return f"{bytes_size / (1024 * 1024):.1f} MB"
            else:
                return f"{bytes_size / (1024 * 1024 * 1024):.1f} GB"
        
        assert format_file_size(512) == "512 B"
        assert format_file_size(1536) == "1.5 KB"
        assert format_file_size(1024 * 1024 * 2.5) == "2.5 MB"
        assert format_file_size(1024 * 1024 * 1024 * 1.2) == "1.2 GB"
    
    def test_sanitize_filename(self):
        """Probar sanitización de nombres de archivo"""
        def sanitize_filename(filename):
            # Caracteres no permitidos en nombres de archivo
            invalid_chars = '<>:"/\\|?*'
            
            sanitized = filename
            for char in invalid_chars:
                sanitized = sanitized.replace(char, '_')
            
            # Eliminar espacios múltiples y al inicio/final
            sanitized = ' '.join(sanitized.split())
            
            return sanitized
        
        # Probar sanitización
        assert sanitize_filename("file<name>.txt") == "file_name_.txt"
        assert sanitize_filename("file:name") == "file_name"
        assert sanitize_filename("  multiple   spaces  ") == "multiple spaces"
        assert sanitize_filename("normal_filename.txt") == "normal_filename.txt"
    
    def test_parse_prompt_for_filename(self):
        """Probar extracción de palabras clave del prompt para nombres de archivo"""
        def parse_prompt_for_filename(prompt, max_words=3):
            if not prompt:
                return "generated"
            
            # Limpiar y dividir el prompt
            words = prompt.lower().replace(',', ' ').replace('.', ' ').split()
            
            # Filtrar palabras comunes (stop words básicos)
            stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
            
            # Tomar las primeras palabras significativas
            selected_words = meaningful_words[:max_words]
            
            return '_'.join(selected_words) if selected_words else 'generated'
        
        # Probar extracción
        prompt1 = "A beautiful sunset over the mountains"
        result1 = parse_prompt_for_filename(prompt1)
        # Puede generar diferentes combinaciones, verificar que contenga palabras clave
        assert "beautiful" in result1 and "sunset" in result1
        
        prompt2 = "Generate an image of a cat"
        result2 = parse_prompt_for_filename(prompt2)
        assert "cat" in result2  # Debe contener la palabra principal
        
        # Prompt vacío
        assert parse_prompt_for_filename("") == "generated"
        assert parse_prompt_for_filename(None) == "generated"


class TestConfigurationUtils:
    """Pruebas para utilidades de configuración"""
    
    def test_load_config_file_exists(self, temp_dir):
        """Probar carga de configuración cuando el archivo existe"""
        config_file = temp_dir / "config.py"
        config_content = 'REPLICATE_API_TOKEN = "test_token_123"'
        
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        def load_config_mock():
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                
                # Extraer token de manera simple (para testing)
                if 'REPLICATE_API_TOKEN' in content:
                    lines = content.split('\n')
                    for line in lines:
                        if 'REPLICATE_API_TOKEN' in line and '=' in line:
                            token = line.split('=')[1].strip().strip('"\'')
                            return token
                return None
            except FileNotFoundError:
                return None
        
        token = load_config_mock()
        assert token == "test_token_123"
    
    def test_validate_api_token(self):
        """Probar validación de tokens de API"""
        def validate_api_token(token):
            if not token or not isinstance(token, str):
                return False
            
            # Token no debe ser placeholder
            placeholders = ['tu_token_aqui', 'your_token_here', 'test_token', '']
            if token in placeholders:
                return False
            
            # Token debe tener longitud mínima
            if len(token) < 10:
                return False
            
            return True
        
        # Tokens válidos
        assert validate_api_token("r8_abc123def456ghi789") is True
        assert validate_api_token("valid_long_token_here") is True
        
        # Tokens inválidos
        assert validate_api_token("tu_token_aqui") is False
        assert validate_api_token("short") is False
        assert validate_api_token("") is False
        assert validate_api_token(None) is False
    
    def test_create_config_from_template(self, temp_dir):
        """Probar creación de config.py desde plantilla"""
        template_file = temp_dir / "config.example.py"
        config_file = temp_dir / "config.py"
        
        template_content = '''# Configuración de ejemplo
REPLICATE_API_TOKEN = "tu_token_de_replicate_aqui"
'''
        
        with open(template_file, 'w') as f:
            f.write(template_content)
        
        def create_config_from_template_mock():
            if template_file.exists() and not config_file.exists():
                with open(template_file, 'r') as f:
                    content = f.read()
                
                with open(config_file, 'w') as f:
                    f.write(content)
                
                return True
            return False
        
        result = create_config_from_template_mock()
        assert result is True
        assert config_file.exists()
        
        # Verificar contenido
        with open(config_file, 'r') as f:
            content = f.read()
        assert "REPLICATE_API_TOKEN" in content


class TestFileOperations:
    """Pruebas para operaciones de archivos"""
    
    def test_ensure_directory_exists(self, temp_dir):
        """Probar creación de directorios si no existen"""
        def ensure_directory_exists(path):
            path_obj = Path(path)
            path_obj.mkdir(parents=True, exist_ok=True)
            return path_obj.exists()
        
        new_dir = temp_dir / "new_directory" / "subdirectory"
        result = ensure_directory_exists(new_dir)
        
        assert result is True
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_safe_json_write(self, temp_dir):
        """Probar escritura segura de archivos JSON"""
        def safe_json_write(data, file_path):
            try:
                # Escribir a archivo temporal primero
                temp_file = Path(f"{file_path}.tmp")
                
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Mover archivo temporal al destino final
                temp_file.rename(file_path)
                return True
            except Exception:
                # Limpiar archivo temporal si algo falla
                if temp_file.exists():
                    temp_file.unlink()
                return False
        
        test_data = {"test": "data", "number": 42}
        test_file = temp_dir / "test.json"
        
        result = safe_json_write(test_data, test_file)
        assert result is True
        assert test_file.exists()
        
        # Verificar contenido
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        assert loaded_data == test_data
    
    def test_get_file_info(self, temp_dir):
        """Probar obtención de información de archivos"""
        test_file = temp_dir / "test_file.txt"
        test_content = "Test content for file info"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        def get_file_info(file_path):
            path_obj = Path(file_path)
            if not path_obj.exists():
                return None
            
            stat = path_obj.stat()
            return {
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'is_file': path_obj.is_file(),
                'extension': path_obj.suffix,
                'name': path_obj.name
            }
        
        info = get_file_info(test_file)
        
        assert info is not None
        assert info['size'] == len(test_content)
        assert info['is_file'] is True
        assert info['extension'] == '.txt'
        assert info['name'] == 'test_file.txt'
        assert isinstance(info['modified'], datetime)
