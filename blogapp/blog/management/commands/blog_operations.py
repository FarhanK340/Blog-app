from django.core.management.base import BaseCommand, CommandError
from blog.models import Blog
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Add or delete blogs fro authenticated users via command line'

    def add_arguments(self, parser):
        parser.add_argument(
            '--add',
            action='store_true',
            help='Create a new blog',
        )

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete a blog',
        )

        parser.add_argument(
            '--title',
            type=str,
            help='Title of the blog',
        )

        parser.add_argument(
            '--content',
            type=str,
            help='Content of the blog',
        )

        parser.add_argument(
            '--author',
            type=str,
            help='Author of the blog',
        )   


    def handle(self, *args, **kwargs):
        if kwargs.get('add'):
            self.create_blog(kwargs)
        elif kwargs.get('delete'):
            self.list_and_delete_blog(kwargs)
        else:
            self.stdout.write(self.style.ERROR('Please provide either --add or --delete option'))

    
    def authenticate_user(self, username):
        """Simulates authentication by checking if user exists."""
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            raise CommandError(f'User with username {username} does not exist')

    def create_blog(self, options):
        title = options.get('title')
        content = options.get('content')
        author = options.get('author')

        if not title or not content or not author:
            raise CommandError('Title, content, and author are required to create a blog.')
        
        author = self.authenticate_user(author)

        blog = Blog.objects.create(title=title, content=content, author=author)
        blog.save()
        self.stdout.write(self.style.SUCCESS(f'Blog with title {title} created successfully')) 


    def list_and_delete_blog(self, options):
        author = options.get('author')

        if not author:
            raise CommandError('Author is required to delete a blog.')
        
        author = self.authenticate_user(author)

        blogs = Blog.objects.filter(author=author)

        if not blogs:
            raise CommandError(f'No blogs found for author {author.username}')
        
        self.stdout.write(f"Blogs by {author.username}:")

        for index, blog in enumerate(blogs, start=1):
            self.stdout.write(f"{index}. {blog.title}")

        blog_choice = input('Enter the number of the blog yu want to delete: ')
        try:
            blog_choice = int(blog_choice)
            blog_to_delete = blogs[blog_choice - 1]
        except (ValueError, IndexError):
            raise CommandError('Invalid choice. Please enter a valid number.')
        
        confirm = input(f"Are you sure you want to delete {blog_to_delete.title}? (yes/no): ")

        if confirm.lower() == 'yes':
            blog_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Blog with title {blog_to_delete.title} deleted successfully'))
        else:
            self.stdout.write(self.style.ERROR('Deletion cancelled'))
