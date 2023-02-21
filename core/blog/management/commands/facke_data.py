from datetime import datetime
from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import User, Profile
from blog.models import Post, Category, Tag


# static category and tag
cat_ = ["news", "jobs", "course"]
tag_ = ["IT", "DevOps", "AI", "Data", "Database", "ANN", "CNN", "Crypto"]


class Command(BaseCommand):
    help = "facke data generation commands"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "number_of_users",
            type=int,
            help="Indicates the number of test \
                                user and post to be created",
        )
        parser.add_argument(
            "number_of_posts",
            type=int,
            help="Indicates the number of test \
                                user and post to be created",
        )

    def handle(self, *args, **options):
        userNo = options["number_of_users"]
        postsNo = options["number_of_posts"]
        for category in cat_:
            Category.objects.get_or_create(name=category)

        for tag in tag_:
            Tag.objects.get_or_create(name=tag)

        for _ in range(userNo):
            user = User.objects.create_user(
                email=self.fake.email(), password="123A/a456@"
            )
            profile = Profile.objects.get(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=20)
            profile.save()

            catid = random.sample(range(len(cat_)), random.randint(1, len(cat_)))
            tagid = random.sample(range(len(tag_)), random.randint(1, len(tag_)))

            for _ in range(postsNo):
                p = Post.objects.create(
                    title=self.fake.sentence().replace(".", ""),
                    description=self.fake.paragraph(nb_sentences=10),
                    content=self.fake.paragraph(nb_sentences=120),
                    published=self.fake.boolean(chance_of_getting_true=90),
                    view=self.fake.random_int(min=0, max=9000),
                    author=profile,
                    published_date=datetime.now(),
                )

                for id_ in catid:
                    p.category.add(Category.objects.get(name=cat_[id_]).id)

                for id_ in tagid:
                    p.tag.add(Tag.objects.get(name=tag_[id_]).id)
