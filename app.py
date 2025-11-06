from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import GestorRestaurante

app = Flask(__name__)
app.secret_key = 'restaurante_secret_key'

# Instancia del gestor del restaurante
gestor = GestorRestaurante()

# Datos de ejemplo
def cargar_datos_ejemplo():
    """Carga algunos platos de ejemplo"""
    if not gestor.listar_platos():
        gestor.agregar_plato("Pizza Margherita", "Pizza clásica con tomate, mozzarella y albahaca", 12.99, "Principal", 20)
        gestor.agregar_plato("Hamburguesa Clásica", "Carne de res, lechuga, tomate y queso cheddar", 10.50, "Principal", 15)
        gestor.agregar_plato("Ensalada César", "Lechuga romana, crutones, parmesano y aderezo césar", 8.75, "Ensaladas", 10)
        gestor.agregar_plato("Tiramisú", "Postre italiano clásico con café y cacao", 6.25, "Postres", 5)
        gestor.agregar_plato("Sopa del Día", "Sopa casera preparada diariamente", 5.99, "Entradas", 8)

# Rutas principales
@app.route('/')
def index():
    """Página principal del restaurante"""
    return render_template('index.html')

@app.route('/menu')
def ver_menu():
    """Muestra el menú completo"""
    platos = gestor.listar_platos()
    categorias = set(plato.categoria for plato in platos)
    
    categoria_seleccionada = request.args.get('categoria', '')
    if categoria_seleccionada:
        platos = gestor.buscar_platos_por_categoria(categoria_seleccionada)
    
    return render_template('menu.html', 
                         platos=platos, 
                         categorias=categorias, 
                         categoria_seleccionada=categoria_seleccionada)

# Rutas CRUD para platos
@app.route('/platos/agregar', methods=['GET', 'POST'])
def agregar_plato():
    """Agrega un nuevo plato al menú"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        tiempo_preparacion = int(request.form['tiempo_preparacion'])
        
        gestor.agregar_plato(nombre, descripcion, precio, categoria, tiempo_preparacion)
        flash('Plato agregado exitosamente!', 'success')
        return redirect(url_for('ver_menu'))
    
    return render_template('agregar_plato.html')

@app.route('/platos/editar/<int:plato_id>', methods=['GET', 'POST'])
def editar_plato(plato_id):
    """Edita un plato existente"""
    plato = gestor.buscar_plato_por_id(plato_id)
    
    if not plato:
        flash('Plato no encontrado', 'error')
        return redirect(url_for('ver_menu'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        tiempo_preparacion = int(request.form['tiempo_preparacion'])
        disponible = 'disponible' in request.form
        
        gestor.actualizar_plato(plato_id, 
                               nombre=nombre, 
                               descripcion=descripcion, 
                               precio=precio, 
                               categoria=categoria, 
                               tiempo_preparacion=tiempo_preparacion,
                               disponible=disponible)
        
        flash('Plato actualizado exitosamente!', 'success')
        return redirect(url_for('ver_menu'))
    
    return render_template('editar_plato.html', plato=plato)

@app.route('/platos/eliminar/<int:plato_id>', methods=['GET', 'POST'])
def eliminar_plato(plato_id):
    """Elimina un plato del menú"""
    plato = gestor.buscar_plato_por_id(plato_id)
    
    if not plato:
        flash('Plato no encontrado', 'error')
        return redirect(url_for('ver_menu'))
    
    if request.method == 'POST':
        gestor.eliminar_plato(plato_id)
        flash('Plato eliminado exitosamente!', 'success')
        return redirect(url_for('ver_menu'))
    
    return render_template('eliminar_plato.html', plato=plato)

@app.route('/platos/toggle_disponible/<int:plato_id>')
def toggle_disponible_plato(plato_id):
    """Cambia la disponibilidad de un plato"""
    plato = gestor.buscar_plato_por_id(plato_id)
    
    if plato:
        nuevo_estado = not plato.disponible
        gestor.cambiar_disponibilidad_plato(plato_id, nuevo_estado)
        estado = "disponible" if nuevo_estado else "no disponible"
        flash(f'Plato marcado como {estado}!', 'success')
    
    return redirect(url_for('ver_menu'))

# API endpoints
@app.route('/api/platos')
def api_platos():
    """Endpoint API para obtener todos los platos en JSON"""
    platos = [plato.to_dict() for plato in gestor.listar_platos()]
    return jsonify(platos)

@app.route('/api/platos/<int:plato_id>')
def api_plato(plato_id):
    """Endpoint API para obtener un plato específico en JSON"""
    plato = gestor.buscar_plato_por_id(plato_id)
    if plato:
        return jsonify(plato.to_dict())
    return jsonify({'error': 'Plato no encontrado'}), 404

if __name__ == '__main__':
    cargar_datos_ejemplo()
    app.run(debug=True, port=5000)
    