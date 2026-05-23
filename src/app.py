class SmartShopCart:
    def __init__(self):
        self.items = {}

    def adicionar_produto(self, nome_produto: str, preco: float, quantidade: int = 1):
        if preco <= 0:
            raise ValueError("O preço do produto deve ser maior que zero.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser de pelo menos 1 item.")
        
        if nome_produto in self.items:
            self.items[nome_produto]['quantidade'] += quantidade
        else:
            self.items[nome_produto] = {'preco': preco, 'quantidade': quantidade}
        return True

    def calcular_total(self) -> float:
        total = 0.0
        for item in self.items.values():
            total += item['preco'] * item['quantidade']
        
        if total > 500.0:
            total = total * 0.90
        return round(total, 2)

    def esvaziar_carrinho(self):
        self.items.clear()
        return True
