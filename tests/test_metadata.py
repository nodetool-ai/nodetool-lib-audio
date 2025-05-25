import json
from pathlib import Path

PACKAGE_METADATA_PATH = Path(__file__).resolve().parents[1] / 'src' / 'nodetool' / 'package_metadata' / 'nodetool-lib-audio.json'
PYPROJECT_PATH = Path(__file__).resolve().parents[1] / 'pyproject.toml'


def load_metadata():
    return json.loads(PACKAGE_METADATA_PATH.read_text())


def test_metadata_has_correct_name_and_version():
    metadata = load_metadata()
    assert metadata['name'] == 'nodetool-lib-audio'
    # ensure version matches pyproject
    pyproject_text = PYPROJECT_PATH.read_text()
    for line in pyproject_text.splitlines():
        if line.startswith('version'):
            version = line.split('=')[-1].strip().strip('"')
            break
    else:
        raise AssertionError('Version not found in pyproject.toml')
    assert metadata['version'] == version


def test_waveform_property_contains_expected_enums():
    metadata = load_metadata()
    nodes = metadata['nodes']
    oscillator_node = next(n for n in nodes if n.get('title') == 'Oscillator')
    waveform_prop = next(p for p in oscillator_node['properties'] if p['name'] == 'waveform')
    assert waveform_prop['type']['values'] == ['sine', 'square', 'sawtooth', 'triangle']
