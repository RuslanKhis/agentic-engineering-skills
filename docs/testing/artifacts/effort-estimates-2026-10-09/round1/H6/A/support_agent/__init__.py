def __getattr__(name):
    # Lazy so tool and policy modules can be tested without the ADK SDK installed.
    if name == "root_agent":
        from .agent import root_agent
        return root_agent
    raise AttributeError(name)
