from re import S

from django.urls import resolve, reverse
from migrate import views

from .test_post_base import Post, PostTestBase


class PostCategoryViewsTest(PostTestBase):
    
    def test_post_category_view_functions_is_correct(self):
        view = resolve(
            reverse('posts:category', kwargs={'category_id': 1})
            )  
        self.assertIs(view.func, views.category)
    
    def test_post_category_view_returns_404_if_no_posts_found(self):
        response = self.client.get(
            reverse('posts:category', kwargs={'category_id': 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_post_category_template_dont_load_posts_not_published(self):
            # Need a post for this test
        """"test posts is_published False don't show"""
        
        post = self.make_post(is_published=False)
        
        response = self.client.get(
            reverse('posts:post', kwargs={'id': post.category.id})
        )  
        
        self.assertEqual(response.status_code, 404)
        
    
    def test_post_category_template_loads_posts(self):
        needed_title = 'This is a category test'
        # Need a post for this test
        self.make_post(title=needed_title)
        
        response = self.client.get(reverse('posts:category', args=(1,)))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)

        
