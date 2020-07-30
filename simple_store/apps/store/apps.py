from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'store'

    def get_model(self, model_name, require_ready=True):
        return super().get_model(model_name, require_ready=require_ready)
