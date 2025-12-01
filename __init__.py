"""My Agent package."""

try:
    from . import my_agent_app
    from .my_agent_app import root_agent
except ImportError:
    # Fallback for when module is not run as a package
    import my_agent_app  # type: ignore
    from my_agent_app import root_agent  # type: ignore

__all__ = ["my_agent_app", "root_agent"]
