import pytest
from django.forms import ModelForm
from django.urls import reverse

from djmvc_example.stage0.models import Item

pytestmark = pytest.mark.tutorial


@pytest.mark.django_db
def test_stage1_navigation_distinct_from_stage0_item(client, admin_user):
    client.force_login(admin_user)
    response = client.get(reverse('site:item:list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert reverse('site:inventory:item:list') in content
    assert 'bi-boxes' in content
    assert 'Inventory' in content
    assert reverse('site:item:list') in content
    assert 'bi-inbox' in content


@pytest.mark.django_db
def test_stage1_inventory_list(client, admin_user):
    Item.objects.create(name="Widget")
    client.force_login(admin_user)

    response = client.get(reverse("site:inventory:item:list"))
    assert response.status_code == 200
    assert b"Widget" in response.content


@pytest.mark.django_db
def test_stage1_inventory_create(client, admin_user):
    client.force_login(admin_user)

    response = client.get(reverse("site:inventory:item:create"))
    assert response.status_code == 200
    assert isinstance(response.context["form"], ModelForm)
    assert "name" in response.context["form"].fields

    client.post(reverse("site:inventory:item:create"), {"name": "Gadget"})
    assert Item.objects.filter(name="Gadget").exists()