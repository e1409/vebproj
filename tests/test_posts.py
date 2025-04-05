import pytest
from datetime import datetime
from ..app import app, posts_list
from werkzeug.exceptions import NotFound

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Задание к лабораторной работе'.encode('utf-8') in response.data

def test_posts_page(client):
    """Тест страницы со списком постов"""
    response = client.get('/posts')
    assert response.status_code == 200
    assert 'Последние посты'.encode('utf-8') in response.data

def test_post_page(client):
    """Тест страницы конкретного поста"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    post = posts_list()[0]
    assert post['title'].encode('utf-8') in response.data
    assert post['author'].encode('utf-8') in response.data
    assert post['text'].encode('utf-8') in response.data

def test_post_page_404(client):
    """Тест обработки несуществующего поста"""
    response = client.get('/posts/999')
    assert response.status_code == 404
    assert '404 Not Found'.encode('utf-8') in response.data

def test_post_template_used(client):
    """Тест использования правильного шаблона"""
    response = client.get('/posts/0')
    assert 'Оставьте комментарий'.encode('utf-8') in response.data
    assert 'Отправить'.encode('utf-8') in response.data

def test_post_contains_all_elements(client):
    """Тест наличия всех элементов поста"""
    response = client.get('/posts/0')
    assert b'<img class="card-img-top"' in response.data
    assert b'card-footer text-muted' in response.data
    assert b'media mb-4' in response.data

def test_post_date_format(client):
    """Тест формата даты"""
    response = client.get('/posts/0')
    post = posts_list()[0]
    date_str = post['date'].strftime('%d.%m.%Y в %H:%M').encode('utf-8')
    assert date_str in response.data

def test_post_comments_exist(client):
    """Тест наличия комментариев"""
    response = client.get('/posts/0')
    post = posts_list()[0]
    assert str(len(post['comments'])).encode('utf-8') in response.data

def test_comment_replies_exist(client):
    """Тест наличия ответов на комментарии"""
    response = client.get('/posts/0')
    post = posts_list()[0]
    for comment in post['comments']:
        if 'replies' in comment:
            assert comment['author'].encode('utf-8') in response.data
            assert comment['text'].encode('utf-8') in response.data

def test_footer_exists(client):
    """Тест наличия подвала"""
    response = client.get('/')
    assert 'Баранова Екатерина Ивановна, группа 231-352'.encode('utf-8') in response.data

def test_about_page(client):
    """Тест страницы 'Об авторе'"""
    response = client.get('/about')
    assert response.status_code == 200
    assert 'Об авторе'.encode('utf-8') in response.data

def test_posts_list_length():
    """Тест количества постов"""
    assert len(posts_list()) == 5

def test_posts_sorted_by_date():
    """Тест сортировки постов по дате"""
    posts = posts_list()
    for i in range(len(posts)-1):
        assert posts[i]['date'] >= posts[i+1]['date']

def test_post_image_exists(client):
    """Тест наличия изображения поста"""
    response = client.get('/posts/0')
    post = posts_list()[0]
    assert post['image_id'].encode('utf-8') in response.data

def test_comment_form_exists(client):
    """Тест наличия формы комментария"""
    response = client.get('/posts/0')
    assert b'<textarea class="form-control"' in response.data
    assert b'<button type="submit"' in response.data