"""
Configuración global para pytest - Fixtures y configuraciones compartidas
"""
import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
import shutil


@pytest.fixture
def temp_dir():
    """Crear directorio temporal para pruebas"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_config():
    """Mock de configuración con token falso"""
    with patch('config.REPLICATE_API_TOKEN', 'test_token_123'):
        yield


@pytest.fixture
def sample_history_data():
    """Datos de ejemplo para historial"""
    return [
        {
            "tipo": "imagen",
            "fecha": "2025-01-18T10:30:00",
            "prompt": "Imagen de prueba",
            "plantilla": "Personalizado",
            "url": "https://replicate.delivery/test123.webp",
            "archivo_local": "imagen_20250118_103000.webp",
            "parametros": {"width": 1024, "height": 1024, "steps": 25},
            "id_prediccion": "test_prediction_123",
            "modelo": "flux-pro"
        },
        {
            "tipo": "video",
            "fecha": "2025-01-18T11:00:00",
            "prompt": "Video de prueba",
            "plantilla": "Cinematográfico",
            "url": "https://replicate.delivery/test456.mp4",
            "archivo_local": "seedance_20250118_110000.mp4",
            "parametros": {"duration": 5, "fps": 24, "resolution": "1080p"},
            "modelo": "seedance",
            "video_duration": 5
        },
        {
            "tipo": "sticker",
            "fecha": "2025-01-18T12:00:00",
            "prompt": "Sticker de prueba",
            "plantilla": "Kawaii",
            "url": "https://replicate.delivery/test789.png",
            "archivo_local": "sticker_20250118_120000.png",
            "parametros": {"style": "cartoon"},
            "modelo": "sticker-maker"
        }
    ]


@pytest.fixture
def mock_history_file(temp_dir, sample_history_data):
    """Crear archivo de historial temporal con datos de prueba"""
    history_file = temp_dir / "history.json"
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(sample_history_data, f, indent=2, ensure_ascii=False)
    return history_file


@pytest.fixture
def mock_replicate_client():
    """Mock del cliente de Replicate"""
    with patch('replicate.Client') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock de respuesta exitosa para run
        mock_instance.run.return_value = [
            "https://replicate.delivery/test_output.webp"
        ]
        
        # Mock de respuesta para get (estado de predicción)
        mock_prediction = Mock()
        mock_prediction.status = "succeeded"
        mock_prediction.output = ["https://replicate.delivery/test_output.webp"]
        mock_instance.predictions.get.return_value = mock_prediction
        
        yield mock_instance


@pytest.fixture
def mock_requests():
    """Mock de requests para descargas"""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/webp'}
        mock_response.content = b'fake_image_data'
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_streamlit():
    """Mock de Streamlit para pruebas de UI"""
    with patch('streamlit.session_state') as mock_session:
        mock_session.current_page = 'generator'
        mock_session.selected_item_index = None
        yield mock_session


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset del entorno antes de cada prueba"""
    # Limpiar variables de entorno específicas de testing
    test_vars = [var for var in os.environ.keys() if var.startswith('TEST_')]
    for var in test_vars:
        del os.environ[var]
    
    yield
    
    # Cleanup después de cada prueba
    for var in test_vars:
        if var in os.environ:
            del os.environ[var]
