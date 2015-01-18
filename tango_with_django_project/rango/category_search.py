from rango.models import Category

def get_category_list(max_results=0, starts_with=""):
    results = []
    if starts_with:
        results = Category.objects.filter(name__istartswith=starts_with)

    if max_results <= 0:
        return []
    else:
        if max_results < len(results):
            return results[:max_results]
        else:
            return results