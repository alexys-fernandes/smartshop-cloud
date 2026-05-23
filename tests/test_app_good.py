import pytest
from src.app import SmartShopCart

def test_adicionar_produto_sucesso():
    cart = SmartShopCart()
    assert cart.adicionar_produto("Camiseta Cloud", 89.90, 2) is True
    assert "Camiseta Cloud" in cart.items

def test_calcular_total_com_desconto():
    cart = SmartShopCart()
    cart.adicionar_produto("Servidor Dedicado Virtual", 600.00, 1)
    # 600 * 0.90 = 540.00
    assert cart.calcular_total() == 540.00

def test_esvaziar_carrinho():
    cart = SmartShopCart()
    cart.adicionar_produto("Caneca Dev", 25.00, 1)
    cart.esvaziar_carrinho()
    assert len(cart.items) == 0
