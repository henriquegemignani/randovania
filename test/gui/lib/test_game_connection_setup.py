import pytest
from PySide2 import QtWidgets
from mock import MagicMock, AsyncMock

from randovania.game_connection.dolphin_backend import DolphinBackend
from randovania.game_connection.game_connection import GameConnection
from randovania.gui.lib.game_connection_setup import GameConnectionSetup


@pytest.fixture(name="setup")
def _setup(skip_qtbot):
    parent = QtWidgets.QWidget()
    skip_qtbot.addWidget(parent)
    tool = QtWidgets.QToolButton(parent)
    label = QtWidgets.QLabel(parent)

    return GameConnectionSetup(parent, tool, label, GameConnection(DolphinBackend()), MagicMock())


@pytest.mark.parametrize("nintendont_ip", [None, "localhost", "192.168.0.1"])
@pytest.mark.asyncio
async def test_on_use_nintendont_backend_accept(setup, mocker, nintendont_ip):
    mock_execute_dialog = mocker.patch("randovania.gui.lib.async_dialog.execute_dialog", new_callable=AsyncMock,
                                       return_value=QtWidgets.QDialog.Accepted)
    setup.options.nintendont_ip = nintendont_ip
    old_backend = setup.game_connection.backend

    # Run
    await setup.on_use_nintendont_backend()

    # Assert
    mock_execute_dialog.assert_awaited_once()
    dialog: QtWidgets.QInputDialog = mock_execute_dialog.mock_calls[0].args[0]
    if nintendont_ip is not None:
        assert dialog.textValue() == nintendont_ip
        assert setup.game_connection.backend is not old_backend
        assert setup.use_nintendont_backend.isChecked()
        assert setup.use_nintendont_backend.text() == f"Nintendont: {nintendont_ip}"

    else:
        assert dialog.textValue() == ""
        assert setup.game_connection.backend is old_backend