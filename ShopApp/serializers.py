from rest_framework import serializers
from .models import Category, Product, ProductImg,ImgConnector,Tag,TagConnector,Color,Size,Material,Attribute
from Accounts.models import User




# task assing by shahin bhai
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=20)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class ProductImgSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    mainimage = serializers.ImageField()

    def create(self, validated_data):
        print("rrrrrrrrrrrrrrrrrrrrrrrrr",validated_data.get("mainimage"))
        return ProductImg.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mainimage = validated_data.get('mainimage', instance.mainimage)
        instance.save()
        return instance



class ImgConnectorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.IntegerField(required=False, allow_null=True)
    user = serializers.IntegerField(required=False, allow_null=True)
    mainimage = serializers.IntegerField()

    def create(self, validated_data):
        return ImgConnector.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.user = validated_data.get('user', instance.user)
        instance.mainimage = validated_data.get('mainimage', instance.mainimage)
        instance.save()
        return instance


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class TagConnectorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.IntegerField()
    tag = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        return TagConnector.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        return instance


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=264)
    category = serializers.SlugRelatedField(queryset=Category.objects.filter(), slug_field='title', allow_null=True)
    preview_text = serializers.CharField(max_length=200)
    detail_text = serializers.CharField(max_length=1000)
    slug = serializers.SlugField(read_only=True)
    tags = TagSerializer(many=True, required=False)
    images = ProductImgSerializer(many=True, required=False)

    #tags = serializers.ListField(child=serializers.CharField(max_length=255),write_only=True)



    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            TagConnector.objects.create(tag=tag, product=product)
        for image_data in images_data:
            image = ProductImg.objects.create(**image_data)
            ImgConnector.objects.create(product=product, image=image)
        return product
        #return validated_data

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        tags_data = validated_data.pop('tags', [])
        images_data = validated_data.pop('images', [])
        instance.name = validated_data.get('name', instance.name)
        instance.preview_text = validated_data.get('preview_text', instance.preview_text)
        instance.detail_text = validated_data.get('detail_text', instance.detail_text)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.category.title = category_data.get('title', instance.category.title)
        instance.category.save()
        instance.save()
        
        #Update or create tag connectors
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            try:
                tag_connector = TagConnector.objects.get(product=instance, tag=tag)
                tag_connector.save()
            except TagConnector.DoesNotExist:
                TagConnector.objects.create(product=instance, tag=tag)

        # Update or create image connectors
        for image_data in images_data:
            image_id = image_data.pop('id', None)
            image, created = ProductImg.objects.get_or_create(id=image_id, defaults=image_data)
            try:
                img_connector = ImgConnector.objects.get(product=instance, image=image)
                img_connector.save()
            except ImgConnector.DoesNotExist:
                ImgConnector.objects.create(product=instance, image=image)

        return instance

        

        


#Product Variations

class ColorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Color.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class SizeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Size.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class MaterialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Material.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance



class AttributeSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    color = ColorSerializer(required=False)
    size = SizeSerializer(required=False)
    material = MaterialSerializer(required=False)
    # tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Attribute
        fields = ['id', 'color', 'size', 'material', 'price', 'discount_percentage','product']

    def create(self, validated_data):
        product_data = validated_data.pop('product',None)
        color_data = validated_data.pop('color', None)
        size_data = validated_data.pop('size', None)
        material_data = validated_data.pop('material', None)

        # tags_data = validated_data.pop('tags', [])

        attribute = Attribute.objects.create(**validated_data)

        if product_data:
            product, created = Product.objects.get_or_create(**product_data)
            attribute.product = product

        if color_data:
            color, created = Color.objects.get_or_create(**color_data)
            attribute.color = color

        if size_data:
            size, created = Size.objects.get_or_create(**size_data)
            attribute.size = size

        if material_data:
            material, created = Material.objects.get_or_create(**material_data)
            attribute.material = material

        attribute.save()
        return attribute

    




