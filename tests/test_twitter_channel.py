# -*- coding: utf-8 -*-
from unittest.mock import patch, Mock
from agent_reach.channels.twitter import TwitterChannel


def _cp(stdout="", stderr="", returncode=0):
    m = Mock()
    m.stdout = stdout
    m.stderr = stderr
    m.returncode = returncode
    return m


def test_check_bird_found_and_auth_ok():
    """bird found + bird whoami returns 0 → ok."""
    channel = TwitterChannel()
    with patch("shutil.which", side_effect=lambda name: "/usr/local/bin/bird" if name == "bird" else None), patch(
        "subprocess.run",
        return_value=_cp(stdout="authenticated\n", returncode=0),
    ):
        status, message = channel.check()
    assert status == "ok"
    assert "完整可用" in message


def test_check_bird_found_auth_missing():
    """bird found + bird whoami returns non-zero → warn about auth."""
    channel = TwitterChannel()
    with patch("shutil.which", side_effect=lambda name: "/usr/local/bin/bird" if name == "bird" else None), patch(
        "subprocess.run",
        return_value=_cp(stderr="Error: not authenticated\n", returncode=1),
    ):
        status, message = channel.check()
    assert status == "warn"
    assert "未配置 Cookie" in message


def test_check_bird_not_found():
    """bird not found → warn with install hint."""
    channel = TwitterChannel()
    with patch("shutil.which", return_value=None):
        status, message = channel.check()
    assert status == "warn"
    assert "bird CLI 未安装" in message


def test_check_birdx_binary_accepted():
    """birdx is accepted as an alternative binary name."""
    channel = TwitterChannel()
    with patch("shutil.which", side_effect=lambda name: "/usr/local/bin/birdx" if name == "birdx" else None), patch(
        "subprocess.run",
        return_value=_cp(stdout="authenticated\n", returncode=0),
    ):
        status, message = channel.check()
    assert status == "ok"
    assert "完整可用" in message
