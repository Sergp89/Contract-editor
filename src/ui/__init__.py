"""Инициализация пакета UI."""

from src.ui.dashboard import Dashboard, ContentArea, TopAppBar, SkeletonLoader, create_dashboard
from src.ui.navigation import NavigationRail, ResponsiveNavigation

__all__ = [
    "Dashboard",
    "ContentArea",
    "TopAppBar",
    "SkeletonLoader",
    "NavigationRail",
    "ResponsiveNavigation",
    "create_dashboard",
]
