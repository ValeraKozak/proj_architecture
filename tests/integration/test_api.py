from src.models.entities import Role
from tests.conftest import auth_header


def test_healthcheck(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_and_login_flow(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "api@example.com",
            "full_name": "Api User",
            "password": "password123",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": "api@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_listing_moderation_and_message_flow(client, db_session, seeded_users, seeded_category):
    seeded_users["moderator"].role = Role.MODERATOR
    db_session.commit()

    create_response = client.post(
        "/listings",
        json={
            "title": "MacBook Air M2",
            "description": "Great notebook for work and study with charger and warranty included.",
            "price": 950,
            "category_id": seeded_category.id,
        },
        headers=auth_header(seeded_users["owner"].email),
    )
    assert create_response.status_code == 201
    listing_id = create_response.json()["id"]

    moderation_response = client.post(
        f"/moderation/listings/{listing_id}",
        json={"approved": True},
        headers=auth_header(seeded_users["moderator"].email),
    )
    assert moderation_response.status_code == 200

    public_response = client.get("/listings")
    assert public_response.status_code == 200
    assert len(public_response.json()) == 1

    message_response = client.post(
        "/messages",
        json={
            "listing_id": listing_id,
            "recipient_id": seeded_users["owner"].id,
            "body": "Is the laptop still available?",
        },
        headers=auth_header(seeded_users["buyer"].email),
    )
    assert message_response.status_code == 201


def test_blocked_user_cannot_create_listing(client, db_session, seeded_users, seeded_category):
    seeded_users["owner"].is_blocked = True
    db_session.commit()

    response = client.post(
        "/listings",
        json={
            "title": "Blocked listing",
            "description": "This description is long enough for request validation to pass.",
            "price": 100,
            "category_id": seeded_category.id,
        },
        headers=auth_header(seeded_users["owner"].email),
    )
    assert response.status_code == 403


def test_non_moderator_cannot_review_listing(client, seeded_users, approved_listing):
    response = client.post(
        f"/moderation/listings/{approved_listing.id}",
        json={"approved": True},
        headers=auth_header(seeded_users["buyer"].email),
    )
    assert response.status_code == 403
