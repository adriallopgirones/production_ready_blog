import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_blog_post_retrieve(user_client, blog_posts):
    url = reverse("blogpost-detail", kwargs={"pk": blog_posts[0].id})
    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == blog_posts[0].title
    assert (
        "comments" in response.data
    )  # Make sure comments are included in the response


# @pytest.mark.django_db
# def test_blog_post_list(user_client, blog_posts):
#     url = reverse("blogpost-list")
#     response = user_client.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) == 2
#     assert response.data[0]["title"] == blog_posts[0].title
#     assert response.data[1]["title"] == blog_posts[1].title
