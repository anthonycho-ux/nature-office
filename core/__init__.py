"""
nature-office: Alberta's premium mobile office solution for AI professionals.

A marketplace connecting idle RV/cargo van owners with AI consulting firms
and government agencies that need certified mobile office vehicles.

The core features include:
- AI-powered office-ready vehicle certification (5-pillar assessment)
- Executive/Professional/Office/Basic certification tiers
- Multi-model AI integration (Claude, GPT, Gemini)
- Two-sided marketplace platform for mobile office rentals

Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "Alberta AI Mobile Office Team"
__license__ = "MIT"

from .agy_bridge import AgyBridge, AgentStatusInfo
from .policy import OfficeReadyPolicy, ExecutionMode

__all__ = [
    "__version__",
    "AgyBridge",
    "AgentStatusInfo",
    "OfficeReadyPolicy",
    "ExecutionMode",
]