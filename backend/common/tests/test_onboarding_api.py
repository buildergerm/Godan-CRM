import pytest
from rest_framework import status


@pytest.mark.django_db
class TestOnboardingApi:
    url = "/api/auth/onboarding/"

    def test_get_returns_empty_state_for_new_user(self, admin_client, admin_user):
        response = admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"answers": {}, "completed": False}
        assert admin_user.onboarding_data == {}

    def test_partial_answers_are_persisted_and_resumable(
        self, admin_client, admin_user
    ):
        answers = {
            "role": "Founder / business owner",
            "industry": "Technology / SaaS",
        }
        saved = admin_client.patch(
            self.url, {"answers": answers, "completed": False}, format="json"
        )
        assert saved.status_code == status.HTTP_200_OK
        admin_user.refresh_from_db()
        assert admin_user.onboarding_data == {"answers": answers, "completed": False}
        resumed = admin_client.get(self.url)
        assert resumed.data["answers"] == answers

    def test_completion_requires_core_answers_and_rejects_unknown_choices(
        self, admin_client
    ):
        incomplete = admin_client.patch(
            self.url, {"answers": {"role": "Sales"}, "completed": True}, format="json"
        )
        assert incomplete.status_code == status.HTTP_400_BAD_REQUEST
        invalid = admin_client.patch(
            self.url,
            {"answers": {"industry": "Fake Industry"}, "completed": False},
            format="json",
        )
        assert invalid.status_code == status.HTTP_400_BAD_REQUEST

    def test_complete_onboarding_is_saved(self, admin_client, admin_user):
        answers = {
            "role": "Founder / business owner",
            "industry": "Technology / SaaS",
            "company_size": "2–5 people",
            "goals": ["Manage leads", "Grow sales"],
            "current_tool": "Spreadsheet",
            "challenge": "Keeping track of follow-up",
        }
        response = admin_client.patch(
            self.url, {"answers": answers, "completed": True}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["completed"] is True
        admin_user.refresh_from_db()
        assert admin_user.onboarding_data["answers"] == answers
