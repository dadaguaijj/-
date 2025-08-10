from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username



# 基础房源模型（所有城市的表结构一致，继承此类）
class BaseHouseModel(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    image_url = models.URLField(verbose_name="图片链接", null=True, blank=True)
    pattern = models.CharField(max_length=50, verbose_name="格局")
    area = models.FloatField(verbose_name="面积（m²）")
    orientation = models.CharField(max_length=20, verbose_name="房屋朝向")
    community = models.CharField(max_length=100, verbose_name="小区名称")
    total_price = models.FloatField(verbose_name="总价（万元）")
    avg_price = models.FloatField(verbose_name="均价（元/平）")
    home_url = models.URLField(verbose_name="主页链接", null=True, blank=True)
    tags = models.CharField(max_length=255, verbose_name="标签", null=True, blank=True)
    has_elevator = models.CharField(max_length=5, verbose_name="是否有电梯")
    city = models.CharField(max_length=20, verbose_name="城市")

    class Meta:
        abstract = True  # 抽象基类，不生成实际表，仅用于继承


# 各城市的模型（继承基础类，指定对应的数据表名）
class GuangzhouHouse(BaseHouseModel):
    class Meta:
        db_table = 'gz_house'  # 对应MySQL中的gz_house表
        verbose_name = "广州房源"
        verbose_name_plural = verbose_name


class FoshanHouse(BaseHouseModel):
    class Meta:
        db_table = 'fs_house'  # 对应MySQL中的fs_house表
        verbose_name = "佛山房源"
        verbose_name_plural = verbose_name


class DongguanHouse(BaseHouseModel):
    class Meta:
        db_table = 'dg_house'  # 对应MySQL中的dg_house表
        verbose_name = "东莞房源"
        verbose_name_plural = verbose_name


# 依次定义其他城市的模型（按相同格式）
class HuizhouHouse(BaseHouseModel):
    class Meta:
        db_table = 'hz_house'
        verbose_name = "惠州房源"
        verbose_name_plural = verbose_name


class JiangmenHouse(BaseHouseModel):
    class Meta:
        db_table = 'jm_house'
        verbose_name = "江门房源"
        verbose_name_plural = verbose_name


class QingyuanHouse(BaseHouseModel):
    class Meta:
        db_table = 'qy_house'
        verbose_name = "清远房源"
        verbose_name_plural = verbose_name


class ShenzhenHouse(BaseHouseModel):
    class Meta:
        db_table = 'sz_house'
        verbose_name = "深圳房源"
        verbose_name_plural = verbose_name


class ZhanjiangHouse(BaseHouseModel):
    class Meta:
        db_table = 'zj_house'
        verbose_name = "湛江房源"
        verbose_name_plural = verbose_name


class ZhongshanHouse(BaseHouseModel):
    class Meta:
        db_table = 'zs_house'
        verbose_name = "中山房源"
        verbose_name_plural = verbose_name


class ZhuhaiHouse(BaseHouseModel):
    class Meta:
        db_table = 'zh_house'
        verbose_name = "珠海房源"
        verbose_name_plural = verbose_name

class GuangDongHouse(BaseHouseModel):
    class Meta:
        db_table = 'gd_house'
        verbose_name = "全部房源"
        verbose_name_plural = verbose_name


# 用户收藏模型
class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    house_id = models.IntegerField(verbose_name="房源ID")
    city = models.CharField(max_length=20, verbose_name="城市")
    house_title = models.CharField(max_length=255, verbose_name="房源标题")
    house_price = models.FloatField(verbose_name="房源价格")
    house_image = models.URLField(verbose_name="房源图片", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")
    
    class Meta:
        db_table = 'user_favorites'
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'house_id', 'city')  # 防止重复收藏
    
    def __str__(self):
        return f"{self.user.username} - {self.house_title}"