

class TestUtils:
    DUMMY_CONFIG = {}


class DummyConfig:
    def __getitem__(self, key):
        return TestUtils.DUMMY_CONFIG[key]

