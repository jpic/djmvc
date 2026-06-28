import pytest
from django.urls import reverse

from djmvc_example.stage2.models import Article

pytestmark = pytest.mark.tutorial


@pytest.mark.django_db
def test_stage2_list_renders_table_and_filter(client, admin_user):
    for i in range(6):
        Article.objects.create(
            title=f"Article {i}",
            body="body",
            category="news" if i % 2 == 0 else "blog",
        )
    client.force_login(admin_user)

    response = client.get(reverse("site:stage2:list"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "Article 0" in content
    assert "category" in content.lower()


@pytest.mark.django_db
def test_stage2_search_filters_results(client, admin_user):
    Article.objects.create(title="News one", body="", category="news")
    Article.objects.create(title="Blog one", body="", category="blog")
    client.force_login(admin_user)

    response = client.get(reverse("site:stage2:list") + "?search=News")
    content = response.content.decode()
    assert "News one" in content
    assert "Blog one" not in content


@pytest.mark.django_db
def test_stage2_pagination(client, admin_user):
    for i in range(6):
        Article.objects.create(title=f"Row {i}", category="x")
    client.force_login(admin_user)

    response = client.get(reverse("site:stage2:list"))
    assert response.status_code == 200
    assert response.context["paginator"].per_page == 5
    assert response.context["paginator"].num_pages == 2
    assert 'max="2"' in response.content.decode()


@pytest.mark.django_db
def test_stage2_category_update_single_field(client, admin_user):
    article = Article.objects.create(title="Hello", body="text", category="news")
    client.force_login(admin_user)

    url = reverse("site:stage2:categoryupdate", args=[article.pk])
    response = client.get(url)
    assert response.status_code == 200
    form = response.context["form"]
    assert list(form.fields) == ["category"]

    client.post(url, {"category": "blog"})
    article.refresh_from_db()
    assert article.category == "blog"
    assert article.title == "Hello"