from django.db.models.signals import post_save
from django.dispatch import receiver
from pedidos.models import Pedido

@receiver(post_save, sender=Pedido)
def atualizar_estoque(sender, instance, created, **kwargs):
    if created:
        produto = instance.produto
        produto.estoque -= instance.quantidade
        produto.save()
        print(f"Estoque atualizado para o produto {produto.nome}: {produto.estoque}")
