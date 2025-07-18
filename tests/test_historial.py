"""
Pruebas para el sistema de historial
"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, Mock
import tempfile
import os

# Importar funciones reales de utils
from utils import (
    load_history, save_to_history, filter_history_by_type,
    search_history_by_prompt, backup_history_file, validate_history_structure,
    HISTORY_DIR, HISTORY_FILE
)


class TestHistorialSystem:
    """Pruebas para el sistema de gestión de historial"""
    
    def test_load_history_file_exists(self, mock_history_file, sample_history_data):
        """Probar carga de historial cuando el archivo existe"""
        # Usar la función real de utils con mock del archivo
        with patch('utils.HISTORY_FILE', mock_history_file):
            history = load_history()
        
        assert len(history) == 3
        assert history[0]['tipo'] == 'imagen'
        assert history[1]['tipo'] == 'video'
        assert history[2]['tipo'] == 'sticker'
        assert 'fecha' in history[0]
        assert 'prompt' in history[0]
        assert 'url' in history[0]
    
    def test_load_history_file_not_exists(self, temp_dir):
        """Probar carga de historial cuando el archivo no existe"""
        # Crear un archivo de historial temporal que no existe
        non_existent_file = temp_dir / "non_existent_history.json"
        
        # Usar la función real con mock del archivo
        with patch('utils.HISTORY_FILE', non_existent_file):
            history = load_history()
        
        assert history == []
    
    def test_save_history_item(self, temp_dir):
        """Probar guardado de elemento en historial"""
        history_file = temp_dir / "test_history.json"
        
        test_item = {
            "tipo": "imagen",
            "fecha": "2025-01-18T15:00:00",
            "prompt": "Test image",
            "url": "https://test.com/image.webp",
            "archivo_local": "test_image.webp"
        }
        
        # Usar la función real con mock del archivo
        with patch('utils.HISTORY_FILE', history_file):
            result = save_to_history(test_item)
        
        assert result is True
        
        # Verificar que se guardó correctamente
        with open(history_file, 'r', encoding='utf-8') as f:
            saved_history = json.load(f)
        
        assert len(saved_history) == 1
        assert saved_history[0]['tipo'] == 'imagen'
        assert saved_history[0]['prompt'] == 'Test image'
    
    def test_history_item_structure(self, sample_history_data):
        """Probar que los elementos del historial tienen la estructura correcta"""
        required_fields = ['tipo', 'fecha', 'prompt', 'url', 'archivo_local']
        
        for item in sample_history_data:
            for field in required_fields:
                assert field in item, f"Campo requerido '{field}' faltante en item"
            
            # Verificar tipos de datos
            assert isinstance(item['tipo'], str)
            assert isinstance(item['fecha'], str)
            assert isinstance(item['prompt'], str)
            assert isinstance(item['url'], str)
            assert isinstance(item.get('parametros', {}), dict)
    
    def test_filter_history_by_type(self, sample_history_data):
        """Probar filtrado de historial por tipo"""
        # Usar la función real de utils
        
        # Filtrar por imágenes
        imagenes = filter_history_by_type(sample_history_data, 'imagen')
        assert len(imagenes) == 1
        assert imagenes[0]['tipo'] == 'imagen'
        
        # Filtrar por videos
        videos = filter_history_by_type(sample_history_data, 'video')
        assert len(videos) == 1
        assert videos[0]['tipo'] == 'video'
        
        # Filtrar por stickers
        stickers = filter_history_by_type(sample_history_data, 'sticker')
        assert len(stickers) == 1
        assert stickers[0]['tipo'] == 'sticker'
        
        # Filtrar por tipo inexistente
        inexistente = filter_history_by_type(sample_history_data, 'inexistente')
        assert len(inexistente) == 0
    
    def test_history_search_functionality(self, sample_history_data):
        """Probar funcionalidad de búsqueda en historial"""
        # Usar la función real de utils
        
        # Buscar término existente
        results = search_history_by_prompt(sample_history_data, 'prueba')
        assert len(results) == 3  # Todos tienen "prueba" en el prompt
        
        # Buscar término específico
        results = search_history_by_prompt(sample_history_data, 'imagen')
        assert len(results) == 1
        assert results[0]['tipo'] == 'imagen'
        
        # Buscar término inexistente
        results = search_history_by_prompt(sample_history_data, 'inexistente')
        assert len(results) == 0


class TestHistorialFileOperations:
    """Pruebas para operaciones de archivo del historial"""
    
    def test_create_history_directory(self, temp_dir):
        """Probar creación de directorio de historial"""
        history_dir = temp_dir / "historial"
        
        def ensure_history_dir():
            history_dir.mkdir(exist_ok=True)
            return history_dir.exists()
        
        result = ensure_history_dir()
        assert result is True
        assert history_dir.is_dir()
    
    def test_backup_history_file(self, mock_history_file):
        """Probar respaldo de archivo de historial"""
        def backup_history(source_file):
            backup_file = source_file.parent / f"{source_file.stem}_backup.json"
            
            # Leer archivo original
            with open(source_file, 'r', encoding='utf-8') as f:
                data = f.read()
            
            # Escribir backup
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(data)
            
            return backup_file.exists()
        
        result = backup_history(mock_history_file)
        assert result is True
        
        backup_file = mock_history_file.parent / "history_backup.json"
        assert backup_file.exists()
    
    def test_validate_json_structure(self, temp_dir):
        """Probar validación de estructura JSON"""
        # Usar la función real de utils
        
        # Crear archivo JSON válido
        valid_data = [{"tipo": "test", "fecha": "2025-01-18", "prompt": "test"}]
        assert validate_history_structure(valid_data) is True
        
        # Probar estructura inválida - no es lista
        invalid_data = {"tipo": "test", "fecha": "2025-01-18", "prompt": "test"}
        assert validate_history_structure(invalid_data) is False
        
        # Probar estructura inválida - falta campo requerido
        invalid_data = [{"tipo": "test", "fecha": "2025-01-18"}]  # falta 'prompt'
        assert validate_history_structure(invalid_data) is False
