"""
Pruebas para cálculos de costos de modelos de IA
"""
import pytest
from utils import calculate_item_cost, COST_RATES, get_model_from_filename

class TestCostCalculation:
    """Pruebas para el cálculo de costos de los diferentes modelos"""
    
    def test_calculate_flux_cost(self):
        """Probar cálculo de costo para Flux Pro"""
        # Flux Pro: $0.055 por imagen
        item = {
            'tipo': 'imagen',
            'modelo': 'flux_pro',
            'archivo_local': 'flux_image.png',
            'parametros': {'steps': 20}
        }
        cost, model_info, details = calculate_item_cost(item)
        assert cost == 0.055
        assert 'Flux Pro' in model_info
    
    def test_calculate_kandinsky_cost(self):
        """Probar cálculo de costo para Kandinsky 2.2"""
        # Kandinsky: $0.00925 por segundo
        item = {
            'tipo': 'imagen',
            'modelo': 'kandinsky',
            'archivo_local': 'kandinsky_image.png',
            'parametros': {'num_inference_steps': 30},
            'processing_time': 12
        }
        cost, model_info, details = calculate_item_cost(item)
        expected_cost = 0.00925 * 12  # $0.111
        assert cost == round(expected_cost, 3)
        assert 'Kandinsky' in model_info
    
    def test_calculate_ssd_cost(self):
        """Probar cálculo de costo para SSD-1B"""
        # SSD-1B: $0.00925 por segundo, pero estima tiempo basado en steps
        item = {
            'tipo': 'imagen',
            'modelo': 'ssd_1b',
            'archivo_local': 'ssd_image.png',
            'parametros': {'num_inference_steps': 10},
            'processing_time': 6
        }
        cost, model_info, details = calculate_item_cost(item)
        # Con steps=10, estima ~4 segundos (max(4, min(10, 10*0.2)) = 4)
        expected_cost = 0.00925 * 4  # $0.037
        assert cost == round(expected_cost, 3)
        assert 'SSD-1B' in model_info
    
    def test_calculate_seedance_cost(self):
        """Probar cálculo de costo para Seedance"""
        # Seedance: $0.125 por segundo
        item = {
            'tipo': 'video',
            'modelo': 'seedance',
            'archivo_local': 'seedance_video.mp4',
            'parametros': {'duration': 4},
            'video_duration': 4
        }
        cost, model_info, details = calculate_item_cost(item)
        expected_cost = 0.125 * 4  # $0.5
        assert cost == round(expected_cost, 3)
        assert 'Seedance' in model_info
    
    def test_calculate_pixverse_cost(self):
        """Probar cálculo de costo para Pixverse"""
        # Pixverse: $0.000625 por unit, estima units basado en duración/resolución
        item = {
            'tipo': 'video',
            'modelo': 'pixverse',
            'archivo_local': 'pixverse_video.mp4',
            'parametros': {'duration': '3s', 'resolution': '720p'}
        }
        cost, model_info, details = calculate_item_cost(item)
        # Con 3s y 720p: 3*6 = 18 units base, 18*0.000625 = 0.01125, redondeado a 0.011
        expected_cost = 0.011  # Valor real observado  
        assert cost == expected_cost
        assert 'Pixverse' in model_info
    
    def test_calculate_veo3_cost(self):
        """Probar cálculo de costo para VEO 3 Fast"""
        # VEO 3: $0.25 por segundo
        item = {
            'tipo': 'video',
            'modelo': 'veo3',
            'archivo_local': 'veo3_video.mp4',
            'parametros': {'duration': 3},
            'video_duration': 3
        }
        cost, model_info, details = calculate_item_cost(item)
        expected_cost = 0.25 * 3  # $0.75
        assert cost == round(expected_cost, 3)
        assert 'VEO 3' in model_info
    
    def test_calculate_unknown_model_cost(self):
        """Probar que modelos desconocidos usan Flux Pro por defecto"""
        item = {
            'tipo': 'imagen',
            'modelo': 'unknown_model',
            'archivo_local': 'unknown.png',
            'parametros': {}
        }
        cost, model_info, details = calculate_item_cost(item)
        # Por defecto usa Flux Pro
        assert cost == 0.055
        assert 'Flux Pro' in model_info
    
    def test_empty_item_cost(self):
        """Probar que item vacío usa valores por defecto (Flux Pro)"""
        item = {}
        cost, model_info, details = calculate_item_cost(item)
        # Por defecto: tipo='imagen', modelo='flux_pro'
        assert cost == 0.055
        assert 'Flux Pro' in model_info
    
    def test_cost_rates_structure(self):
        """Verificar que la estructura de COST_RATES es correcta"""
        assert 'imagen' in COST_RATES
        assert 'video' in COST_RATES
        
        # Verificar modelos de imagen
        imagen_models = COST_RATES['imagen']
        assert 'flux_pro' in imagen_models
        assert 'kandinsky' in imagen_models
        assert 'ssd_1b' in imagen_models
        
        # Verificar modelos de video
        video_models = COST_RATES['video']
        assert 'seedance' in video_models
        assert 'pixverse' in video_models
        assert 'veo3' in video_models
        
        # Verificar que cada modelo tiene rate y unit
        for category in COST_RATES.values():
            for model_data in category.values():
                assert 'rate' in model_data
                assert 'unit' in model_data
                assert isinstance(model_data['rate'], (int, float))
                assert isinstance(model_data['unit'], str)
        
        # Verificar valores específicos
        assert COST_RATES['imagen']['flux_pro']['rate'] == 0.055
        assert COST_RATES['imagen']['kandinsky']['rate'] == 0.00925
        assert COST_RATES['imagen']['ssd_1b']['rate'] == 0.00925
        assert COST_RATES['video']['seedance']['rate'] == 0.125
        assert COST_RATES['video']['pixverse']['rate'] == 0.000625
        assert COST_RATES['video']['veo3']['rate'] == 0.25
    
    def test_get_model_from_filename(self):
        """Probar extracción de modelo desde nombre de archivo"""
        assert get_model_from_filename('flux_image_123.png') == 'Flux Pro'
        assert get_model_from_filename('kandinsky_art.jpg') == 'Kandinsky'
        assert get_model_from_filename('ssd_fast_gen.png') == 'SSD-1B'
        assert get_model_from_filename('seedance_video.mp4') == 'Seedance'
        assert get_model_from_filename('pixverse_anime.mp4') == 'Pixverse'
        assert get_model_from_filename('veo3_cinema.mp4') == 'VEO 3 Fast'
        assert get_model_from_filename('unknown_model.png') == 'Desconocido'
        
        # Verificar case-insensitive
        assert get_model_from_filename('FLUX_IMAGE.PNG') == 'Flux Pro'
        assert get_model_from_filename('VEO3_VIDEO.MP4') == 'VEO 3 Fast'
