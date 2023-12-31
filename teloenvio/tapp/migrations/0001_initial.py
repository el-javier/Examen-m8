# Generated by Django 4.2.3 on 2023-07-11 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fono', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254)),
                ('nombre', models.CharField(max_length=100)),
                ('identificador', models.CharField(max_length=20)),
                ('numIdentificador', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Productor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreContacto', models.CharField(max_length=100)),
                ('RUT', models.CharField(max_length=12)),
                ('razonSocial', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('comuna', models.CharField(max_length=100)),
                ('rubro', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcionProducto', models.CharField(max_length=255)),
                ('precioProducto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('imagenProducto', models.ImageField(upload_to='productos/')),
                ('stockProducto', models.IntegerField()),
                ('idProductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tapp.productor')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('numero_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('direccion_entrega', models.CharField(max_length=255)),
                ('cantidades', models.CharField(max_length=255)),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('forma_pago', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('PR', 'En preparación'), ('D', 'En despacho'), ('E', 'Entregado')], default='P', max_length=2)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tapp.cliente')),
                ('productos', models.ManyToManyField(through='tapp.DetallePedido', to='tapp.producto')),
            ],
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tapp.pedido'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tapp.producto'),
        ),
    ]
