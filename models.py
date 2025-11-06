from datetime import datetime

class Plato:
    """Clase que representa un plato del menú del restaurante"""
    
    # Variable de clase para almacenar todos los platos
    platos = []
    # Contador para IDs automáticos
    contador_id = 1
    
    def __init__(self, nombre, descripcion, precio, categoria, disponible=True, tiempo_preparacion=30):
        self.id = Plato.contador_id
        Plato.contador_id += 1
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.disponible = disponible
        self.tiempo_preparacion = tiempo_preparacion
        self.fecha_creacion = datetime.now()
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    def to_dict(self):
        """Convierte el objeto plato a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'categoria': self.categoria,
            'disponible': self.disponible,
            'tiempo_preparacion': self.tiempo_preparacion,
            'fecha_creacion': self.fecha_creacion.strftime("%Y-%m-%d %H:%M")
        }
    
    @classmethod
    def crear_plato(cls, nombre, descripcion, precio, categoria, tiempo_preparacion=30):
        """Método de clase para crear un nuevo plato"""
        nuevo_plato = cls(nombre, descripcion, precio, categoria, True, tiempo_preparacion)
        cls.platos.append(nuevo_plato)
        return nuevo_plato
    
    @classmethod
    def obtener_plato_por_id(cls, plato_id):
        """Método de clase para buscar un plato por ID"""
        for plato in cls.platos:
            if plato.id == plato_id:
                return plato
        return None
    
    @classmethod
    def obtener_todos_platos(cls):
        """Método de clase para obtener todos los platos"""
        return cls.platos
    
    @classmethod
    def obtener_platos_por_categoria(cls, categoria):
        """Método de clase para filtrar platos por categoría"""
        return [plato for plato in cls.platos if plato.categoria.lower() == categoria.lower()]
    
    @classmethod
    def actualizar_plato(cls, plato_id, **kwargs):
        """Método de clase para actualizar un plato"""
        plato = cls.obtener_plato_por_id(plato_id)
        if plato:
            for key, value in kwargs.items():
                if hasattr(plato, key):
                    setattr(plato, key, value)
            return plato
        return None
    
    @classmethod
    def eliminar_plato(cls, plato_id):
        """Método de clase para eliminar un plato"""
        plato = cls.obtener_plato_por_id(plato_id)
        if plato:
            cls.platos.remove(plato)
            return True
        return False


class Pedido:
    """Clase que representa un pedido del restaurante"""
    
    pedidos = []
    contador_id = 1
    
    def __init__(self, mesa, platos):
        self.id = Pedido.contador_id
        Pedido.contador_id += 1
        self.mesa = mesa
        self.platos = platos  # Lista de objetos Plato
        self.estado = "pendiente"  # pendiente, en_preparacion, listo, entregado
        self.total = sum(plato.precio for plato in platos)
        self.fecha_creacion = datetime.now()
    
    def calcular_total(self):
        """Calcula el total del pedido"""
        self.total = sum(plato.precio for plato in self.platos)
        return self.total
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del pedido"""
        self.estado = nuevo_estado


class GestorRestaurante:
    """Clase para gestionar las operaciones del restaurante"""
    
    def __init__(self):
        self.platos = Plato.obtener_todos_platos()
        self.pedidos = Pedido.pedidos
    
    # Métodos para gestión de platos
    def agregar_plato(self, nombre, descripcion, precio, categoria, tiempo_preparacion=30):
        """Agrega un nuevo plato al menú"""
        return Plato.crear_plato(nombre, descripcion, precio, categoria, tiempo_preparacion)
    
    def listar_platos(self):
        """Retorna todos los platos"""
        return self.platos
    
    def buscar_plato_por_id(self, plato_id):
        """Busca un plato por su ID"""
        return Plato.obtener_plato_por_id(plato_id)
    
    def buscar_platos_por_categoria(self, categoria):
        """Busca platos por categoría"""
        return Plato.obtener_platos_por_categoria(categoria)
    
    def actualizar_plato(self, plato_id, **kwargs):
        """Actualiza un plato existente"""
        return Plato.actualizar_plato(plato_id, **kwargs)
    
    def eliminar_plato(self, plato_id):
        """Elimina un plato del menú"""
        return Plato.eliminar_plato(plato_id)
    
    def cambiar_disponibilidad_plato(self, plato_id, disponible):
        """Cambia la disponibilidad de un plato"""
        plato = self.buscar_plato_por_id(plato_id)
        if plato:
            plato.disponible = disponible
            return plato
        return None
    
    # Métodos para gestión de pedidos
    def crear_pedido(self, mesa, platos_ids):
        """Crea un nuevo pedido"""
        platos = [self.buscar_plato_por_id(pid) for pid in platos_ids]
        platos = [p for p in platos if p is not None and p.disponible]
        
        if platos:
            nuevo_pedido = Pedido(mesa, platos)
            self.pedidos.append(nuevo_pedido)
            return nuevo_pedido
        return None
    
    def listar_pedidos(self):
        """Retorna todos los pedidos"""
        return self.pedidos
    