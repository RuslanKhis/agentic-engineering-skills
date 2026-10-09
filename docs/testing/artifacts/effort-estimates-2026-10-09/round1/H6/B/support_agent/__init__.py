# Lazy so tool and policy modules import without the ADK SDK installed.
def __getattr__(name):
    if name == "root_agent":
        from .agent import root_agent

        return root_agent
    raise AttributeError(name)
