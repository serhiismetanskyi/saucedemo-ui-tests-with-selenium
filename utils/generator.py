from faker import Faker


class DataGenerator:
    """Generate fake test data using Faker library"""

    def __init__(self, seed=None):
        """Initialize data generator with optional seed"""
        self.fake = Faker()
        if seed:
            self.fake.seed(seed)

    def first_name(self):
        """Generate random first name"""
        return self.fake.first_name()

    def last_name(self):
        """Generate random last name"""
        return self.fake.last_name()

    def zip_code(self):
        """Generate random zip code"""
        return self.fake.postcode()
