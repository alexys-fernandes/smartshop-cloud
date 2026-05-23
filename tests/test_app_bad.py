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
    """
    Este teste simula um erro lógico forçando uma asserção falsa.
    Como a SmartShopCloud calcula o total corretamente, o pytest
    irá falhar neste assert, derrubando o pipeline.
    """
    cart = SmartShopCart()
    # Adiciona R$ 150.00 em produtos
    cart.adicionar_produto("Monitor Gamer", 150.00, 1)
    
    # FORÇA A FALHA: Compara 150.00 com um valor errado (999.99)
    assert cart.calcular_total() == 999.99
