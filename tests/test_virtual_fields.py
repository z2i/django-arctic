import pytest

from django.core.urlresolvers import reverse

from articles.views import ArticleListView
from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestVirtualFields(object):
    def _request(self, admin_client):
        response = admin_client.get(reverse('articles:list'))
        assert response.status_code == 200
        return response

    def _assert_list_items_len(self, response, length):
        assert 'list_items' in response.context_data
        assert len(response.context_data['list_items']) == length

    def test_virtual_field(self, admin_client):
        """
        Virtual field displayed in ListView
        """
        article = ArticleFactory()
        view = ArticleListView()
        view.fields = ['title', 'description', 'published', 'category']
        response = self._request(admin_client)
        self._assert_list_items_len(response, 1)

        item = response.context_data['list_items'][0]
        assert item[1] == article.title
        assert item[2] == article.description
        assert item[3] == article.published
        assert item[4] == article.category.name

    def test_missing_virtual_field(self, admin_client):
        """
        Error happens on wrong virtual field name
        """
        article = ArticleFactory()
        view = ArticleListView()
        view.fields = ['title', 'description', 'published', 'virtual_field']
        with pytest.raises(AttributeError) as excinfo:
            view.get_list_items([article])

        message = "'Article' object has no attribute 'virtual_field'"
        assert str(excinfo.value) == message
