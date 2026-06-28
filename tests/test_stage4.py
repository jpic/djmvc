import pytest
from django.urls import reverse

from djmvc_example.stage4.models import Post

pytestmark = pytest.mark.tutorial


@pytest.mark.django_db
def test_stage4_list_shows_custom_list_action(client, admin_user):
    Post.objects.create(title="Hello", category="news")
    client.force_login(admin_user)

    response = client.get(reverse("site:post:list"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "list-action-bar" in content
    assert "Set category" in content
    assert "/post/setcategory/" in content


@pytest.mark.django_db
def test_stage4_bulk_set_category(client, admin_user):
    a = Post.objects.create(title="A", category="news")
    b = Post.objects.create(title="B", category="news")
    c = Post.objects.create(title="C", category="news")
    client.force_login(admin_user)

    url = reverse("site:post:setcategory") + f"?pks={a.pk}&pks={b.pk}"
    assert client.get(url).status_code == 200
    client.post(url, {"category": "blog"})

    a.refresh_from_db()
    b.refresh_from_db()
    c.refresh_from_db()
    assert a.category == "blog"
    assert b.category == "blog"
    assert c.category == "news"


@pytest.mark.django_db
def test_stage4_set_category_form_renders_field(client, admin_user):
    post = Post.objects.create(title="One", category="x")
    client.force_login(admin_user)

    url = reverse("site:post:setcategory") + f"?pks={post.pk}"
    response = client.get(url)
    assert "category" in response.context["form"].fields