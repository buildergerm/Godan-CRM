from django.test import RequestFactory, SimpleTestCase

from common.middleware.get_company import GetProfileAndOrg
from common.middleware.rls_context import RequireOrgContext


RECOVERY_PATHS = (
    "/api/auth/recovery/request-code/",
    "/api/auth/recovery/resend-code/",
    "/api/auth/recovery/validate-code/",
    "/api/auth/recovery/reset-password/",
)


class AnonymousRecoveryMiddlewareExemptionTests(SimpleTestCase):
    def test_recovery_routes_are_exact_org_context_exemptions(self):
        middleware = RequireOrgContext(lambda request: None)
        for path in RECOVERY_PATHS:
            with self.subTest(path=path):
                self.assertIn(path, middleware.EXEMPT_EXACT_PATHS)
                self.assertTrue(middleware._is_exempt(path))

    def test_recovery_routes_skip_jwt_org_resolution(self):
        middleware = GetProfileAndOrg(lambda request: None)
        factory = RequestFactory()
        for path in RECOVERY_PATHS:
            with self.subTest(path=path):
                request = factory.post(path)
                self.assertIsNone(middleware.process_request(request))

    def test_reset_route_exemption_does_not_cover_subpaths(self):
        middleware = RequireOrgContext(lambda request: None)
        self.assertFalse(middleware._is_exempt(
            "/api/auth/recovery/reset-password/extra/"
        ))

    def test_old_misspelled_reset_route_is_not_exempt(self):
        middleware = RequireOrgContext(lambda request: None)
        self.assertFalse(middleware._is_exempt(
            "/api/auth/recovery/complete-reset/"
        ))
