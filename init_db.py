from app import create_app
from app.models import Category, Product

app = create_app()
app.app_context().push()

# 清空数据库
Category.objects.delete()
Product.objects.delete()

# 添加示例数据
cat1 = Category(name='Art & Collectibles')
cat2 = Category(name='Jewellery')

prod1 = Product(name='Custom Portrait', attributes='Faceless portrait, custom illustration', quantity=10, price=20.00, image_url='https://example.com/image1.jpg', seller='Seller1', category=cat1)
prod2 = Product(name='Handmade Necklace', attributes='Beautiful handmade necklace', quantity=5, price=15.00, image_url='https://example.com/image2.jpg', seller='Seller2', category=cat2)

cat1.save()
cat2.save()
prod1.save()
prod2.save()

cat1.products.append(prod1)
cat2.products.append(prod2)
cat1.save()
cat2.save()
