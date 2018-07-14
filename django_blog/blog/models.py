from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField

# 创建分类class
class Category(models.Model):
    #分类的名称
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


# 创建标签class
class Tag(models.Model):
    #标签的名称
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


# 创建文章lass
class Post(models.Model):
    #文章的名称
    title = models.CharField(max_length = 70)

    #文章正文
    # body = models.TextField()
    body  = UEditorField(verbose_name=u'作品正文',width=800, height=600, imagePath="ueditor/imgage/",filePath="ueditor/files/", default='')

    #文章创建的时间
    created_time = models.DateTimeField()
    #文章修改的时间
    modified_time = models.DateTimeField()

    #文章的摘要-允许空值
    excerpt = models.CharField(max_length = 200, blank = True)

    #文章分类
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #文章标签-允许空值
    tags = models.ForeignKey(Tag, blank = True, on_delete=models.CASCADE)

    #文章作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #文章图片
    image = models.ImageField(default='default.jpg', upload_to='images/')

    #文章阅读量
    views = models.PositiveIntegerField(default=0)

    #返回文章标题
    def __str__(self):
        return self.title

    #自动生成文章摘要
    def short_text(self):
        return self.body[:60] + '...'

    #文章阅读数自增
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})