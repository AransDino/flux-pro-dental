"""
Módulo de utilidades centralizadas para AI Models Pro Generator
Contiene funciones compartidas para historial, cálculos de costo, configuración y más.
"""

import os
import json
import base64
import requests
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st


# ===============================
# FUNCIONES AUXILIARES
# ===============================

def get_model_from_filename(filename: str) -> str:
    """
    Extraer nombre del modelo desde el nombre del archivo

    Args:
        filename: Nombre del archivo

    Returns:
        str: Nombre del modelo
    """
    if 'flux' in filename.lower():
        return 'Flux Pro'
    elif 'kandinsky' in filename.lower():
        return 'Kandinsky'
    elif 'ssd' in filename.lower():
        return 'SSD-1B'
    elif 'seedance' in filename.lower():
        return 'Seedance'
    elif 'pixverse' in filename.lower():
        return 'Pixverse'
    elif 'veo3' in filename.lower():
        return 'VEO 3 Fast'
    else:
        return 'Desconocido'


# ===============================
# CONFIGURACIÓN Y CONSTANTES
# ===============================

# Configuración de directorios
HISTORY_DIR = Path("historial")
HISTORY_FILE = HISTORY_DIR / "history.json"
BACKUPS_DIR = Path("backups")

# Asegurar que los directorios existen
HISTORY_DIR.mkdir(exist_ok=True)
BACKUPS_DIR.mkdir(exist_ok=True)

# Tarifas de modelos actualizadas (USD por segundo/imagen)
COST_RATES = {
    'imagen': {
        'flux_pro': {'rate': 0.055, 'unit': 'per_image'},
        'kandinsky': {'rate': 0.00925, 'unit': 'per_second'},
        'ssd_1b': {'rate': 0.00925, 'unit': 'per_second'}
    },
    'video': {
        'seedance': {'rate': 0.125, 'unit': 'per_second'},
        'pixverse': {'rate': 0.000625, 'unit': 'per_unit'},  # $0.000625 por unit
        'veo3': {'rate': 0.25, 'unit': 'per_second'}
    }
}


# ===============================
# GESTIÓN DE CONFIGURACIÓN
# ===============================

def load_replicate_token() -> Optional[str]:
    """
    Cargar token de Replicate desde config.py o variables de entorno
    
    Returns:
        str: Token de Replicate o None si no se encuentra
    """
    try:
        # Intentar cargar desde config.py primero
        from config import REPLICATE_API_TOKEN
        if REPLICATE_API_TOKEN and REPLICATE_API_TOKEN != "tu_token_aqui":
            os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
            return REPLICATE_API_TOKEN
    except ImportError:
        pass
    
    # Intentar desde variables de entorno
    token = os.getenv("REPLICATE_API_TOKEN")
    if token:
        return token
    
    return None


def validate_api_token(token: str) -> bool:
    """
    Validar que el token de API es válido
    
    Args:
        token: Token a validar
        
    Returns:
        bool: True si el token es válido
    """
    if not token or token == "tu_token_aqui" or len(token) < 10:
        return False
    
    # Validar formato básico del token
    if not token.startswith('r8_'):
        return False
    
    return True


def create_config_from_template() -> bool:
    """
    Crear archivo de configuración desde template si no existe
    
    Returns:
        bool: True si se creó exitosamente
    """
    config_path = Path("config.py")
    
    if config_path.exists():
        return True
    
    try:
        template_content = '''"""
Configuración para AI Models Pro Generator
Reemplaza 'tu_token_aqui' con tu token real de Replicate
"""

# Token de API de Replicate
# Obtén tu token en: https://replicate.com/account/api-tokens
REPLICATE_API_TOKEN = "tu_token_aqui"

# Configuración opcional
DEBUG = False
MAX_HISTORY_ITEMS = 100
'''
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        return True
    except Exception:
        return False


# ===============================
# GESTIÓN DE HISTORIAL
# ===============================

def load_history() -> List[Dict[str, Any]]:
    """
    Cargar historial desde archivo JSON y normalizar datos
    
    Returns:
        List[Dict]: Lista de elementos del historial
    """
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
            
            # Normalizar tipos de video incorrectos
            for item in history:
                if item.get('tipo') in ['video_seedance', 'video_anime']:
                    item['tipo'] = 'video'
                    # Asegurar que el modelo está correctamente asignado
                    if 'video_seedance' in str(item.get('tipo', '')):
                        if not item.get('modelo'):
                            item['modelo'] = 'Seedance'
                    elif 'video_anime' in str(item.get('tipo', '')):
                        if not item.get('modelo'):
                            item['modelo'] = 'Pixverse'
            
            return history
    except Exception:
        return []


def save_to_history(item: Dict[str, Any]) -> bool:
    """
    Guardar item al historial
    
    Args:
        item: Elemento a guardar en el historial
        
    Returns:
        bool: True si se guardó exitosamente
    """
    try:
        # Limpiar cualquier objeto no serializable del item
        clean_item = {}
        for key, value in item.items():
            try:
                # Intentar serializar cada valor individualmente
                json.dumps(value)
                clean_item[key] = value
            except (TypeError, ValueError):
                # Si no se puede serializar, convertir a string
                clean_item[key] = str(value)
        
        history = load_history()
        history.insert(0, clean_item)  # Añadir al principio
        
        # Mantener solo los últimos 100 elementos
        history = history[:100]
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        if 'st' in globals():
            st.error(f"Error al guardar historial: {str(e)}")
        return False


def filter_history_by_type(history: List[Dict[str, Any]], tipo: str) -> List[Dict[str, Any]]:
    """
    Filtrar historial por tipo de contenido
    
    Args:
        history: Lista del historial
        tipo: Tipo a filtrar ('imagen', 'video')
        
    Returns:
        List[Dict]: Elementos filtrados
    """
    return [item for item in history if item.get('tipo') == tipo]


def search_history_by_prompt(history: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """
    Buscar en el historial por término en el prompt
    
    Args:
        history: Lista del historial
        search_term: Término a buscar
        
    Returns:
        List[Dict]: Elementos que coinciden con la búsqueda
    """
    return [
        item for item in history 
        if search_term.lower() in item.get('prompt', '').lower()
    ]


def backup_history_file() -> bool:
    """
    Crear respaldo del archivo de historial
    
    Returns:
        bool: True si se creó el backup exitosamente
    """
    if not HISTORY_FILE.exists():
        return False
    
    try:
        backup_file = HISTORY_DIR / f"history_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(HISTORY_FILE, 'r', encoding='utf-8') as source:
            with open(backup_file, 'w', encoding='utf-8') as backup:
                backup.write(source.read())
        
        return True
    except Exception:
        return False


def validate_history_structure(history: List[Dict[str, Any]]) -> bool:
    """
    Validar que la estructura del historial es correcta
    
    Args:
        history: Lista del historial a validar
        
    Returns:
        bool: True si la estructura es válida
    """
    if not isinstance(history, list):
        return False
    
    required_fields = ['tipo', 'fecha', 'prompt']
    
    for item in history:
        if not isinstance(item, dict):
            return False
        
        for field in required_fields:
            if field not in item:
                return False
    
    return True


# ===============================
# CÁLCULOS DE COSTO
# ===============================

def calculate_item_cost(item: Dict[str, Any]) -> Tuple[float, str, str]:
    """
    Calcular el costo de un item individual basado en sus características reales
    
    Args:
        item: Elemento del historial con información del contenido generado
        
    Returns:
        Tuple[float, str, str]: (costo, información_del_modelo, detalles_del_cálculo)
    """
    item_type = item.get('tipo', 'imagen')
    archivo_local = item.get('archivo_local', '')
    modelo = item.get('modelo', '').lower()
    parametros = item.get('parametros', {})
    
    # Normalizar tipos de video incorrectos
    if item_type in ['video_seedance', 'video_anime']:
        item_type = 'video'
    
    # Variables para el cálculo
    cost = 0
    model_info = ""
    calculation_details = ""
    
    if item_type == 'imagen':
        cost, model_info, calculation_details = _calculate_image_cost(
            archivo_local, modelo, parametros, item
        )
    elif item_type == 'video':
        cost, model_info, calculation_details = _calculate_video_cost(
            archivo_local, modelo, parametros, item
        )
    
    return round(cost, 3), model_info, calculation_details


def _calculate_image_cost(archivo_local: str, modelo: str, parametros: Dict, item: Dict) -> Tuple[float, str, str]:
    """Calcular costo para imágenes"""
    # Detectar modelo de imagen
    if 'kandinsky' in archivo_local.lower() or 'kandinsky' in modelo:
        model_key = 'kandinsky'
        # Usar tiempo guardado o estimar basado en parámetros
        seconds = item.get('processing_time', 12)  # Tiempo real si está guardado
        if 'num_inference_steps' in parametros:
            # Estimar basado en steps (más steps = más tiempo)
            steps = parametros['num_inference_steps']
            seconds = max(8, min(15, steps * 0.4))  # Entre 8-15 segundos según steps
        cost = COST_RATES['imagen'][model_key]['rate'] * seconds
        model_info = f"Kandinsky ({seconds:.1f}s)"
        calculation_details = f"${COST_RATES['imagen'][model_key]['rate']} × {seconds:.1f}s"
        
    elif 'ssd' in archivo_local.lower() or 'ssd' in modelo:
        model_key = 'ssd_1b'
        # Usar tiempo guardado o estimar basado en parámetros
        seconds = item.get('processing_time', 6)  # Tiempo real si está guardado
        if 'num_inference_steps' in parametros:
            # Estimar basado en steps (más steps = más tiempo)
            steps = parametros['num_inference_steps']
            seconds = max(4, min(10, steps * 0.2))  # Entre 4-10 segundos según steps
        cost = COST_RATES['imagen'][model_key]['rate'] * seconds
        model_info = f"SSD-1B ({seconds:.1f}s)"
        calculation_details = f"${COST_RATES['imagen'][model_key]['rate']} × {seconds:.1f}s"
        
    else:  # Flux Pro por defecto
        model_key = 'flux_pro'
        cost = COST_RATES['imagen'][model_key]['rate']
        model_info = "Flux Pro"
        calculation_details = f"${COST_RATES['imagen'][model_key]['rate']} por imagen"
    
    return cost, model_info, calculation_details


def _calculate_video_cost(archivo_local: str, modelo: str, parametros: Dict, item: Dict) -> Tuple[float, str, str]:
    """Calcular costo para videos"""
    # Detectar modelo de video
    if 'seedance' in archivo_local.lower() or 'seedance' in modelo or item.get('modelo') == 'Seedance':
        model_key = 'seedance'
        # Usar duración guardada o estimar basado en parámetros
        duration = item.get('video_duration', 6)  # Duración real si está guardada
        if 'video_length' in parametros:
            duration = parametros['video_length']
        elif 'duration' in parametros:
            duration = parametros['duration']
        cost = COST_RATES['video'][model_key]['rate'] * duration
        model_info = f"Seedance ({duration}s)"
        calculation_details = f"${COST_RATES['video'][model_key]['rate']} × {duration}s"
        
    elif 'pixverse' in archivo_local.lower() or 'pixverse' in modelo or item.get('modelo') == 'Pixverse':
        model_key = 'pixverse'
        # Para Pixverse usar units calculadas por duración y resolución
        units = item.get('pixverse_units', 1)  # Units reales si están guardadas
        
        # Si no tenemos units guardadas, estimar basado en parámetros
        if units == 1 and parametros:
            # Estimar units basado en duración y resolución
            duration = parametros.get('duration', '5s')
            resolution = parametros.get('resolution', '720p')
            
            # Convertir duración a número
            duration_num = 5  # Por defecto
            if isinstance(duration, str) and duration.endswith('s'):
                try:
                    duration_num = int(duration[:-1])
                except ValueError:
                    duration_num = 5
            elif isinstance(duration, (int, float)):
                duration_num = duration
            
            # Calcular units basado en duración y resolución
            base_units = duration_num * 6  # Base: 6 units por segundo
            if '1080p' in str(resolution):
                units = base_units * 1.5  # 50% más para 1080p
            elif '540p' in str(resolution):
                units = base_units * 0.7  # 30% menos para 540p
            else:  # 720p
                units = base_units
            
            units = round(units, 1)
        
        cost = COST_RATES['video'][model_key]['rate'] * units
        model_info = f"Pixverse ({units} units)"
        calculation_details = f"${COST_RATES['video'][model_key]['rate']} × {units} units"
        
    elif 'veo3' in archivo_local.lower() or 'veo' in modelo:
        model_key = 'veo3'
        # Usar duración guardada o estimar (generalmente 5 segundos)
        duration = item.get('video_duration', 5)
        if 'duration' in parametros:
            duration = parametros['duration']
        cost = COST_RATES['video'][model_key]['rate'] * duration
        model_info = f"VEO 3 Fast ({duration}s)"
        calculation_details = f"${COST_RATES['video'][model_key]['rate']} × {duration}s"
        
    else:  # Seedance por defecto
        model_key = 'seedance'
        # Usar duración guardada o estimar basado en parámetros
        duration = item.get('video_duration', 4)  # Duración real si está guardada
        if 'video_length' in parametros:
            duration = parametros['video_length']
        elif 'duration' in parametros:
            duration = parametros['duration']
        cost = COST_RATES['video'][model_key]['rate'] * duration
        model_info = f"Video genérico ({duration}s)"
        calculation_details = f"${COST_RATES['video'][model_key]['rate']} × {duration}s"
    
    return cost, model_info, calculation_details


def calculate_total_cost(history: List[Dict[str, Any]]) -> float:
    """
    Calcular el costo total de todo el historial
    
    Args:
        history: Lista del historial
        
    Returns:
        float: Costo total en USD
    """
    total = 0
    for item in history:
        cost, _, _ = calculate_item_cost(item)
        total += cost
    return round(total, 3)


def calculate_cost_breakdown(history: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Calcular desglose de costos por modelo y tipo
    
    Args:
        history: Lista del historial
        
    Returns:
        Dict: Desglose detallado de costos
    """
    breakdown = {}
    
    for item in history:
        cost, model_info, _ = calculate_item_cost(item)
        item_type = item.get('tipo', 'imagen')
        
        key = f"{item_type}_{model_info.split()[0].lower()}"
        
        if key not in breakdown:
            breakdown[key] = {
                'type': item_type,
                'model': model_info,
                'count': 0,
                'total_cost': 0
            }
        
        breakdown[key]['count'] += 1
        breakdown[key]['total_cost'] += cost
    
    # Redondear totales
    for key in breakdown:
        breakdown[key]['total_cost'] = round(breakdown[key]['total_cost'], 3)
    
    return breakdown


def convert_usd_to_eur(usd_amount: float, exchange_rate: float = 0.85) -> float:
    """
    Convertir USD a EUR
    
    Args:
        usd_amount: Cantidad en USD
        exchange_rate: Tasa de cambio USD a EUR
        
    Returns:
        float: Cantidad en EUR
    """
    return round(usd_amount * exchange_rate, 3)


def validate_cost(cost: float) -> bool:
    """
    Validar que un costo es válido
    
    Args:
        cost: Costo a validar
        
    Returns:
        bool: True si el costo es válido
    """
    return isinstance(cost, (int, float)) and cost >= 0


def validate_cost_range(cost: float, item_type: str) -> bool:
    """
    Validar que un costo está en un rango razonable para el tipo de ítem
    
    Args:
        cost: Costo a validar
        item_type: Tipo de ítem ('imagen', 'video')
        
    Returns:
        bool: True si el costo está en un rango razonable
    """
    ranges = {
        'imagen': (0.001, 1.0),
        'video': (0.1, 10.0)
    }
    
    if item_type not in ranges:
        return False
    
    min_cost, max_cost = ranges[item_type]
    return min_cost <= cost <= max_cost


# ===============================
# UTILIDADES DE ARCHIVOS
# ===============================

def download_and_save_file(url: str, filename: str, file_type: str) -> Optional[str]:
    """
    Descargar archivo y guardarlo localmente
    
    Args:
        url: URL del archivo a descargar
        filename: Nombre del archivo local
        file_type: Tipo de archivo para mensajes de error
        
    Returns:
        str: Ruta del archivo local o None si falló
    """
    try:
        local_path = HISTORY_DIR / filename
        
        # Si ya existe, no descargar de nuevo
        if local_path.exists():
            return str(local_path)
        
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return str(local_path)
        else:
            return None
    except Exception as e:
        if 'st' in globals():
            st.error(f"Error al descargar {file_type}: {str(e)}")
        return None


def ensure_directory_exists(directory: Path) -> bool:
    """
    Asegurar que un directorio existe
    
    Args:
        directory: Ruta del directorio
        
    Returns:
        bool: True si el directorio existe o se creó exitosamente
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def safe_json_write(file_path: Path, data: Any) -> bool:
    """
    Escribir JSON de forma segura con respaldo
    
    Args:
        file_path: Ruta del archivo
        data: Datos a escribir
        
    Returns:
        bool: True si se escribió exitosamente
    """
    try:
        # Crear respaldo si el archivo existe
        if file_path.exists():
            backup_path = file_path.with_suffix(f'.backup{file_path.suffix}')
            file_path.replace(backup_path)
        
        # Escribir datos
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception:
        return False


def get_file_info(file_path: Path) -> Dict[str, Any]:
    """
    Obtener información de un archivo
    
    Args:
        file_path: Ruta del archivo
        
    Returns:
        Dict: Información del archivo
    """
    try:
        stat = file_path.stat()
        return {
            'exists': True,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'is_file': file_path.is_file(),
            'is_dir': file_path.is_dir()
        }
    except Exception:
        return {'exists': False}


# ===============================
# DASHBOARD DE ESTADÍSTICAS Y COSTOS
# ===============================

def get_comprehensive_stats():
    """
    Obtener estadísticas completas del sistema
    
    Returns:
        Dict: Estadísticas completas organizadas
    """
    history = load_history()
    generation_stats = {}
    
    # Cargar estadísticas de generación si existen
    if os.path.exists("generation_stats.json"):
        with open("generation_stats.json", "r", encoding="utf-8") as f:
            generation_stats = json.load(f)
    
    # Estadísticas por tipo de contenido
    stats_by_type = {
        'imagen': {'count': 0, 'total_cost': 0, 'models': {}},
        'video': {'count': 0, 'total_cost': 0, 'models': {}},
        'texto': {'count': 0, 'total_cost': 0, 'models': {}},  # Para futuros modelos de texto
    }
    
    # Estadísticas por modelo
    stats_by_model = {}
    
    # Estadísticas temporales (por mes)
    stats_by_month = {}
    
    # Procesar historial
    total_cost = 0
    for item in history:
        item_cost, model_info, _ = calculate_item_cost(item)
        item_type = item.get('tipo', 'unknown')
        modelo = item.get('modelo', 'unknown')
        fecha = item.get('fecha', '')
        
        # Normalizar tipo
        if item_type in ['imagen']:
            normalized_type = 'imagen'
        elif item_type in ['video', 'video_seedance']:
            normalized_type = 'video'
        else:
            normalized_type = 'texto'  # Para futuros modelos
        
        # Estadísticas por tipo
        if normalized_type in stats_by_type:
            stats_by_type[normalized_type]['count'] += 1
            stats_by_type[normalized_type]['total_cost'] += item_cost
            
            # Estadísticas por modelo dentro del tipo
            if modelo not in stats_by_type[normalized_type]['models']:
                stats_by_type[normalized_type]['models'][modelo] = {
                    'count': 0, 'cost': 0, 'avg_cost': 0
                }
            stats_by_type[normalized_type]['models'][modelo]['count'] += 1
            stats_by_type[normalized_type]['models'][modelo]['cost'] += item_cost
        
        # Estadísticas por modelo
        if modelo not in stats_by_model:
            stats_by_model[modelo] = {
                'count': 0, 'total_cost': 0, 'type': normalized_type,
                'avg_cost': 0, 'success_rate': 0
            }
        stats_by_model[modelo]['count'] += 1
        stats_by_model[modelo]['total_cost'] += item_cost
        
        # Estadísticas por mes
        if fecha:
            try:
                month_key = fecha[:7]  # YYYY-MM
                if month_key not in stats_by_month:
                    stats_by_month[month_key] = {
                        'count': 0, 'cost': 0, 'types': {'imagen': 0, 'video': 0, 'texto': 0}
                    }
                stats_by_month[month_key]['count'] += 1
                stats_by_month[month_key]['cost'] += item_cost
                stats_by_month[month_key]['types'][normalized_type] += 1
            except:
                pass
        
        total_cost += item_cost
    
    # Calcular promedios y completar datos
    for tipo in stats_by_type:
        for modelo in stats_by_type[tipo]['models']:
            model_data = stats_by_type[tipo]['models'][modelo]
            if model_data['count'] > 0:
                model_data['avg_cost'] = model_data['cost'] / model_data['count']
    
    for modelo in stats_by_model:
        model_data = stats_by_model[modelo]
        if model_data['count'] > 0:
            model_data['avg_cost'] = model_data['total_cost'] / model_data['count']
        
        # Tasa de éxito desde generation_stats.json
        if modelo in generation_stats:
            gen_data = generation_stats[modelo]
            if gen_data.get('total', 0) > 0:
                model_data['success_rate'] = (gen_data.get('exitosas', 0) / gen_data['total']) * 100
    
    return {
        'total_generations': len(history),
        'total_cost_usd': total_cost,
        'total_cost_eur': total_cost * 0.92,
        'stats_by_type': stats_by_type,
        'stats_by_model': stats_by_model,
        'stats_by_month': dict(sorted(stats_by_month.items(), reverse=True)),
        'generation_performance': generation_stats
    }


def get_cost_breakdown_by_period(period='month'):
    """
    Obtener desglose de costos por período
    
    Args:
        period: 'day', 'week', 'month'
        
    Returns:
        Dict: Costos organizados por período
    """
    history = load_history()
    breakdown = {}
    
    for item in history:
        fecha = item.get('fecha', '')
        if not fecha:
            continue
            
        try:
            fecha_obj = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
            
            if period == 'day':
                key = fecha_obj.strftime('%Y-%m-%d')
            elif period == 'week':
                # Obtener el lunes de esa semana
                monday = fecha_obj - timedelta(days=fecha_obj.weekday())
                key = monday.strftime('%Y-W%W')
            else:  # month
                key = fecha_obj.strftime('%Y-%m')
            
            if key not in breakdown:
                breakdown[key] = {
                    'total_cost': 0,
                    'count': 0,
                    'types': {'imagen': {'count': 0, 'cost': 0}, 
                             'video': {'count': 0, 'cost': 0}, 
                             'texto': {'count': 0, 'cost': 0}}
                }
            
            item_cost, _, _ = calculate_item_cost(item)
            item_type = item.get('tipo', 'unknown')
            
            # Normalizar tipo
            if item_type in ['imagen']:
                normalized_type = 'imagen'
            elif item_type in ['video', 'video_seedance']:
                normalized_type = 'video'
            else:
                normalized_type = 'texto'
            
            breakdown[key]['total_cost'] += item_cost
            breakdown[key]['count'] += 1
            breakdown[key]['types'][normalized_type]['count'] += 1
            breakdown[key]['types'][normalized_type]['cost'] += item_cost
            
        except Exception:
            continue
    
    # Ordenar por fecha (más reciente primero)
    return dict(sorted(breakdown.items(), reverse=True))


def get_model_efficiency_ranking():
    """
    Obtener ranking de eficiencia de modelos
    
    Returns:
        List: Modelos ordenados por eficiencia
    """
    stats = get_comprehensive_stats()
    models = []
    
    for model_name, model_data in stats['stats_by_model'].items():
        efficiency_score = 0
        
        # Factores para el score de eficiencia
        success_rate = model_data.get('success_rate', 0)
        avg_cost = model_data.get('avg_cost', 0)
        total_uses = model_data.get('count', 0)
        
        # Calcular score: mayor éxito, menor costo, más uso = mejor score
        if avg_cost > 0:
            cost_factor = 1 / avg_cost  # Inverso del costo
            usage_factor = min(total_uses / 10, 1)  # Normalizar uso (máximo factor 1)
            success_factor = success_rate / 100
            
            efficiency_score = (success_factor * 0.4 + cost_factor * 0.4 + usage_factor * 0.2) * 100
        
        models.append({
            'name': model_name,
            'type': model_data.get('type', 'unknown'),
            'efficiency_score': efficiency_score,
            'success_rate': success_rate,
            'avg_cost': avg_cost,
            'total_uses': total_uses,
            'total_cost': model_data.get('total_cost', 0)
        })
    
    # Ordenar por score de eficiencia
    return sorted(models, key=lambda x: x['efficiency_score'], reverse=True)


def get_spending_alerts():
    """
    Obtener alertas de gasto
    
    Returns:
        List: Lista de alertas
    """
    stats = get_comprehensive_stats()
    alerts = []
    
    # Alerta por gasto total alto
    if stats['total_cost_usd'] > 50:
        alerts.append({
            'type': 'warning',
            'title': 'Gasto Total Elevado',
            'message': f"El gasto total acumulado es ${stats['total_cost_usd']:.2f} USD",
            'icon': '💰'
        })
    
    # Alerta por gasto mensual alto
    monthly_costs = get_cost_breakdown_by_period('month')
    if monthly_costs:
        current_month_cost = list(monthly_costs.values())[0]['total_cost']
        if current_month_cost > 20:
            alerts.append({
                'type': 'warning',
                'title': 'Gasto Mensual Alto',
                'message': f"El gasto del mes actual es ${current_month_cost:.2f} USD",
                'icon': '📅'
            })
    
    # Alerta por modelos ineficientes
    ranking = get_model_efficiency_ranking()
    for model in ranking[-3:]:  # Los 3 menos eficientes
        if model['total_uses'] > 5 and model['success_rate'] < 70:
            alerts.append({
                'type': 'info',
                'title': 'Modelo Poco Eficiente',
                'message': f"{model['name']}: {model['success_rate']:.1f}% éxito, ${model['avg_cost']:.3f} promedio",
                'icon': '⚠️'
            })
    
    return alerts


# ===============================
# UTILIDADES GENERALES
# ===============================

def generate_filename_with_timestamp(prefix: str = "generated", extension: str = "webp") -> str:
    """
    Generar nombre de archivo con timestamp
    
    Args:
        prefix: Prefijo del archivo
        extension: Extensión del archivo
        
    Returns:
        str: Nombre de archivo generado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def sanitize_filename(filename: str) -> str:
    """
    Limpiar nombre de archivo removiendo caracteres no válidos
    
    Args:
        filename: Nombre de archivo a limpiar
        
    Returns:
        str: Nombre de archivo limpio
    """
    # Caracteres no permitidos en nombres de archivo
    invalid_chars = '<>:"/\\|?*'
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limitar longitud
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:95] + ('.' + ext if ext else '')
    
    return filename


def parse_prompt_for_filename(prompt: str, max_words: int = 3) -> str:
    """
    Extraer palabras clave del prompt para nombre de archivo
    
    Args:
        prompt: Prompt del usuario
        max_words: Máximo número de palabras a extraer
        
    Returns:
        str: Nombre base para archivo
    """
    if not prompt:
        return 'generated'
    
    # Palabras a ignorar
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'among', 'image', 'generate', 'create', 'make'
    }
    
    # Limpiar y dividir el prompt
    words = prompt.lower().replace(',', ' ').replace('.', ' ').split()
    
    # Filtrar palabras válidas
    selected_words = []
    for word in words:
        if (len(word) > 2 and 
            word not in stop_words and 
            word.isalpha() and 
            len(selected_words) < max_words):
            selected_words.append(word)
    
    return '_'.join(selected_words) if selected_words else 'generated'


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validar extensión de archivo
    
    Args:
        filename: Nombre del archivo
        allowed_extensions: Lista de extensiones permitidas
        
    Returns:
        bool: True si la extensión es válida
    """
    if not filename or '.' not in filename:
        return False
    
    extension = filename.split('.')[-1].lower()
    return extension in [ext.lower() for ext in allowed_extensions]


def format_file_size(size_bytes: int) -> str:
    """
    Formatear tamaño de archivo en formato legible
    
    Args:
        size_bytes: Tamaño en bytes
        
    Returns:
        str: Tamaño formateado
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_logo_base64(logo_path: str = "assets/logo22.jpg") -> str:
    """
    Cargar el logo y convertirlo a base64 para embebido en HTML
    
    Args:
        logo_path: Ruta al archivo del logo
        
    Returns:
        str: Logo en base64 o string vacío si falla
    """
    try:
        logo_file = Path(logo_path)
        if logo_file.exists():
            with open(logo_file, "rb") as f:
                return base64.b64encode(f.read()).decode()
        else:
            return ""
    except Exception:
        return ""


# ===============================
# VALIDADORES Y HELPERS
# ===============================

def is_valid_url(url: str) -> bool:
    """
    Validar si una URL es válida
    
    Args:
        url: URL a validar
        
    Returns:
        bool: True si la URL es válida
    """
    if not url:
        return False
    
    return url.startswith(('http://', 'https://')) and len(url) > 10


def get_current_timestamp() -> str:
    """
    Obtener timestamp actual en formato ISO
    
    Returns:
        str: Timestamp actual
    """
    return datetime.now().isoformat()


def round_cost(cost: float, decimals: int = 3) -> float:
    """
    Redondear costo con precisión específica
    
    Args:
        cost: Costo a redondear
        decimals: Número de decimales
        
    Returns:
        float: Costo redondeado
    """
    return round(cost, decimals)


# ===============================
# FUNCIONES DE BACKUP Y RESTAURACIÓN
# ===============================

def create_backup() -> Tuple[bool, str, Optional[str]]:
    """
    Crear backup completo de todos los datos de la aplicación
    
    Returns:
        Tuple[bool, str, Optional[str]]: (éxito, mensaje, ruta_del_backup)
    """
    import zipfile
    import shutil
    from datetime import datetime
    
    try:
        # Crear nombre único para el backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"ai_models_backup_{timestamp}.zip"
        backup_path = BACKUPS_DIR / backup_filename
        
        # Crear archivo ZIP
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # 1. Respaldar generation_stats.json
            stats_file = Path("generation_stats.json")
            if stats_file.exists():
                zipf.write(stats_file, "generation_stats.json")
            
            # 2. Respaldar history.json
            if HISTORY_FILE.exists():
                zipf.write(HISTORY_FILE, "historial/history.json")
            
            # 3. Respaldar todos los archivos multimedia del historial
            if HISTORY_DIR.exists():
                for file_path in HISTORY_DIR.iterdir():
                    if file_path.is_file() and file_path.name != "history.json":
                        # Incluir solo archivos multimedia comunes
                        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.mp4', '.mov', '.avi']:
                            zipf.write(file_path, f"historial/{file_path.name}")
            
            # 4. Crear archivo de metadatos del backup
            metadata = {
                "backup_date": timestamp,
                "app_name": "AI Models Pro Generator",
                "backup_version": "1.0",
                "files_included": {
                    "generation_stats": stats_file.exists(),
                    "history_json": HISTORY_FILE.exists(),
                    "media_files": len([f for f in HISTORY_DIR.iterdir() 
                                      if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.mp4', '.mov', '.avi']]) if HISTORY_DIR.exists() else 0
                }
            }
            
            # Añadir metadatos al ZIP
            zipf.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
        
        # Calcular tamaño del backup
        backup_size = backup_path.stat().st_size / (1024 * 1024)  # MB
        
        return True, f"Backup creado exitosamente: {backup_filename} ({backup_size:.1f} MB)", str(backup_path)
        
    except Exception as e:
        return False, f"Error al crear backup: {str(e)}", None


def restore_backup(backup_file_path: str) -> Tuple[bool, str]:
    """
    Restaurar backup desde archivo ZIP
    
    Args:
        backup_file_path: Ruta al archivo de backup
        
    Returns:
        Tuple[bool, str]: (éxito, mensaje)
    """
    import zipfile
    import shutil
    
    try:
        backup_path = Path(backup_file_path)
        
        if not backup_path.exists():
            return False, "El archivo de backup no existe"
        
        if not backup_path.suffix.lower() == '.zip':
            return False, "El archivo debe ser un ZIP válido"
        
        # Crear backup de seguridad de los datos actuales
        current_backup_result = create_backup()
        if current_backup_result[0]:
            safety_backup = current_backup_result[2]
        
        # Extraer y validar el backup
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            
            # Verificar que es un backup válido
            file_list = zipf.namelist()
            if "backup_metadata.json" not in file_list:
                return False, "Archivo de backup inválido (falta metadata)"
            
            # Leer metadatos
            metadata_content = zipf.read("backup_metadata.json").decode('utf-8')
            metadata = json.loads(metadata_content)
            
            # Crear directorio temporal para extraer
            temp_dir = Path("temp_restore")
            temp_dir.mkdir(exist_ok=True)
            
            try:
                # Extraer todos los archivos
                zipf.extractall(temp_dir)
                
                # Restaurar generation_stats.json
                temp_stats = temp_dir / "generation_stats.json"
                if temp_stats.exists():
                    shutil.copy2(temp_stats, "generation_stats.json")
                
                # Restaurar history.json
                temp_history = temp_dir / "historial" / "history.json"
                if temp_history.exists():
                    HISTORY_DIR.mkdir(exist_ok=True)
                    shutil.copy2(temp_history, HISTORY_FILE)
                
                # Restaurar archivos multimedia
                temp_historial_dir = temp_dir / "historial"
                if temp_historial_dir.exists():
                    HISTORY_DIR.mkdir(exist_ok=True)
                    for file_path in temp_historial_dir.iterdir():
                        if file_path.is_file() and file_path.name != "history.json":
                            dest_path = HISTORY_DIR / file_path.name
                            shutil.copy2(file_path, dest_path)
                
                # Limpiar directorio temporal
                shutil.rmtree(temp_dir)
                
                backup_date = metadata.get("backup_date", "desconocida")
                files_count = sum([
                    1 if metadata.get("files_included", {}).get("generation_stats", False) else 0,
                    1 if metadata.get("files_included", {}).get("history_json", False) else 0,
                    metadata.get("files_included", {}).get("media_files", 0)
                ])
                
                return True, f"Backup restaurado exitosamente. Fecha: {backup_date}, Archivos: {files_count}"
                
            except Exception as e:
                # Limpiar directorio temporal si hay error
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                raise e
                
    except Exception as e:
        return False, f"Error al restaurar backup: {str(e)}"


def list_available_backups() -> List[Dict[str, Any]]:
    """
    Listar todos los backups disponibles en la carpeta backups/
    
    Returns:
        List[Dict]: Lista de backups con información
    """
    backups = []
    
    # Buscar archivos de backup en la carpeta backups/
    for file_path in BACKUPS_DIR.glob("ai_models_backup_*.zip"):
        try:
            # Obtener información del archivo
            stat = file_path.stat()
            size_mb = stat.st_size / (1024 * 1024)
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            # Intentar leer metadatos si es posible
            metadata = None
            try:
                import zipfile
                with zipfile.ZipFile(file_path, 'r') as zipf:
                    if "backup_metadata.json" in zipf.namelist():
                        metadata_content = zipf.read("backup_metadata.json").decode('utf-8')
                        metadata = json.loads(metadata_content)
            except:
                pass
            
            backup_info = {
                "filename": file_path.name,
                "full_path": str(file_path),
                "size_mb": round(size_mb, 2),
                "created": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
                "metadata": metadata
            }
            
            backups.append(backup_info)
            
        except Exception:
            continue
    
    # Ordenar por fecha de creación (más reciente primero)
    backups.sort(key=lambda x: x["created"], reverse=True)
    
    return backups


def delete_backup(backup_filename: str) -> Tuple[bool, str]:
    """
    Eliminar un archivo de backup específico
    
    Args:
        backup_filename: Nombre del archivo de backup
        
    Returns:
        Tuple[bool, str]: (éxito, mensaje)
    """
    try:
        # Si solo se proporciona el nombre, construir la ruta completa
        if not backup_filename.startswith(str(BACKUPS_DIR)):
            backup_path = BACKUPS_DIR / backup_filename
        else:
            backup_path = Path(backup_filename)
        
        if not backup_path.exists():
            return False, "El archivo de backup no existe"
        
        if not backup_path.name.startswith("ai_models_backup_"):
            return False, "Solo se pueden eliminar archivos de backup válidos"
        
        backup_path.unlink()
        return True, f"Backup {backup_path.name} eliminado exitosamente"
        
    except Exception as e:
        return False, f"Error al eliminar backup: {str(e)}"
