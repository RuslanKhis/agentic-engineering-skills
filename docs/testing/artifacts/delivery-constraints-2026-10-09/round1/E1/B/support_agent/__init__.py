"""Support agent package.

root_agent is loaded lazily so that `from support_agent import tools` works
without google-adk installed (tool unit tests).
"""


def __getattr__(name):
    if name == "root_agent":
        from .agent import root_agent

        return root_agent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
