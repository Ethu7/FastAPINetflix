import pytest
from app import schemas



def test_get_all_titles(authorized_client, test_titles):
    res = authorized_client.get("/titles/")

    def validate(title):
        return schemas.TitleOut(**title)
    titles_map = map(validate, res.json())
    titles_list = list(titles_map)

    assert len(res.json()) == len(test_titles)
    assert res.status_code == 200


def test_unauthorized_user_get_all_titless(client, test_titles):
    res = client.get("/titles/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_title(client, test_titles):
    res = client.get(f"/titles/{test_titles[0].id}")
    assert res.status_code == 401


def test_get_one_title_not_exist(authorized_client, test_titles):
    res = authorized_client.get(f"/titles/7881234")
    assert res.status_code == 404


def test_get_one_title(authorized_client, test_titles):
    res = authorized_client.get(f"/titles/{test_titles[0].id}")
    title = schemas.TitleOut(**res.json())
    assert title.Title.show_id == test_titles[0].show_id
    assert title.TItle.title == test_titles[0].title


