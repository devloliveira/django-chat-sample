from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

STATUS = (
    ('p', 'pending'),
    ('a', 'accepted'),
    ('r', 'rejected'),
)

class UserConnection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, related_name='target_user', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='p',
    )

    @staticmethod
    def get_connection(userA, userB, status=None):
        from django.db.models import Q

        dataset = UserConnection.objects.filter(
            (
                Q(author=userA) & Q(target_user=userB)
            ) |
            (
                Q(author=userB) & Q(target_user=userA)
            )
        )

        if status:
            dataset = dataset.filter(Q(status=status))

        return dataset.first()
