#!/usr/bin/env python3
"""
Tests unitarios para el motor de scoring de Cazador CLI.
Valida la función pura calcular_score contra el Contrato 01.

Ejecutar: python -m pytest src/test.py -v
      o:  python src/test.py
"""
import sys
import os

# Asegurar que src/ esté en el path para imports locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import calcular_score, PATRONES_DOLOR


def test_zero_engagement_zero_patterns():
    """Sin engagement y sin patrones de dolor → score 0."""
    assert calcular_score("hello world") == 0.0


def test_zero_engagement_one_pattern():
    """RSS Mode: un patrón detectado → score 1.0."""
    assert calcular_score("I hate this tool") == 1.0


def test_zero_engagement_multiple_patterns():
    """RSS Mode: múltiples patrones → score = conteo."""
    # "hate" + "broken" = 2
    assert calcular_score("I hate this broken app") == 2.0


def test_zero_engagement_pattern_in_dolor():
    """RSS Mode: patrón en campo dolor, no en título."""
    score = calcular_score("Just a post", dolor="this is a nightmare")
    assert score == 1.0


def test_zero_engagement_patterns_in_both():
    """RSS Mode: patrones en título Y dolor se suman."""
    # "struggle" en título + "broken" en dolor = 2
    score = calcular_score("I struggle daily", dolor="everything is broken")
    assert score == 2.0


def test_with_engagement_no_patterns():
    """Plan A: engagement real sin patrones → base_score puro."""
    # (10 * 0.4) + (100 * 0.0009) = 4.0 + 0.09 = 4.09
    score = calcular_score("normal post", comentarios=10, votos=100)
    assert score == 4.09


def test_with_engagement_and_patterns():
    """Plan A: engagement + patrones → multiplicador aplicado."""
    # base = (10 * 0.4) + (0 * 0.0009) = 4.0
    # "hate" = 1 coincidencia → multiplier = 1.0 + (1 * 0.5) = 1.5
    # score = 4.0 * 1.5 = 6.0
    score = calcular_score("I hate this", comentarios=10, votos=0)
    assert score == 6.0


def test_dolor_none_no_crash():
    """dolor=None no causa crash."""
    score = calcular_score("normal title", dolor=None)
    assert isinstance(score, float)


def test_case_insensitive():
    """Detección es case-insensitive."""
    assert calcular_score("I HATE THIS") == calcular_score("i hate this")


def test_score_never_negative():
    """Contrato: score_gap >= 0 siempre."""
    score = calcular_score("", dolor=None, comentarios=0, votos=0)
    assert score >= 0.0


def test_partial_pattern_no_match():
    """'hater' no matchea 'hate' por substring? — SÍ matchea (in operator)."""
    # Nota: 'hate' IN 'hater' es True en Python. Esto es comportamiento esperado.
    score = calcular_score("I am a hater")
    assert score == 1.0  # 'hate' está contenido en 'hater'


def test_all_patterns_count():
    """Verificar que PATRONES_DOLOR tiene exactamente 16 patrones."""
    assert len(PATRONES_DOLOR) == 16


def test_return_type_is_float():
    """El retorno siempre es float, nunca int."""
    score = calcular_score("test")
    assert type(score) is float


# --- Runner directo ---
if __name__ == "__main__":
    tests = [
        test_zero_engagement_zero_patterns,
        test_zero_engagement_one_pattern,
        test_zero_engagement_multiple_patterns,
        test_zero_engagement_pattern_in_dolor,
        test_zero_engagement_patterns_in_both,
        test_with_engagement_no_patterns,
        test_with_engagement_and_patterns,
        test_dolor_none_no_crash,
        test_case_insensitive,
        test_score_never_negative,
        test_partial_pattern_no_match,
        test_all_patterns_count,
        test_return_type_is_float,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print(f"  ✅ {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  ❌ {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"  💥 {test.__name__}: {type(e).__name__}: {e}")

    print(f"\n{'='*40}")
    print(f"  Resultado: {passed} passed, {failed} failed / {len(tests)} total")
    if failed == 0:
        print("  🟢 ALL CLEAR — Contrato verificado.")
    else:
        print("  🔴 HAY FALLOS — Revisar antes de producción.")
        sys.exit(1)
