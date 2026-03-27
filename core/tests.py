from importlib import reload

from django.conf import settings
from django.core.handlers.asgi import ASGIHandler
from django.core.handlers.wsgi import WSGIHandler
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import resolve, reverse

import config.asgi
import config.urls
import config.wsgi

from .views import HomePageView


class HomePageTests(TestCase):
    def test_home_page_returns_success(self) -> None:
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_expected_templates(self) -> None:
        response = self.client.get(reverse("core:home"))

        self.assertTemplateUsed(response, "core/home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_home_page_contains_key_content(self) -> None:
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "Vacation Memories")
        self.assertContains(response, "Photo and video stories from the road")
        self.assertContains(response, "Start simple")

    def test_home_page_url_resolves_to_home_view(self) -> None:
        match = resolve("/")

        self.assertEqual(match.func.view_class, HomePageView)


class ProjectConfigurationTests(SimpleTestCase):
    def test_asgi_application_is_configured(self) -> None:
        module = reload(config.asgi)

        self.assertIsInstance(module.application, ASGIHandler)

    def test_wsgi_application_is_configured(self) -> None:
        module = reload(config.wsgi)

        self.assertIsInstance(module.application, WSGIHandler)

    @override_settings(DEBUG=True)
    def test_debug_urlpatterns_include_media_serving(self) -> None:
        module = reload(config.urls)

        self.assertEqual(len(module.urlpatterns), 3)

    def test_static_url_uses_root_path(self) -> None:
        self.assertEqual(settings.STATIC_URL, "/static/")

    def test_whitenoise_middleware_is_enabled(self) -> None:
        self.assertIn("whitenoise.middleware.WhiteNoiseMiddleware", settings.MIDDLEWARE)

    def test_staticfiles_storage_uses_whitenoise(self) -> None:
        staticfiles_backend = settings.STORAGES["staticfiles"]["BACKEND"]

        self.assertEqual(
            staticfiles_backend,
            "whitenoise.storage.CompressedStaticFilesStorage",
        )

    def test_static_css_is_served(self) -> None:
        response = self.client.get("/static/css/site.css")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], 'text/css; charset="utf-8"')
        self.assertContains(response, "color-scheme: dark")
