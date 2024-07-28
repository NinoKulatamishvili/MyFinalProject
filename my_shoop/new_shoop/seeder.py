from .models import Categories, Gender


def seeder_func():
    category_name = ['Drees', 'Trouser', 'Skirt', 'Jeans', 'Jacket', 'Blazer', 'Sneakers']
    category = ['Women', "Men", 'Kids']

    for category_name in category_name:
        if not Categories.objects.filter( category_name=category_name):
            new_category_name = Categories( category_name=category_name)
            new_category_name.save()

    for category in category:
        if not Gender.objects.filter(category=category):
            new_category = Gender(category=category)
            new_category.save()