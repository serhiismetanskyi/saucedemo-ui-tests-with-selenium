import pytest


class BaseTest:
    """Base test class with common fixtures"""

    @pytest.fixture(autouse=True)
    def injector(self, pages, data):
        """Inject pages and data fixtures into test class"""
        self.pages = pages
        self.data = data
