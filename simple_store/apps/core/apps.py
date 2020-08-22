from django.apps import AppConfig
from watson import search as watson


class CoreConfig(AppConfig):
    name = "simple_store.apps.core"

    def ready(self):
        Product = self.get_model("Product")
        Brand = self.get_model("Brand")
        Category = self.get_model("Category")

        watson.register(Product)
        watson.register(Brand)
        watson.register(Category)

