import pytest
from app import schemas


def test_get_all_titles(authorized_client, test_titles):
    res = authorized_client.get("/posts/")

    def validate(title):
        return schemas.PostOut(**title)
    titles_map = map(validate, res.json())
    titles_list = list(titles_map)

    assert len(res.json()) == len(test_titles)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_titles):
    res = client.get("/titles/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_titles):
    res = client.get(f"/posts/{test_titles[0].id}")
    assert res.status_code == 401


def test_get_one_title_not_exist(authorized_client, test_titles):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_title(authorized_client, test_titles):
    res = authorized_client.get(f"/posts/{test_titles[0].id}")
    title = schemas.PostOut(**res.json())
    assert title.Title.show_id == test_titles[0].show_id
    assert title.Post.title == test_titles[0].title


