from utils import Environment


class LoginEnvAwareManager(object):

    def __init__(
        self, login_manager_prod, login_manager_test, login_manager_staging=None
    ):
        self.login_manager = login_manager_prod
        self.login_manager_test = login_manager_test
        self.login_manager_staging = login_manager_staging

    def check_login_status(self, resp, current_env=Environment.PROD):
        self._get_login_manger_by_env(current_env).check_login_status(resp)

    def get_cookies(self, current_env=Environment.PROD):
        return self._get_login_manger_by_env(current_env).get_cookies()

    def _get_login_manger_by_env(self, env):
        if env == Environment.PROD:
            return self.login_manager
        elif env == Environment.TEST:
            return self.login_manager_test
        elif env == Environment.STAGING:
            return self.login_manager_staging

    def get_url(self, relative_path, env=Environment.PROD):
        if relative_path.startswith("http"):
            return relative_path
        return self._get_login_manger_by_env(env).login_url + relative_path
