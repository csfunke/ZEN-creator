"""Pytest fixtures for end-to-end tests with registry isolation."""

from __future__ import annotations

from typing import Iterator

import pytest

from zen_creator.elements import Element

# Global variable to store the clean registry state at session start
_CLEAN_REGISTRY_STATE: dict[str, type] | None = None


@pytest.fixture(scope="session", autouse=True)
def save_clean_registry_state() -> Iterator[None]:
    """Save the clean registry state at the beginning of the session.

    This fixture runs once at the start of the entire test session and captures
    the registry state BEFORE test_from_config.py's classes are imported.
    This ensures we have a reference to the original, uncontaminated state.
    """
    global _CLEAN_REGISTRY_STATE
    _CLEAN_REGISTRY_STATE = Element.get_registry().copy()
    yield


@pytest.fixture(autouse=True)
def reset_element_registry() -> Iterator[None]:
    """Reset element registry before each test to prevent cross-test pollution.

    This function-scoped fixture restores the clean registry state before
    each test runs, ensuring that custom element classes defined in test_from_config.py
    don't interfere with tests like test_crystal_ball.
    """
    # Before the test: restore to the clean state
    if _CLEAN_REGISTRY_STATE is not None:
        Element.clear_registry()
        Element.update_registry(_CLEAN_REGISTRY_STATE)

    yield

    # After the test: we don't need to do anything special
