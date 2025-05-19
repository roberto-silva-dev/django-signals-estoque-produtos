# Sistema de Gerenciamento de Pedidos - Django

## 1️⃣ Criação do Projeto
```bash
django-admin startproject core .
# OU
# python -m django startproject core .
python manage.py startapp produtos
python manage.py startapp pedidos
```

Adicione as apps no `settings.py`:
```python
INSTALLED_APPS = [
    ...,
    'produtos',
    'pedidos',
]

# Nesse trecho apenas adicione 'core/templates' na lista de DIRS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['core/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

```

## 2️⃣ Modelos (models.py)
**produtos/models.py**
```python
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    estoque = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - Estoque: {self.estoque}"
```

**pedidos/models.py**
```python
from django.db import models
from produtos.models import Produto

class Pedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.quantidade}x {self.produto.nome}"
```

## 3️⃣ Forms
**produtos/forms.py**
```python
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'estoque']
```

**pedidos/forms.py**
```python
from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['produto', 'quantidade']
```

## 4️⃣ Signal para atualizar estoque
**pedidos/signals.py**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido
from produtos.models import Produto

@receiver(post_save, sender=Pedido)
def atualizar_estoque(sender, instance, created, **kwargs):
    if created:
        produto = instance.produto
        produto.estoque -= instance.quantidade
        produto.save()
        print(f"Estoque atualizado para o produto {produto.nome}: {produto.estoque}")
```

**pedidos/apps.py** (registrar o signal)
```python
from django.apps import AppConfig

class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedidos'

    def ready(self):
        import pedidos.signals
```

## 5️⃣ Views
**produtos/views.py**
```python
from django.shortcuts import render, redirect
from .models import Produto
from .forms import ProdutoForm

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar.html', {'form': form})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista.html', {'produtos': produtos})
```

**pedidos/views.py**
```python
from django.shortcuts import render, redirect
from .models import Pedido
from .forms import PedidoForm

def cadastrar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/cadastrar.html', {'form': form})

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})
```

## 6️⃣ Templates
**base.html**
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="/">Gestão de Pedidos</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/produtos/">Produtos</a>
                <a class="nav-link" href="/pedidos/">Pedidos</a>
            </div>
        </div>
    </nav>
    <div class="container mt-5">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**produtos/cadastrar.html**
```html
{% extends 'base.html' %}
{% block content %}
    <h2>Cadastrar produto</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Salvar</button>
    </form>
{% endblock %}
```

**pedidos/cadastrar.html**
```html
{% extends 'base.html' %}
{% block content %}
    <h2>Cadastrar pedido</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Salvar Pedido</button>
    </form>
{% endblock %}
```

## 7️⃣ URLs
**core/urls.py**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produtos/', include('produtos.urls')),
    path('pedidos/', include('pedidos.urls')),
]
```

**produtos/urls.py**
```python
from django.urls import path
from .views import cadastrar_produto, lista_produtos

urlpatterns = [
    path('cadastrar/', cadastrar_produto, name='cadastrar_produto'),
    path('', lista_produtos, name='lista_produtos'),
]
```

**pedidos/urls.py**
```python
from django.urls import path
from .views import cadastrar_pedido, lista_pedidos

urlpatterns = [
    path('cadastrar/', cadastrar_pedido, name='cadastrar_pedido'),
    path('', lista_pedidos, name='lista_pedidos'),
]
```

## 8️⃣ Finalizando
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Testes
Acesse `/produtos/` para cadastrar produtos e `/pedidos/` para realizar pedidos e ver a atualização do estoque em tempo real!