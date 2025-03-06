from typing import Dict, Optional
from enum import Enum
import logging

from utils import Environment, logger
import LoginManager


class LoginEnvAwaredManager(LoginManager):
    """
    A class to manage login across different environments.
    """

    def __init__(self, env: Environment = Environment.PROD, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.env = env


    def get_url(self, relative_path: str, env: Environment = Environment.PROD) -> str:
        """
        Get the full URL for the specified relative path and environment.

        Args:
            relative_path: Relative path to append to the base URL
            env: Current environment (default: PROD)

        Returns:
            str: Full URL

        Raises:
            ValueError: If the specified environment is not found
        """
        if relative_path.startswith("http"):
            return relative_path
        try:
            return self._get_login_manager_by_env(env).login_url + relative_path
        except KeyError:
            logger.error(f"Login manager not found for environment: {env}")
            raise ValueError(f"Invalid environment: {env}")

    @property
    def prod_manager(self):
        """Get the production login manager."""
        return self._login_managers[Environment.PROD]

    @property
    def test_manager(self):
        """Get the test login manager."""
        return self._login_managers[Environment.TEST]

    @property
    def staging_manager(self):
        """Get the staging login manager."""
        return self._login_managers.get(Environment.STAGING)
