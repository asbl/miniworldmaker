def bind_method(instance, method):
    bound_method = method.__get__(instance, instance.__class__)
    setattr(instance, method.__name__, bound_method)
    if method.__name__ == "on_setup":
        instance.on_setup()
    return bound_method