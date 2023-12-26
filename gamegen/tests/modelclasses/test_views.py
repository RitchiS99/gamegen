import pytest
import test_helpers

from django.urls import reverse


pytestmark = [pytest.mark.django_db]


def tests_dislikes_list_view(client):
    instance1 = test_helpers.create_modelclasses_dislikes()
    instance2 = test_helpers.create_modelclasses_dislikes()
    url = reverse("modelclasses_dislikes_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_dislikes_create_view(client):
    game = test_helpers.create_modelclasses_game()
    location = test_helpers.create_modelclasses_location()
    url = reverse("modelclasses_dislikes_create")
    data = {
        "disliker": "text",
        "game": game.pk,
        "location": location.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_dislikes_detail_view(client):
    instance = test_helpers.create_modelclasses_dislikes()
    url = reverse("modelclasses_dislikes_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_dislikes_update_view(client):
    game = test_helpers.create_modelclasses_game()
    location = test_helpers.create_modelclasses_location()
    instance = test_helpers.create_modelclasses_dislikes()
    url = reverse("modelclasses_dislikes_update", args=[instance.pk, ])
    data = {
        "disliker": "text",
        "game": game.pk,
        "location": location.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_expansion_list_view(client):
    instance1 = test_helpers.create_modelclasses_expansion()
    instance2 = test_helpers.create_modelclasses_expansion()
    url = reverse("modelclasses_expansion_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_expansion_create_view(client):
    base_game = test_helpers.create_modelclasses_game()
    url = reverse("modelclasses_expansion_create")
    data = {
        "rule_link": http://127.0.0.1,
        "release_date": datetime.now(),
        "number": 1,
        "name": "text",
        "max_player": 1,
        "min_player": 1,
        "teaming": "text",
        "base_game": base_game.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_expansion_detail_view(client):
    instance = test_helpers.create_modelclasses_expansion()
    url = reverse("modelclasses_expansion_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_expansion_update_view(client):
    base_game = test_helpers.create_modelclasses_game()
    instance = test_helpers.create_modelclasses_expansion()
    url = reverse("modelclasses_expansion_update", args=[instance.pk, ])
    data = {
        "rule_link": http://127.0.0.1,
        "release_date": datetime.now(),
        "number": 1,
        "name": "text",
        "max_player": 1,
        "min_player": 1,
        "teaming": "text",
        "base_game": base_game.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_game_list_view(client):
    instance1 = test_helpers.create_modelclasses_game()
    instance2 = test_helpers.create_modelclasses_game()
    url = reverse("modelclasses_game_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_game_create_view(client):
    genre = test_helpers.create_modelclasses_genre()
    url = reverse("modelclasses_game_create")
    data = {
        "rule_link": http://127.0.0.1,
        "teaming": "text",
        "name": "text",
        "max_player": 1,
        "release_date": datetime.now(),
        "duration": 1,
        "min_player": 1,
        "genre": genre.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_game_detail_view(client):
    instance = test_helpers.create_modelclasses_game()
    url = reverse("modelclasses_game_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_game_update_view(client):
    genre = test_helpers.create_modelclasses_genre()
    instance = test_helpers.create_modelclasses_game()
    url = reverse("modelclasses_game_update", args=[instance.pk, ])
    data = {
        "rule_link": http://127.0.0.1,
        "teaming": "text",
        "name": "text",
        "max_player": 1,
        "release_date": datetime.now(),
        "duration": 1,
        "min_player": 1,
        "genre": genre.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_genre_list_view(client):
    instance1 = test_helpers.create_modelclasses_genre()
    instance2 = test_helpers.create_modelclasses_genre()
    url = reverse("modelclasses_genre_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_genre_create_view(client):
    url = reverse("modelclasses_genre_create")
    data = {
        "name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_genre_detail_view(client):
    instance = test_helpers.create_modelclasses_genre()
    url = reverse("modelclasses_genre_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_genre_update_view(client):
    instance = test_helpers.create_modelclasses_genre()
    url = reverse("modelclasses_genre_update", args=[instance.pk, ])
    data = {
        "name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_location_list_view(client):
    instance1 = test_helpers.create_modelclasses_location()
    instance2 = test_helpers.create_modelclasses_location()
    url = reverse("modelclasses_location_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_location_create_view(client):
    wishlist_games = test_helpers.create_modelclasses_game()
    creater = test_helpers.create_User()
    viewer = test_helpers.create_User()
    expansions = test_helpers.create_modelclasses_expansion()
    wishlist_expansions = test_helpers.create_modelclasses_expansion()
    editer = test_helpers.create_User()
    game = test_helpers.create_modelclasses_game()
    url = reverse("modelclasses_location_create")
    data = {
        "name": "text",
        "wishlist_games": wishlist_games.pk,
        "creater": creater.pk,
        "viewer": viewer.pk,
        "expansions": expansions.pk,
        "wishlist_expansions": wishlist_expansions.pk,
        "editer": editer.pk,
        "game": game.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_location_detail_view(client):
    instance = test_helpers.create_modelclasses_location()
    url = reverse("modelclasses_location_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_location_update_view(client):
    wishlist_games = test_helpers.create_modelclasses_game()
    creater = test_helpers.create_User()
    viewer = test_helpers.create_User()
    expansions = test_helpers.create_modelclasses_expansion()
    wishlist_expansions = test_helpers.create_modelclasses_expansion()
    editer = test_helpers.create_User()
    game = test_helpers.create_modelclasses_game()
    instance = test_helpers.create_modelclasses_location()
    url = reverse("modelclasses_location_update", args=[instance.pk, ])
    data = {
        "name": "text",
        "wishlist_games": wishlist_games.pk,
        "creater": creater.pk,
        "viewer": viewer.pk,
        "expansions": expansions.pk,
        "wishlist_expansions": wishlist_expansions.pk,
        "editer": editer.pk,
        "game": game.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302
