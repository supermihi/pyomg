from pathlib import Path

from omg.files.filesystem import FilesystemTagProvider


def test_filesystem():
    audio_files = FilesystemTagProvider(Path(__file__).resolve().parent.parent.parent / 'testdata')
    tags = audio_files.get_tags(Path('r2.mp3'))
    expected_tags = {'COMMENT': ['A COMMENT'], 'GENRE': ['Pop'],
                'QUODLIBET::USERTEXTDESCRIPTION2': ['userTextData1', 'userTextData2'],
                'TITLE': ['I Can Walk On Water I Can Fly'], 'URL': ['http://a.user.url/with/empty/description'],
                'URL:USERURL': ['http://a.user.url'], 'USERTEXTDESCRIPTION1': ['userTextData1', 'userTextData2']}
    assert tags == expected_tags
