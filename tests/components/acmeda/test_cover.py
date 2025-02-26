"""Define tests for the Acmeda config flow."""

import pytest

from homeassistant.components.acmeda.const import DOMAIN
from homeassistant.components.cover import DOMAIN as COVER_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("mock_hub_run")
async def test_cover_id_migration(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test migrating unique id."""
    mock_config_entry.add_to_hass(hass)
    entity_registry.async_get_or_create(
        COVER_DOMAIN, DOMAIN, 1234567890123, config_entry=mock_config_entry
    )
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    await hass.async_block_till_done()
    entities = er.async_entries_for_config_entry(
        entity_registry, mock_config_entry.entry_id
    )
    assert len(entities) == 1
    assert entities[0].unique_id == "1234567890123"
