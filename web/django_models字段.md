# Django Model 定义语法

(https://www.jianshu.com/u/cf5d0e67d416)

# Django Model 定义语法

> 版本：1.7
> 主要来源：[https://docs.djangoproject.com/en/1.7/topics/db/models/](https://link.jianshu.com/?t=https://docs.djangoproject.com/en/1.7/topics/db/models/)

## 简单用法

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

```

会自动生成SQL：

```
CREATE TABLE myapp_person (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);

```

> 

-默认会根据APP的名称生成"app名称"+"_"+"类名"
-会自动增加ID字段
-Django会根据settings配置中指定的数据库类型来生成相应的SQL语句

## 使用Model

要想使用Model需要在settings配置中INSTALLED_APPS中增加你的APP，例如，你的models在myapp.models中，那么就应该使用:

```
INSTALLED_APPS = (
    #...
    'myapp',
    #...
)

```

> 在将app添加到INSTALLD_APPS中后需要执行manage.py migrate,也可通过manage.py makemigrations进行迁移。

## Fields

Django提供了各种数据字段类型。需要注意不要使用与API相冲突的字段名称如clean,save或delete

```
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

```

### Field types

django会根据field类型确定

- 数据库字段类型（如INTEGER,VARCHAR）
- 默认的HTML生成什么样的表单项
- 最低限度的验证需求。它被用在 Django 管理后台和自动生成的表单中。

field是可以自定义的。

### Field options

每个field类型都有自己特定的参数，但也有一些通用的参数，这些参数都是可选的：

#### null

如果为 True ， Django 在数据库中会将空值(empty)存储为 NULL 。默认为 False 。

#### blank

设置字段是否可以为空，默认为False（不允许为空）

> 和null的区别在于：null是数据库的范围，而blank是用于验证。如果一个字段的 blank=True ，Django 在进行表单数据验证时，会允许该字段是空值。如果字段的 blank=False ，该字段就是必填的。

#### choices

它是一个可迭代的二元组(例如，列表或是元组)，用来给字段提供选择项。如果设置了 choices， Django会显示选择框，而不是标准的文本框，而且这个选择框的选项就是 choices 中的元组。

```
YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
)

```

每个元组中的第一个元素，是存储在数据库中的值；第二个元素是在管理界面或 ModelChoiceField 中用作显示的内容。在一个给定的 model 类的实例中，想得到某个 choices 字 段的显示值，就调用 get_FOO_display 方法(这里的 FOO 就是 choices 字段的名称 )。

```
from django.db import models

class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
u'L'
>>> p.get_shirt_size_display()
u'Large'

```

#### default

默认值，可以是一个具体的值也可以是一个对象，每次调用次会创建一个新的对象

#### help_text

附加的帮助信息。在使用表单时会显示在字段下面。即使不使用表单也可以起来帮助文档的作用。

#### primary_key

如果为True,则表示这个字段是主键。

如果你没有设置主键，Django会自动创建一个自增的IntergerField类型主键，可以通过自定义主键来覆盖默认的行为。

#### unique

如果为 True ，那么字段值就必须是全表唯一的。

------

## Automatic primary key fields

默认情况下，Django 会给每个 model 添加下面这个字段:

```
id = models.AutoField(primary_key=True)

```

这是一个自增主键字段。

如果你想指定一个自定义主键字段，只要在某个字段上指定 primary_key=True 即可。如果 Django 看到你显式地设置了 Field.primary_key，就不会自动添加 id 列。

每个 model 只要有一个字段指定 primary_key=True 就可以了。（可以自定义也可以保持默认自动增加的主键）

------

## Verbose field names（详细名称）

每个字段的类型，除了ForeignKey, ManyToManyField 和 OneToOneField外，还有一个可选的第一位置参数，这个参数用于标记字段的详细名称。如果Verbose field names没有显示的给出，Django会自动创建这一字段属性，将字段名中的"_"转换成空格。

例如：设置详细名称为 "person's first name":

```
first_name = models.CharField("person's first name", max_length=30)

```

如果没有设置详细名称，则详细名称为： "first name":

```
first_name = models.CharField(max_length=30)

```

由于ForeignKey, ManyToManyField和 OneToOneField
需要使用第一参数，所以可以显示的使用 verbose_name来设置详细名称：

```
poll = models.ForeignKey(Poll, verbose_name="the related poll")
sites = models.ManyToManyField(Site, verbose_name="list of sites")
place = models.OneToOneField(Place, verbose_name="related place")

```

仅在以上特列中使用verbose_name，Django会自动利用第一个参数。

## Relationships（关系）

Django支持关系数据库中常用的many-to-one,many-tomany,one-to-one

### Many-to-one(多对一关系)

定义Many-to-one关系，使用django.db.models.ForeignKey。使用方法和其他字段类型一样：在model中定义时包含ForeignKey属性。

ForeignKey必须要一个参数：需要链接到哪个model.

例如：一辆汽车（car）和汽车制造商(manufacturer)的关系，那么一个汽车制造商会有制造多辆车，但每辆车却只能有一个汽车制造商：

```
from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)

```

你也可以定义一个递归的关系（在对象内容实部Many-to-one的定义）和relationships to models not yet defined（没看明白，看完模型关系后再修改）;

建议但不强制要求ForeignKey字段的名字是模型的小写字母的名字(例如在上例中使用的manufacturer)。当然你可以使用任何你想要的名字，例如：

```
class Car(models.Model):
    company_that_makes_it = models.ForeignKey(Manufacturer)

```

### Many-to-many(多对多关系)

定义Many-to-many关系，使用django.db.models.ManyToManyField.使用方法和其他字段类型一样：在model中定义包含ManyToManyField属性。

ManyToManyField必须要一个参数：需要链接到那个model.

例如，一个Pizza有多个Topping对象——也就是一个Topping可以在多个Pizza上，每个Pizza有多个Toppings——这种情况我们可以这样定义：

```
from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)

```

和ForeignKey一样，可以创建递归关系（在对象内部实现Many-to-many的定义）和relationships to models not yet defined

建议但不强制要求ManyToManyField的名字(上面的例子中的toppings)是复数形式，复数形式是为了描述相关模型对象的集合。

哪个模型带有ManyToManyField都没关系，但你只能在其中一个模型中使用它，而不能在两个模型中都使用它。

一般来说，ManyToManyField实例应该包含在使用表单编辑的对象中，在上面的例子中，toppings在Pizza中(而不是Topping有pizzas ManyToManyField)，因为一个pizzas有多个Topping，比一个Topping在多个pizzas上更容易让人理解。这就是上面我们使用的方式，Pizza管理表单将让用户选择那种Topping。

还有一些可选参数。

#### Many-to-many关系的额外字段

如果只需要处理简单的多对多关系，就像上面pizzas和topping的关系，那么ManyToManyField字段就可以满足需要，然而，有些时候你需要让数据在两个模型之间产生联系。

例如，考虑一下跟踪乐队和乐队拥有的音乐家的应用程序的例子。这是一个人和这个人所在团队之间的多对多关系，因此你可以使用ManyToManyField来描述这个关系。然而，这种成员关系有很多你想要搜集的细节，比如这个人加入团队的时间。

对于这种情况，Django让你可以指定用来管理多对多关系的模型。然后你可以在中间模型中放入额外的字段。中间模型使用through参数指向像中间人一样工作的模型，来和ManyToManyField发生关系。对于四个音乐家的例子，代码可能像这样子：

```
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

```

当你建立中间模型时，你需要为模型明确地指定外键，以建立多对多关系。这个明确的声明定义了两个模型是如何产生联系的。

> 对于中间模型，有一些限制：

> 中间模型必须包含并且只包含一个到目标模型的外键(在上面的例子中的Group)。或者使用ManyToManyField.through_fields来明确指定外键关系。如果你有多个外键，但没有指定through_fields,会产生校验错误。类似的限制适用于外键的目标model(例如Person)

> 对于一个model通过中间model实现多对多关系，两个到同一模型的外键是允许的，但会被认为是多对多关系的两个不同侧面。如果有两个或以上的外键定义，你必须要定义through_fields,否则会产生校验错误。

> 当使用中间模型来定义一个到自己的多对多关系的模型时，你必须使用symmetrical=False(参阅“模型字段参考”)。

现在你已经建立了ManyToManyField来使用中间模型(在这个例子中是MemberShip)，你可以开始创建一些多对多的对应关系了。具体来说是创建中间模型的一些实例：

现在已经在中间model中设置了ManyToManyField（例子中的Membership）,你可以通过中间model创建关系实例：

```
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason="Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
[<Person: Ringo Starr>]
>>> ringo.group_set.all()
[<Group: The Beatles>]
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason="Wanted to form a band.")
>>> beatles.members.all()
[<Person: Ringo Starr>, <Person: Paul McCartney>]

```

不同于一般的many-to-many关系字段，你不能通过直接通过关系对象进行增加、创建或赋值（即：beatles.members = [...]）

```
# THIS WILL NOT WORK
>>> beatles.members.add(john)
# NEITHER WILL THIS
>>> beatles.members.create(name="George Harrison")
# AND NEITHER WILL THIS
>>> beatles.members = [john, paul, ringo, george]

```

这是因为你需要知道一些Person和Group关系之外的一些细节，这些细节在中间model--Membership中定义，而不仅仅只是简单创建了Person和Group之间的关系。类似关系的唯一解决办法是创建中间model

基于同样的原因 remove() 也是被禁用的，但可以通过 clear() 清除所有多对多关系实例：

```
>>> # Beatles have broken up
>>> beatles.members.clear()
>>> # Note that this deletes the intermediate model instances
>>> Membership.objects.all()
[]

```

一旦创建了中间model实例，并建立了一个多对多关系实例，就可以和正常的多对多关系一样进行查询：

```
# Find all the groups with a member whose name starts with 'Paul'
>>> Group.objects.filter(members__name__startswith='Paul')
[<Group: The Beatles>]

```

因为你正在使用中间模型，你也可以使用它的属性来进行查询：

```
# Find all the members of the Beatles that joined after 1 Jan 1961
>>> Person.objects.filter(
...     group__name='The Beatles',
...     membership__date_joined__gt=date(1961,1,1))
[<Person: Ringo Starr]

```

如果你需要访问membership’s 信息，你可以这样做直接查询Membership:

```
>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
u'Needed a new drummer.'

```

当然你也可以通过多对多的反向关系从Person 实例进行查询：

```
>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
u'Needed a new drummer.'

```

### One-to-one关系

要定义一对一关系，请使用OneToOneField。它的使用方法和其它字段一样：把它包含在模型的类属性中。

当对象以某种方式扩展了另一个对象的主键时，对象的主键是最重要的。

OneToOneField要求一个位置参数：该模型相关的类。

例如，如果你将创建一个数据表places，你可能会在数据表中建立一些相当标准的东西，就像地址、电话号码等等。然后，如果你想在places上建立一个饭馆，你可以不必重复劳动，在Restaurant模型中复制这些字段，你可以建立一个带有到Place的OneToOneField(因为饭馆就是一个place；实际上，对于这种情况典型的做法是使用继承，这实际上是一种隐式的一对一关系)。

和外键一样，你可以定义循环关系和到未定义模型的关系；

OneToOneField也接受一个可选的参数parent_link 这个参数在“模型字段参考”有介绍。

OneToOneField类曾经会自动成为模型的主键。现在情况不再如此了(如果你愿意你可以手动传递一个primary_key参数)。因此，现在一个模型可以拥有多个OneToOneField类型的字段。

### Models across files（跨文件的model）

在当前model和另一个应用程序中的model建立关系是没有问题的，只需要引入相关的model，然后在需要的时候使用就可以了:

```
from django.db import models
from geography.models import ZipCode

class Restaurant(models.Model):
    # ...
    zip_code = models.ForeignKey(ZipCode)

```

### Field name restrictions（字段名限制 ）

Django对字段名只有两个限制：

1. 字段名不能是Python的保留关键字，不然会导致Python语法错误。例如：

   class Example(models.Model):
   pass = models.IntegerField() # 'pass' is a reserved word!

2. 字段名在一行中不能包含一个以上的下划线，这和Django的搜索查询语法的工作方式有关。例如：

   class Example(models.Model):
   foo__bar = models.IntegerField() # 'foo__bar' has two underscores!

这些限制是可以绕过的，因为你的字段名并不需要和数据表的列名匹配。

SQL保留字，比如join、where或select，可以用作模型字段名，因为Django在进行底层的SQL查询前会对所有数据表名和列名进行转义。

### Custom field types（自定义字段类型）

如果现有的字段类型不能满足你的需要，或者你使用的数据库具有一些特殊的类型，你可以创建自己字段类型。

## Meta options

定义model的metadata(元数据)是通过使用一个内部类Meta，例：

```
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"

```

model元数据不是一个字段，例如ordering，db_table，verbose_name 和 verbose_name_plural这些附加选项，都可以放到class Meta中，这些选项都不是必需的。

## Model attributes

### objects

这是model最重要的Manager属性，通过它查询数据库并于model之间形成映射。如果没有自定义manager，默认名称为objects。managers只能通过model类，而不能通过model类实例来访问。

## Model methods

通过model自定义方法添加自定义"行级"功能，而managers方法是为“表级”添加自定义功能，model自定义方法可以通过model实例来使用。

这样就可以把业务逻辑都放在一个model里。例如:

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

```

上个实例的最后一个方法是属性。

这个model实例继承自models.Model，会自动具备大量的方法，可以覆盖大部分的方法，但有几个却是必须的：

#### **str**() (Python 3)

在Python3中相当于**unicode**()

#### **unicode**() (Python 2)

这是一个Python的"魔术方法"，它以unicode方式返回任何对象的陈述。Python和Django需要输出字符串陈述时使用。例如在交互式控制台或管理后台显示的输出陈述。

默认的实现并不能很好的满足需要，所以最好自定义这个方法，

#### get_absolute_url()

定义对象的URL.在管理界面中，任何时候都可以通过URL找到一个对象。

任何通过URL访问的对象，都应该有唯一标识。

## Overriding predefined model methods

还有一些model方法封装了一些行为。当你想自定义数据库行为，尤其是想改变save() 和 delete()方式的时候。

你可以自由地重写这些方法来改变行为。

如果你想在保存对象的时候，覆盖内置save() 行为：

```
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        do_something()
        super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
        do_something_else()

```

你也可以阻止保存：

```
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        if self.name == "Yoko Ono's blog":
            return # Yoko shall never have her own blog!
        else:
            super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.

```

需要特别注意的要记得调用父类的方法--super(Blog, self).save(*args, **kwargs)，以确保对象仍然被保存到数据库中，如果你忘记调用父类的方法，默认的行为不会发生，数据库也不会发生改变。

随着时间的推移，django会增加或扩展一些新的方法，如果你使用*args, **kwargs作为你的方法参数，就必须要保证能正确处理这些参数的增加。

> 覆盖方法大多数不会用于批量操作
>
> delete()并不一定是在调用一个QuerySet批量删除时被触发。为了确保自定义的删除逻辑被执行，则需要使用 pre_delete and/or post_delete 信号。

> 不幸的是，还没有一个好的方法用于批量的创建和更新，因为没有save()、pre_save、post_save会被调用。

### Executing custom SQL

另外一种常见的模式是在model方法和module-level方法中执行自定义SQL。

### Model inheritance（Model继承）

Model的继承和普通的Python类继承几乎相同，但基类的继承必须是django.db.models.Model.

在Django中有三种继承风格：

1、如果你想用父类来保存每个子类共有的信息，并且这个类是不会被独立使用的，那么应该使用抽象基类。

2、如果你继承现有model(甚至可能这个类是在另一个应用程序中)，并希望每个model都拥有自己对应的数据库，那就应该使用多表继承。

3、如果你只是想修改model的Python-level行为，而不改变models fields，则使用代理模式。

#### Abstract base classes

当你想集中一些公共信息，可以使用虚类。你需要在model的元数据中设置 abstract=True ，这个model将不会被用于创建任何数据表。相反，当他被作为其他子类的基类时，他的字段将被添加到这些子类中。如果抽象类和他的子类有相同名称的字段会产生一个异常。

例如：

```
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

```

Student会拥有三个字段：name\age\home_group。CommonInfo将不能像普通的Django model一样使用，因为他是一个抽象基类。他不会产生一个数据表或者拥有一个管理器，也不能被实例化或直接调用。

在许多情况下这种类型的继承正是你想要的，它提供了一种用来分解公共信息的方法，虽然只能实现数据表级别创建子模型。

#### Meta inheritance

当创建一个抽象基类的时候，Django允许在基类中声明各种Meta属性，如果子类没有声明自己的Meta元数据，他将继承父类的。如果子类想扩展父类的Meta元数据，则可以继承父类的Meta。例如：

```
from django.db import models

class CommonInfo(models.Model):
    # ...
    class Meta:
        abstract = True
        ordering = ['name']

class Student(CommonInfo):
    # ...
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'

```

Django对于抽象基类的元数据调整只应该在安装之前设置abstract=false。这意味着从抽象基类派生的子类不会自动转型成抽象类本身。当然你也可以继承来自别一个抽象基类。只需要记住abstract=True每次都应该明确设置。（这段没怎么看明白）

在抽象基类中某些属性几乎是没有任何意义的，包括父类的元数据。例如使用db_table将意味着所有的子类（那些没有指定自己的Meta）将使用同一数据库，这肯定不会是你想要的。

#### Be careful with related_name(注意抽象基类中的反向关系名称定义)

如果你在ForeignKey和ManyToManyField的属性中使用related_name,你必须为字段指定一个唯一反向关系名称。在抽象基类中会有一些问题，因为抽象基类的每个字段都会被包括在他的每一个子类中，包括related_name.

要解决这个问题，应该在抽象基类中使用related_name时，名称中应包含'%(app_label)s' 和 '%(class)s'.

> '%(class)s':小写的子类名称
> '%(app_label)s'：应用的小写名称（app）。因为每个已安装的应用名称都是唯一的，所以产生的名称最终也会不同。

例如：首先定义common/models.py:

```
from django.db import models

class Base(models.Model):
    m2m = models.ManyToManyField(OtherModel, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True

class ChildA(Base):
    pass

class ChildB(Base):
    pass

```

然后另一个APP rare/models.py:

```
from common.models import Base

class ChildB(Base):
    pass

```

在这个示例中 common.ChildA.m2m 字段的反向关系名称是common_childa_related,而common.ChildB.m2m 的关系名称ommon_childb_related。这是因为使用了'%(app_label)s' 和 '%(class)s'产生了不同的反向关系名称。如果你定义了related_name,但忘记了使用'%(app_label)s' 和 '%(class)s' Django会系统检查或运行migrate时引发错误。

如果没有在抽象基类的字段中定义related_name属性，默认关系名称将是子类名称+"_set"。通常related_name会被直接在子类的字段属性中被定义。例如上例中，如果related_name属性被省略。common.ChildA.m2m 的反向关系名称应该是childa_set，common.ChildB.m2m的反向关系名称应该是childb_set。

### Multi-table inheritance（多表继承）

Django支持的第二种model继承是多表继承，在继承结构中每个model都是独立的。都对应着自己的数据库表，可以进行独立的查询等操作。继承关系实际是子model和每个父model之间的关系(通过自动创建OneToOneField)。例如：

```
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

```

所有Place的字段都可以在Restaurant中使用，虽然数据存放在不同的数据表中。所以可以如下使用：

```
>>> Place.objects.filter(name="Bob's Cafe")
>>> Restaurant.objects.filter(name="Bob's Cafe")

```

如果一个Place对象存在相应的Restaurant对象，那么就可以使用Place对象通过关系获得Restaurant对象：

```
>>> p = Place.objects.get(id=12)
# If p is a Restaurant object, this will give the child class:
>>> p.restaurant
<Restaurant: ...>

```

但如果place对象所对应的Restaurant对象不存在，则会引发 Restaurant.DoesNotExist 异常。

#### Meta and multi-table inheritance

在多表继承的情况下继承父类的Meta是没有意义的。所有的Meta都已经被应用到父类，再应用这些Meta只会导致矛盾。

所以子model不能访问到父model的Meta，然而也有少数的情况下，子model会从父model中继承一些行为，例如子model没有指定 ordering或 get_latest_by属性，那么就会从父model中继承。

如果父model中有一个排序，但你不希望子model有任何的排序规划，你可以明确的禁用：

```
class ChildModel(ParentModel):
    # ...
    class Meta:
        # Remove parent's ordering effect
        ordering = []

```

#### Inheritance and reverse relations（继承与反向关系）

因为多表继承实际是隐式的使用OneToOneField来键接父Model和子model,在这种关系有可能会使用父model来调用子model，比如上面的例子。但是如果你把ForeignKey和ManyToManyField关系应用到这样一个继承关系中，Django会返回一个验证错误，必须要指定一个related_name字段属性。

例如上面的例子，我们再创建一个子类，其中包含一个到父model的ManyToManyField关系字段：

```
class Supplier(Place):
    customers = models.ManyToManyField(Place)

```

这时会产生一个错误：

```
Reverse query name for 'Supplier.customers' clashes with reverse query
name for 'Supplier.place_ptr'.

HINT: Add or change a related_name argument to the definition for
'Supplier.customers' or 'Supplier.place_ptr'.

```

解决这个问题只需要在customers字段属性中增加related_name属性：models.ManyToManyField(Place, related_name='provider').

#### Specifying the parent link field

如上所述，Django会自动创建一个OneToOneField链接你的子model和任何非抽象父model。如果你想自定义子model键接回父model的属性名称，你可以创建自己的OneToOneField并设置parent_link=True，表示这个字段是对父model的回链。

### Proxy models

当使用多表继承时一个新的数据表model会在每一个子类中创建，这是因为子model需要存储父mdoel不存在的一些数据字段。但有时只需要改变model的操作行为，可能是为了改变默认的管理行为或添加新的方法。

这时就应该使用代理模式的继承：创建原始model的代理。你可以创建一个用于 create, delete 和 update的代理model,使用代理model的时候数据将会真实保存。这和使用原始model是一样的，所不同的是当你改变model操作时，不需要去更改原始的model。

代理模式的声明和正常的继承声明方式一样。你只需要在Meta class 中定义proxy为True就可以了。

例如，你想为Person model添加一个方法：

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass

```

MyPerson这个类将作用于父类Person所对应的真实数据表。可通过MyPerson进行所有相应的操作：

```
>>> p = Person.objects.create(first_name="foobar")
>>> MyPerson.objects.get(first_name="foobar")
<MyPerson: foobar>

```

你也可以使用代理模式来定义model的不同默认排序，例如：

```
class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True

```

这样当使用原始model查询时结果是无序的，而使用OrderedPerson进行查询时将按last_name进行排序。

#### QuerySets still return the model that was requested（QuerySets的类型依然会是原始model类型）

当你通过MyPerson来查询Person对象时，返回的QuerySet依然会是Person对象类型的集合。使用代理模式的model是依靠原始model的,是原始model的扩展。而不是用来替代父model。

#### Base class restrictions（基类限制）

代理model必须继承一个非抽像model。

不能从多个非抽像model继承，代理模式不能为不同model之间创建链接。

代理模式可以从任意没有定义字段的抽象model继承。

#### Proxy model managers

如果没有指定代理model的管理器(managers)，它将继承父类的管理行为。如果你定义了代理model的管理器,它将会成为默认的，当然父类中定义的定义的任何管理器仍然是可以使用的。

继续上面的例了，增加一个默认的管理器：

```
from django.db import models

class NewManager(models.Manager):
    # ...
    pass

class MyPerson(Person):
    objects = NewManager()

    class Meta:
        proxy = True

```

可以通过创建一个含有新的管理器并进行继承，来增加一个新的管理器，而不需要去改变更有的默认管理器。

```
# Create an abstract class for the new manager.
class ExtraManagers(models.Model):
    secondary = NewManager()

    class Meta:
        abstract = True

class MyPerson(Person, ExtraManagers):
    class Meta:
        proxy = True

```

#### Differences between proxy inheritance and unmanaged models

代理model看起来很像一个在Meta class中设置了manged的非托管模式model。但实际上这两种方案是不太一样，应该考虑在不同的情况下使用那一个：

两者区别在于：你可以设置model的Meta.managed=False以及通过Meta.db_table指定数据表有创建非托管模式model,并对其添加各种方法，但如果你可保持非托管模式和真实数据表之间的同步，做任何更改都将是很麻烦的事。

而代理model主要用于管理model的各种行为或方法，他们将继承父model的管理器等。

曾经尝试将两种模式合并，但由于API会变得非常复杂，并且难以理解，所以现在是分离成两种模式：

一般的使用规划是：

1、如果正使用现有的数据表，但不想在Django中镜像所有的列，所以应该使用Meta.managed=False，通过这个选项使不在django控制下的数据表或视图是可用的。

2、如果你想改变一个model的操作行为，但希望保持原始model不被改变，就应该使用Meta.proxy=True.

### Multiple inheritance(多重继承)

和Python的继承方式一样，django中的model也可以从多个父model继承，当然也和Python的继承方式 一样，如果出现相同名字的时候只有第一个将被使用。例如：如果多个父model中都包含Meta类，将只有第一个将被使用，其他会被忽略。

通常情况下是不会用到多重继承的。主是用于“混合式”model:增加一个特殊的额外字段或方式是由多个父model组合而来。应该尽量保持继承层次的简单，不然会很难排查某个信息是从那里来的。

在django1.7以前，多个父model中有id主键字段时虽然不会引发错误，但有可能导致数据的丢失。例如像下面的model:

```
class Article(models.Model):
    headline = models.CharField(max_length=50)
    body = models.TextField()

class Book(models.Model):
    title = models.CharField(max_length=50)

class BookReview(Book, Article):
    pass

```

下面的使用方法演示了怎么用一个子对象来覆盖父对象的值：

```
>>> article = Article.objects.create(headline='Some piece of news.')
>>> review = BookReview.objects.create(
...     headline='Review of Little Red Riding Hood.',
...     title='Little Red Riding Hood')
>>>
>>> assert Article.objects.get(pk=article.pk).headline == article.headline
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AssertionError
>>> # the "Some piece of news." headline has been overwritten.
>>> Article.objects.get(pk=article.pk).headline
'Review of Little Red Riding Hood.'

```

要正确的使用多重继承，你应该使用一个明确的 AutoField 在父model中：

```
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    ...

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    ...

class BookReview(Book, Article):
    pass

```

或者使用一个共同的父类来定义AutoField:

```
class Piece(models.Model):
    pass

class Article(Piece):
    ...

class Book(Piece):
    ...

class BookReview(Book, Article):
    pass

```

#### Field name “hiding” is not permitted

正常的Python类继承，允许一个子类覆盖父类的任何属性。在Django中是不允许覆盖父类的属性字段的。如果一个父类中定义了一个叫author的字段，你就不能在子model中创建别一个叫author的字段。

这种限制仅适用于字段（field），普通的python属性是可以的。也有一种情况是可以覆盖的:多表继承的时候进行手动指定数据库列名，可以出现子model和父model有同名的字段名称，因为他们属于不同的数据表。

如果你覆盖了父model的字段属性，django会抛出FieldError异常。