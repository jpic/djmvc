import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from djmvc_example.models import User
from djmvc_example.stage2.models import Document

pytestmark = pytest.mark.tutorial


def grant_document_perm(user, codename):
    content_type = ContentType.objects.get_for_model(Document)
    perm = Permission.objects.get(content_type=content_type, codename=codename)
    user.user_permissions.add(perm)


@pytest.mark.django_db
def test_stage2_list_scoped_to_owner(client, admin_user):
    owner = User.objects.create_user("owner", password="pass")
    other = User.objects.create_user("other", password="pass")
    grant_document_perm(owner, "view_document")
    Document.objects.create(title="mine", owner=owner)
    Document.objects.create(title="theirs", owner=other)
    client.force_login(owner)

    response = client.get(reverse("site:document:list"))
    content = response.content.decode()
    assert response.status_code == 200
    assert "mine" in content
    assert "theirs" not in content


@pytest.mark.django_db
def test_stage2_detail_404_outside_scope(client, admin_user):
    owner = User.objects.create_user("owner", password="pass")
    other = User.objects.create_user("other", password="pass")
    grant_document_perm(owner, "view_document")
    doc = Document.objects.create(title="secret", owner=other)
    client.force_login(owner)

    response = client.get(reverse("site:document:detail", args=[doc.pk]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_stage2_list_denied_without_view_permission(client, admin_user):
    Document.objects.create(title="Doc", owner=admin_user)
    reader = User.objects.create_user("reader", password="pass")
    client.force_login(reader)

    response = client.get(reverse("site:document:list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_stage2_list_allowed_with_view_permission(client, admin_user):
    reader = User.objects.create_user("reader", password="pass")
    grant_document_perm(reader, "view_document")
    Document.objects.create(title="Visible", owner=reader)
    client.force_login(reader)

    response = client.get(reverse("site:document:list"))
    assert response.status_code == 200
    assert b"Visible" in response.content


@pytest.mark.django_db
def test_stage2_bulk_delete_intersects_scope(client, admin_user):
    owner = User.objects.create_user("owner", password="pass")
    other = User.objects.create_user("other", password="pass")
    grant_document_perm(owner, "view_document")
    grant_document_perm(owner, "delete_document")
    mine = Document.objects.create(title="mine", owner=owner)
    theirs = Document.objects.create(title="theirs", owner=other)
    client.force_login(owner)

    url = (
        reverse("site:document:deleteobjects")
        + f"?pks={mine.pk}&pks={theirs.pk}"
    )
    response = client.get(url)
    content = response.content.decode()
    assert "mine" in content
    assert "theirs" not in content

    client.post(url, {"next": reverse("site:document:list")})
    assert Document.objects.filter(pk=mine.pk).exists() is False
    assert Document.objects.filter(pk=theirs.pk).exists() is True