"""
Script para crear categorías iniciales en Nails Marketplace
Ejecutar: python manage.py shell < create_categories.py
O copiar y pegar en: python manage.py shell
"""

from apps.products.models import Category

# Definición de categorías con emojis para hacerlo más visual
categories_data = [
    {
        'name': 'Esmaltes y Lacas',
        'slug': 'esmaltes-lacas',
        'description': 'Esmaltes tradicionales, semipermanentes, en gel, vinílicos. Todas las marcas y colores.',
    },
    {
        'name': 'Sistemas de Uñas',
        'slug': 'sistemas-unas',
        'description': 'Acrílico, polygel, sistema ruso, tips, moldes y todo para construcción de uñas.',
    },
    {
        'name': 'Herramientas Básicas',
        'slug': 'herramientas-basicas',
        'description': 'Limas, cortaúñas, alicates, empujadores de cutícula, palitos de naranjo.',
    },
    {
        'name': 'Equipamiento Profesional',
        'slug': 'equipamiento-profesional',
        'description': 'Lámparas UV/LED, tornos, pulidoras, aspiradores de polvo, esterilizadores.',
    },
    {
        'name': 'Cuidado de Uñas',
        'slug': 'cuidado-unas',
        'description': 'Aceites de cutícula, cremas nutritivas, tratamientos fortalecedores, removedores.',
    },
    {
        'name': 'Arte y Decoración',
        'slug': 'arte-decoracion',
        'description': 'Stickers, calcomanías, strass, brillos, glitters, plantillas, accesorios 3D, foils.',
    },
    {
        'name': 'Preparación y Acabado',
        'slug': 'preparacion-acabado',
        'description': 'Primers, base coat, top coat, deshidratadores, limpiadores, buff, brillos finales.',
    },
    {
        'name': 'Pinceles y Aplicadores',
        'slug': 'pinceles-aplicadores',
        'description': 'Pinceles para arte, gel, acrílico. Dotting tools, esponjas, degradadores.',
    },
    {
        'name': 'Organización y Mobiliario',
        'slug': 'organizacion-mobiliario',
        'description': 'Exhibidores, organizadores, porta esmaltes, mesas, sillas, lámparas de trabajo.',
    },
    {
        'name': 'Insumos Sanitarios',
        'slug': 'insumos-sanitarios',
        'description': 'Desinfectantes, alcohol, guantes, barbijos, toallas desechables, papel camilla.',
    },
]

print("🎨 Iniciando creación de categorías para Nails Marketplace...\n")

created_count = 0
updated_count = 0
skipped_count = 0

for cat_data in categories_data:
    try:
        # Intentar obtener o crear la categoría
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
            }
        )
        
        if created:
            print(f"✅ Creada: {category.name}")
            created_count += 1
        else:
            # Si ya existe, actualizar descripción por si cambió
            if category.description != cat_data['description']:
                category.description = cat_data['description']
                category.save()
                print(f"🔄 Actualizada: {category.name}")
                updated_count += 1
            else:
                print(f"⏭️  Ya existe: {category.name}")
                skipped_count += 1
                
    except Exception as e:
        print(f"❌ Error con '{cat_data['name']}': {e}")

print("\n" + "="*60)
print("📊 Resumen:")
print(f"   ✅ Creadas: {created_count}")
print(f"   🔄 Actualizadas: {updated_count}")
print(f"   ⏭️  Omitidas: {skipped_count}")
print(f"   📦 Total en BD: {Category.objects.count()}")
print("="*60)
print("\n🎉 ¡Listo! Categorías configuradas para Nails Marketplace")
print("💅 Tu marketplace está listo para recibir productos\n")