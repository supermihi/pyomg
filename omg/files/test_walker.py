from pathlib import Path

import pytest

from omg.files.walker import FilesystemAudioFileWalker


@pytest.mark.parametrize('ext', ['.mp3', '.mp4', '.flac', '.ogg'])
def test_is_audio_file(ext):
    test_path = Path(f'file{ext}')
    assert FilesystemAudioFileWalker.is_audio_file(test_path)


@pytest.mark.parametrize('ext', ['.pdf', '.a', '.exe', '.png', '.album'])
def test_is_no_audio_file(ext):
    test_path = Path(f'file{ext}')
    assert not FilesystemAudioFileWalker.is_audio_file(test_path)
