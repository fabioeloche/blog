from django.core.management.base import BaseCommand
from blog.models import Category, Tag, Post


class Command(BaseCommand):
    help = 'Create sample categories and tags for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and tags...')

        # Create categories
        categories = [
            {'name': 'Tennis News', 'description': 'Latest tennis news and updates'},
            {'name': 'Player Profiles',
                'description': 'In-depth profiles of tennis players'},
            {'name': 'Tournament Coverage',
                'description': 'Coverage of major tournaments'},
            {'name': 'Tennis Tips', 'description': 'Tips and advice for tennis players'},
            {'name': 'Tennis History', 'description': 'Historical moments in tennis'},
        ]

        created_categories = []
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            created_categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # Create tags
        tags = [
            'Grand Slam', 'ATP', 'WTA', 'Roland Garros', 'Wimbledon',
            'US Open', 'Australian Open', 'Italian Tennis', 'Jannik Sinner',
            'Lorenzo Musetti', 'Novak Djokovic', 'Rafael Nadal', 'Roger Federer',
            'Tennis Strategy', 'Tennis Equipment', 'Tennis Training', 'Tennis History',
            'Tennis Records', 'Tennis Legends', 'Tennis Analysis', 'Tennis Statistics'
        ]

        created_tags = []
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            created_tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
            else:
                self.stdout.write(f'Tag already exists: {tag.name}')

        # Update existing posts with categories and tags
        posts = Post.objects.all()
        if posts.exists():
            self.stdout.write(
                'Updating existing posts with categories and tags...')

            for i, post in enumerate(posts):
                # Assign a category (cycling through available categories)
                if created_categories:
                    post.category = created_categories[i % len(
                        created_categories)]

                # Assign some tags
                if created_tags:
                    # Assign 2-4 random tags to each post
                    import random
                    num_tags = random.randint(2, 4)
                    selected_tags = random.sample(
                        created_tags, min(num_tags, len(created_tags)))
                    post.tags.set(selected_tags)

                post.save()
                self.stdout.write(f'Updated post: {post.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_categories)} categories and {len(created_tags)} tags!'
            )
        )
