from core.models import Cart


def cart_context_processor(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
    else:
        cart = None

    return {'cart': cart}
