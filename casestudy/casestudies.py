from collections import namedtuple


from django.contrib.staticfiles.storage import staticfiles_storage


Casestudy = namedtuple('Casestudy', ['title', 'description', 'image_url'])

HELLO_BABY = Casestudy(
    title="Hello Baby's rapid online growth",
    description=(
        'Hello Baby is an online nursery business that gets more than half '
        'its profits from exporting through online marketplaces such as '
        'Amazon, eBay and Cdiscount.'
    ),
    image_url=staticfiles_storage.url('images/stories/hellobaby.jpg'),
)

MARKETPLACE = Casestudy(
    title="Online marketplaces propel FreestyleXtreme",
    description=(
        'Like many businesses, Bristol-based specialist sports retailer '
        'FreestyleXtreme has seen big growth through online sales overseas.'
    ),
    image_url=staticfiles_storage.url('images/stories/freestylextreme.jpg'),
)

YORK = Casestudy(
    title="York bag retailer goes global via e-commerce",
    description=(
        'York-based retailer Maxwell Scott Bags was already selling '
        'internationally from its UK website when its owners made the '
        'decision to launch a German website.'
    ),
    image_url=staticfiles_storage.url('images/stories/maxwellscottbags.jpg'),
)
