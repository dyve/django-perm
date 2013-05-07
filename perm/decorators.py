from .permissions import permissions_manager

# Decorator for models
def permissions(permissions_class):
    def wrap(model):
        permissions_manager.register(model, permissions_class)
        return model
    return wrap


# Decorator for permissions class
def permissions_for(model):
    def wrap(permissions_class):
        permissions_manager.register(model, permissions_class)
        return permissions_class
    return wrap
