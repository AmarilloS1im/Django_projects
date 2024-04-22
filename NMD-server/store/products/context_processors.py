from products.models import *
def footer_context(request):
    return {'footer_info': '127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».',
            'footer_info_2':'Копирование материалов запрещено.'}
def sizes(request):
    sizes = Size.objects.all()
    return {'sizes':sizes}
def filter_data(request):
    categories = ProductCategory.objects.all()
    products_types = ProductType.objects.all()
    genders = ProductGender.objects.all()
    ages = ProductAge.objects.all()
    seasons = ProductSeason.objects.all()
    return {'categories': categories,'product_types': products_types,'genders': genders,
           'ages': ages,'seasons': seasons}


