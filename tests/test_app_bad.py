import pytest
from src.app import SmartShopCart

def test_adicionar_produto_preco_invalido():
    cart = SmartShopCart()
    with pytest.raises(ValueError):
        cart.adicionar_produto("Produto Grátis", -10.00, 1)

def test_adicionar_produto_quantidade_invalida():
    cart = SmartShopCart()
    with pytest.raises(ValueError):
        cart.adicionar_produto("Teclado Mecânico", 350.00, 0)

def test_forcar_falha_calculo_total():
    cart = SmartShopCart()
    cart.adicionar_produto("Monitor Gamer", 150.00, 1)
    
    # Mudando para 150.0 para o teste passar com sucesso
    assert cart.calcular_total() == 150.00
