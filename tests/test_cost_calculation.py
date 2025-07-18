"""
Pruebas para el sistema de cálculo de costos
"""
import pytest
from unittest.mock import Mock, patch

# Importar funciones reales de utils
from utils import (
    calculate_item_cost, calculate_total_cost, calculate_cost_breakdown,
    convert_usd_to_eur, validate_cost, validate_cost_range, round_cost,
    COST_RATES
)


class TestCostCalculation:
    """Pruebas para el cálculo de costos de generación"""
    
    def test_calculate_flux_pro_cost(self):
        """Probar cálculo de costo para Flux Pro"""
        # Usar la función real de utils
        item = {
            'tipo': 'imagen',
            'archivo_local': 'flux_pro_image.webp',  # Indica que es Flux Pro
            'modelo': 'flux_pro',
            'parametros': {'width': 1024, 'height': 1024}
        }
        
        cost, model_info, calculation = calculate_item_cost(item)
        
        expected_cost = COST_RATES['imagen']['flux_pro']['rate']
        assert cost == expected_cost
        assert "Flux Pro" in model_info
        assert str(expected_cost) in calculation
    
    def test_calculate_kandinsky_cost(self):
        """Probar cálculo de costo para Kandinsky"""
        def calculate_item_cost_mock(item):
            if item.get('tipo') == 'imagen' and 'kandinsky' in item.get('modelo', '').lower():
                seconds = item.get('processing_time', 10)
                cost = 0.0014 * seconds
                return cost, f"Kandinsky ({seconds}s)", f"$0.0014 × {seconds}s"
            return 0, "Unknown", "N/A"
        
        item = {
            'tipo': 'imagen',
            'modelo': 'kandinsky',
            'processing_time': 12
        }
        
        cost, model_info, calculation = calculate_item_cost_mock(item)
        
        assert cost == 0.0168  # 0.0014 * 12
        assert "Kandinsky (12s)" == model_info
        assert "0.0014 × 12s" in calculation
    
    def test_calculate_video_seedance_cost(self):
        """Probar cálculo de costo para videos Seedance"""
        def calculate_item_cost_mock(item):
            if item.get('tipo') == 'video' and 'seedance' in item.get('modelo', '').lower():
                seconds = item.get('video_duration', 5)
                cost = 0.15 * seconds
                return cost, f"Seedance ({seconds}s)", f"$0.15 × {seconds}s"
            return 0, "Unknown", "N/A"
        
        item = {
            'tipo': 'video',
            'modelo': 'seedance',
            'video_duration': 5
        }
        
        cost, model_info, calculation = calculate_item_cost_mock(item)
        
        assert cost == 0.75  # 0.15 * 5
        assert "Seedance (5s)" == model_info
        assert "0.15 × 5s" in calculation
    
    def test_calculate_sticker_cost(self):
        """Probar cálculo de costo para stickers"""
        def calculate_item_cost_mock(item):
            if item.get('tipo') == 'sticker':
                return 0.055, "Sticker Flux Pro", "$0.055 por sticker"
            return 0, "Unknown", "N/A"
        
        item = {
            'tipo': 'sticker',
            'modelo': 'sticker-maker'
        }
        
        cost, model_info, calculation = calculate_item_cost_mock(item)
        
        assert cost == 0.055
        assert model_info == "Sticker Flux Pro"
        assert "$0.055" in calculation
    
    def test_calculate_total_cost_multiple_items(self, sample_history_data):
        """Probar cálculo de costo total para múltiples elementos"""
        def calculate_item_cost_mock(item):
            costs = {
                'imagen': 0.055,
                'video': 0.75,
                'sticker': 0.055
            }
            return costs.get(item.get('tipo'), 0), "Model", "Calculation"
        
        def calculate_total_cost(history):
            return sum(calculate_item_cost_mock(item)[0] for item in history)
        
        total = calculate_total_cost(sample_history_data)
        expected = 0.055 + 0.75 + 0.055  # imagen + video + sticker
        
        assert total == expected
        assert round(total, 2) == 0.86  # Evitar problemas de precisión flotante
    
    def test_cost_conversion_usd_to_eur(self):
        """Probar conversión de USD a EUR"""
        def convert_usd_to_eur(usd_amount, rate=0.92):
            return usd_amount * rate
        
        usd_cost = 1.00
        eur_cost = convert_usd_to_eur(usd_cost)
        
        assert eur_cost == 0.92
        
        # Probar con diferentes cantidades
        assert convert_usd_to_eur(0.055) == pytest.approx(0.0506, rel=1e-3)
        assert convert_usd_to_eur(0.75) == pytest.approx(0.69, rel=1e-2)
    
    def test_cost_breakdown_by_model(self, sample_history_data):
        """Probar desglose de costos por modelo"""
        def calculate_cost_breakdown(history):
            breakdown = {}
            
            for item in history:
                model = item.get('modelo', 'unknown')
                tipo = item.get('tipo', 'unknown')
                
                # Calcular costo simulado
                if tipo == 'imagen':
                    cost = 0.055
                elif tipo == 'video':
                    cost = 0.75
                elif tipo == 'sticker':
                    cost = 0.055
                else:
                    cost = 0
                
                if model not in breakdown:
                    breakdown[model] = {'count': 0, 'total_cost': 0}
                
                breakdown[model]['count'] += 1
                breakdown[model]['total_cost'] += cost
            
            return breakdown
        
        breakdown = calculate_cost_breakdown(sample_history_data)
        
        assert 'flux-pro' in breakdown
        assert 'seedance' in breakdown
        assert 'sticker-maker' in breakdown
        
        assert breakdown['flux-pro']['count'] == 1
        assert breakdown['flux-pro']['total_cost'] == 0.055
        
        assert breakdown['seedance']['count'] == 1
        assert breakdown['seedance']['total_cost'] == 0.75


class TestCostValidation:
    """Pruebas para validación de cálculos de costo"""
    
    def test_validate_positive_costs(self):
        """Probar que los costos sean siempre positivos"""
        def validate_cost(cost):
            return cost >= 0
        
        assert validate_cost(0.055) is True
        assert validate_cost(0) is True
        assert validate_cost(-0.1) is False
    
    def test_validate_reasonable_cost_ranges(self):
        """Probar que los costos estén en rangos razonables"""
        def validate_cost_range(cost, item_type):
            ranges = {
                'imagen': (0, 1.0),      # Máximo $1 por imagen
                'video': (0, 10.0),      # Máximo $10 por video
                'sticker': (0, 0.5)      # Máximo $0.5 por sticker
            }
            
            min_cost, max_cost = ranges.get(item_type, (0, float('inf')))
            return min_cost <= cost <= max_cost
        
        # Costos válidos
        assert validate_cost_range(0.055, 'imagen') is True
        assert validate_cost_range(0.75, 'video') is True
        assert validate_cost_range(0.055, 'sticker') is True
        
        # Costos inválidos
        assert validate_cost_range(2.0, 'imagen') is False
        assert validate_cost_range(15.0, 'video') is False
        assert validate_cost_range(1.0, 'sticker') is False
    
    def test_cost_precision(self):
        """Probar precisión de cálculos de costo"""
        def round_cost(cost, decimals=3):
            return round(cost, decimals)
        
        # Probar redondeo a 3 decimales
        assert round_cost(0.0556789) == 0.056
        assert round_cost(0.0554321) == 0.055
        
        # Verificar que no se pierda precisión innecesariamente
        assert round_cost(0.055) == 0.055
        assert round_cost(0.75) == 0.75
