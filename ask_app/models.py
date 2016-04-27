from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()

class TagManager(models.Manager):
    # adds number of questions to each tag
    def with_question_count(self):
        return self.annotate(questions_count=Count('question'))

    # sorts tags using number of questions
    def order_by_question_count(self):
        return self.with_question_count().order_by('-questions_count')

    # searches using title
    def get_by_title(self, title):
        return self.get(title=title)

    # finds or creates
    def get_or_create(self, title):
        try:
            tag = self.get_by_title(title)
        except Tag.DoesNotExist:
            tag = self.create(title=title, color=choice(Tag.COLORS)[0])
        return tag

    # counts most popular tags
    def count_popular(self):
        return self.order_by_question_count().all()[:20]

class Tag(models.Model):
    GREEN = 'success'
    DBLUE = 'primary'
    BLACK = 'default'
    RED = 'danger'
    LBLUE = 'info'
    COLORS = (
            ('GR', GREEN),
            ('DB', DBLUE),
            ('B', BLACK),
            ('RE', RED),
            ('BL', LBLUE)
    )
    
    objects = TagManager()
    
    title = models.CharField(max_length=30)
    color = models.CharField(max_length=2, choices=COLORS, default=BLACK)

    def get_url(self):
        return reverse(kwargs={'tag': self.title})

class QuestionQuerySet(models.QuerySet):
    # preloads tags
    def with_tags(self):
        return self.prefetch_related('tags')

    # preloads answers
    def with_answers(self):
        res = self.prefetch_related('answer_set')
        res = self.prefetch_related('answer_set__author')
        res = self.prefetch_related('answer_set__author__profile')
        return res

    # loads number of answers
    def with_answers_count(self):
        return self.annotate(answers=Count('answer__id', distinct=True))

    # loads author
    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    # order by popularity
    def order_by_popularity(self):
        return self.order_by('-likes')

    # filter by date
    def with_date_greater(self, date):
        return self.filter(date__gt=date)

class QuestionManager(models.Manager):
    # custom query set
    def get_queryset(self):
        res = QuestionQuerySet(self.model, using=self._db)
        return res.with_answers_count().with_author().with_tags()

    # list of new questions
    def list_new(self):
        return self.order_by('-date')

    # list of hot questions
    def list_hot(self):
        return self.order_by('-likes')

    # list of questions with tag
    def list_tag(self, tag):
        return self.filter(tags=tag)

    # single question
    def get_single(self, id):
        res = self.get_queryset()
        return res.with_answers().get(pk=id)

    # best questions
    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset().order_by_popularity().with_date_greater(week_ago)

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    objects = QuestionManager()

    class Meta:
        ordering = ['-date']

    def get_url(self):
        return reverse('question', kwargs={'id': self.id})

class QuestionLikeManager(models.Manager):
    # adds a condition: with question
    def has_question(self, question):
        return self.filter(question=question)

    # returns likes count (sum) for a question
    def sum_for_question(self, question):
        return self.has_question(question).aggregate(sum=Sum('value'))['sum']

    # add like if not exists
    def add_or_update(self, author, question, value):
        obj, new = self.update_or_create(
                author=author,
                question=question,
                defaults={'value': value}
                )

        question.likes = self.sum_for_question(question)
        question.save()
        return new

class QuestionLike(models.Model):
    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)

    objects = QuestionLikeManager()

class AnswerQuerySet(models.QuerySet):
    # loads author
    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    # loads question
    def with_question(self):
        return self.select_related('question')

    # order by popularity
    def order_by_popularity(self):
        return self.order_by('-likes')

    # filter by date
    def with_date_greater(self, date):
        return self.filter(date__gt=date)

class AnswerManager(models.Manager):
    # custom query set
    def get_queryset(self):
        res = AnswerQuerySet(self.model, using=self._db)
        return res.with_author()

    # create
    def create(self, **kwargs):
        ans = super(AnswerManager, self).create(**kwargs);
        
        text = ans.text[:100]
        if len(ans.text) > 100:
            text += '...'

        helpers.comet_send_message(
                helpers.comet_channel_id_question(ans.question),
                u'New Answer (' + ans.author.last_name + ' ' + ans.author.first_name + '): ' + text 
                )
        return ans

    # best answers
    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset().order_by_popularity().with_date_greater(week_ago)

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    objects = AnswerManager()

    class Meta:
        ordering = ['-correct', '-date', '-likes']

class AnswerLikeManager(models.Manager):
	# adds a condition: with answer
    def has_answer(self, answer):
        return self.filter(answer=answer)

    # returns likes count (sum) for an answer
    def sum_for_answer(self, answer):
        return self.has_answer(answer).aggregate(sum=Sum('value'))['sum']

    # adds a like if not exists
    def add_or_update(self, author, answer, value):
        obj, new = self.update_or_create(
                author=author,
                answer=answer,
                defaults={'value': value}
                )

        answer.likes = self.sum_for_answer(answer)
        answer.save()
        return new


class AnswerLike(models.Model):
	UP = 1
	DOWN = -1

	answer = models.ForeignKey(Answer)
	author = models.ForeignKey(User)
	value = models.SmallIntegerField(default=1)

	objects = AnswerLikeManager()