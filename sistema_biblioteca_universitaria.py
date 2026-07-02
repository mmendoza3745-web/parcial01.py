
"""
================================================================================
SISTEMA DE GESTIÓN DE BIBLIOTECA UNIVERSITARIA
Parcial - Programación Orientada a Objetos (Python)
IDAT - Escuela de Tecnología
================================================================================

TEMAS INTEGRADOS:
- POO: Clases, Encapsulamiento, Herencia, Polimorfismo, Abstracción
- Constructores y Destructores
- Manejo de Excepciones
- Funciones y Métodos
- Listas, Tuplas, Diccionarios
- Matrices (listas anidadas)
- Recursividad
- Manejo de Cadenas (Strings)
- Operadores Lógicos
- Validaciones

AUTOR: Estudiante IDAT
FECHA: 2026
================================================================================
"""

import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ============================================================================
# CAPA DE EXCEPCIONES PERSONALIZADAS
# ============================================================================

class BibliotecaException(Exception):
    """Excepción base para errores del sistema de biblioteca."""
    pass

class LibroNoDisponibleError(BibliotecaException):
    """Se lanza cuando un libro no está disponible para préstamo."""
    pass

class UsuarioNoEncontradoError(BibliotecaException):
    """Se lanza cuando no se encuentra un usuario/miembro."""
    pass

class LibroNoEncontradoError(BibliotecaException):
    """Se lanza cuando no se encuentra un libro."""
    pass

class ValidacionError(BibliotecaException):
    """Se lanza cuando falla una validación de datos."""
    pass

class MembresiaExpiradaError(BibliotecaException):
    """Se lanza cuando la membresía del usuario ha expirado."""
    pass


# ============================================================================
# CLASE ABSTRACTA BASE (ABSTRACCIÓN)
# ============================================================================

class EntidadBiblioteca(ABC):
    """
    Clase abstracta base que define el contrato para todas las entidades
    del sistema de biblioteca. Implementa el principio de ABSTRACCIÓN.
    """

    @abstractmethod
    def obtener_id(self):
        """Retorna el identificador único de la entidad."""
        pass

    @abstractmethod
    def mostrar_info(self):
        """Muestra la información completa de la entidad."""
        pass

    @abstractmethod
    def to_dict(self):
        """Convierte la entidad a un diccionario."""
        pass


# ============================================================================
# CLASE LIBRO (ENCAPSULAMIENTO COMPLETO)
# ============================================================================

class Libro(EntidadBiblioteca):
    """
    Clase que representa un libro en la biblioteca.
    Implementa ENCAPSULAMIENTO con atributos privados.
    """

    # Contador estático para generar IDs automáticos
    _contador_libros = 0

    def __init__(self, titulo, autor, isbn, anio_publicacion, categoria, 
                 editorial="Desconocida", copias=1):
        """
        CONSTRUCTOR: Inicializa un objeto Libro con valores predeterminados
        o suministrados.
        """
        Libro._contador_libros += 1
        self.__id_libro = f"LIB-{Libro._contador_libros:04d}"
        self.__titulo = titulo.strip().title()
        self.__autor = autor.strip().title()
        self.__isbn = isbn.strip()
        self.__anio_publicacion = anio_publicacion
        self.__categoria = categoria.strip().title()
        self.__editorial = editorial.strip().title()
        self.__copias_total = copias
        self.__copias_disponibles = copias
        self.__estado = "Disponible"  # Disponible, Prestado, Reservado
        self.__prestamos_realizados = 0
        self.__fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[+] Libro creado: {self.__titulo} (ID: {self.__id_libro})")

    # ==================== DESTRUCTOR ====================
    def __del__(self):
        """DESTRUCTOR: Se ejecuta al eliminar el objeto."""
        print(f"[-] Libro eliminado: {self.__titulo} (ID: {self.__id_libro})")

    # ==================== GETTERS (property) ====================
    @property
    def id_libro(self):
        return self.__id_libro

    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def isbn(self):
        return self.__isbn

    @property
    def anio_publicacion(self):
        return self.__anio_publicacion

    @property
    def categoria(self):
        return self.__categoria

    @property
    def editorial(self):
        return self.__editorial

    @property
    def copias_total(self):
        return self.__copias_total

    @property
    def copias_disponibles(self):
        return self.__copias_disponibles

    @property
    def estado(self):
        return self.__estado

    @property
    def prestamos_realizados(self):
        return self.__prestamos_realizados

    # ==================== SETTERS ====================
    @titulo.setter
    def titulo(self, valor):
        if not valor or not valor.strip():
            raise ValidacionError("El título no puede estar vacío.")
        self.__titulo = valor.strip().title()

    @autor.setter
    def autor(self, valor):
        if not valor or not valor.strip():
            raise ValidacionError("El autor no puede estar vacío.")
        self.__autor = valor.strip().title()

    @isbn.setter
    def isbn(self, valor):
        if not self._validar_isbn(valor):
            raise ValidacionError("ISBN inválido. Debe tener 10 o 13 dígitos.")
        self.__isbn = valor.strip()

    @anio_publicacion.setter
    def anio_publicacion(self, valor):
        anio_actual = datetime.now().year
        if not (1000 <= valor <= anio_actual):
            raise ValidacionError(f"Año inválido. Debe estar entre 1000 y {anio_actual}.")
        self.__anio_publicacion = valor

    @categoria.setter
    def categoria(self, valor):
        self.__categoria = valor.strip().title()

    @editorial.setter
    def editorial(self, valor):
        self.__editorial = valor.strip().title()

    @copias_total.setter
    def copias_total(self, valor):
        if valor < 1:
            raise ValidacionError("Debe haber al menos 1 copia.")
        self.__copias_total = valor

    # ==================== MÉTODOS DE NEGOCIO ====================

    def _validar_isbn(self, isbn):
        """Valida que el ISBN tenga 10 o 13 caracteres numéricos."""
        isbn_limpio = isbn.replace("-", "").replace(" ", "")
        return len(isbn_limpio) in [10, 13] and isbn_limpio.isdigit()

    def prestar(self):
        """Reduce las copias disponibles y actualiza el estado."""
        if self.__copias_disponibles <= 0:
            raise LibroNoDisponibleError(
                f"El libro '{self.__titulo}' no tiene copias disponibles."
            )
        self.__copias_disponibles -= 1
        self.__prestamos_realizados += 1
        if self.__copias_disponibles == 0:
            self.__estado = "Prestado"
        return True

    def devolver(self):
        """Aumenta las copias disponibles y actualiza el estado."""
        if self.__copias_disponibles >= self.__copias_total:
            raise ValidacionError("No se pueden devolver más copias de las existentes.")
        self.__copias_disponibles += 1
        self.__estado = "Disponible"
        return True

    def agregar_copias(self, cantidad):
        """Agrega copias adicionales al libro."""
        if cantidad <= 0:
            raise ValidacionError("La cantidad debe ser mayor a 0.")
        self.__copias_total += cantidad
        self.__copias_disponibles += cantidad
        print(f"[+] Se agregaron {cantidad} copias de '{self.__titulo}'.")

    # ==================== MÉTODOS ABSTRACTOS IMPLEMENTADOS ====================

    def obtener_id(self):
        return self.__id_libro

    def mostrar_info(self):
        print(f"\n{'='*50}")
        print(f"  📚 LIBRO: {self.__titulo}")
        print(f"{'='*50}")
        print(f"  ID:              {self.__id_libro}")
        print(f"  Autor:           {self.__autor}")
        print(f"  ISBN:            {self.__isbn}")
        print(f"  Año:             {self.__anio_publicacion}")
        print(f"  Categoría:       {self.__categoria}")
        print(f"  Editorial:       {self.__editorial}")
        print(f"  Copias Total:    {self.__copias_total}")
        print(f"  Copias Disp.:    {self.__copias_disponibles}")
        print(f"  Estado:          {self.__estado}")
        print(f"  Préstamos:       {self.__prestamos_realizados}")
        print(f"  Registrado:      {self.__fecha_registro}")
        print(f"{'='*50}\n")

    def to_dict(self):
        return {
            "id_libro": self.__id_libro,
            "titulo": self.__titulo,
            "autor": self.__autor,
            "isbn": self.__isbn,
            "anio_publicacion": self.__anio_publicacion,
            "categoria": self.__categoria,
            "editorial": self.__editorial,
            "copias_total": self.__copias_total,
            "copias_disponibles": self.__copias_disponibles,
            "estado": self.__estado,
            "prestamos_realizados": self.__prestamos_realizados,
            "fecha_registro": self.__fecha_registro
        }

    def __str__(self):
        return f"[{self.__id_libro}] {self.__titulo} - {self.__autor} ({self.__estado})"

    def __repr__(self):
        return self.__str__()


# ============================================================================
# CLASE MIEMBRO (HERENCIA DE ENTIDAD BIBLIOTECA)
# ============================================================================

class Miembro(EntidadBiblioteca):
    """
    Clase que representa un miembro/usuario de la biblioteca.
    Implementa ENCAPSULAMIENTO y HERENCIA.
    """

    _contador_miembros = 0

    def __init__(self, nombres, apellidos, dni, email, telefono="", 
                 tipo_membresia="Estándar"):
        Miembro._contador_miembros += 1
        self.__id_miembro = f"MEM-{Miembro._contador_miembros:04d}"
        self.__nombres = nombres.strip().title()
        self.__apellidos = apellidos.strip().title()
        self.__dni = dni.strip()
        self.__email = email.strip().lower()
        self.__telefono = telefono.strip()
        self.__tipo_membresia = tipo_membresia.strip().title()
        self.__fecha_registro = datetime.now()
        self.__fecha_expiracion = self.__fecha_registro + timedelta(days=365)
        self.__libros_prestados = []  # Lista de IDs de libros prestados
        self.__historial_prestamos = []  # Lista de diccionarios
        self.__penalizaciones = 0
        self.__activo = True

        print(f"[+] Miembro registrado: {self.__nombres} {self.__apellidos} (ID: {self.__id_miembro})")

    def __del__(self):
        print(f"[-] Miembro eliminado: {self.__nombres} {self.__apellidos}")

    # ==================== GETTERS ====================
    @property
    def id_miembro(self):
        return self.__id_miembro

    @property
    def nombres(self):
        return self.__nombres

    @property
    def apellidos(self):
        return self.__apellidos

    @property
    def dni(self):
        return self.__dni

    @property
    def email(self):
        return self.__email

    @property
    def telefono(self):
        return self.__telefono

    @property
    def tipo_membresia(self):
        return self.__tipo_membresia

    @property
    def fecha_expiracion(self):
        return self.__fecha_expiracion.strftime("%Y-%m-%d")

    @property
    def libros_prestados(self):
        return tuple(self.__libros_prestados)  # Tupla inmutable

    @property
    def penalizaciones(self):
        return self.__penalizaciones

    @property
    def activo(self):
        return self.__activo

    # ==================== SETTERS ====================
    @nombres.setter
    def nombres(self, valor):
        self.__nombres = valor.strip().title()

    @apellidos.setter
    def apellidos(self, valor):
        self.__apellidos = valor.strip().title()

    @email.setter
    def email(self, valor):
        if "@" not in valor or "." not in valor:
            raise ValidacionError("Email inválido.")
        self.__email = valor.strip().lower()

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor.strip()

    @tipo_membresia.setter
    def tipo_membresia(self, valor):
        tipos_validos = ["Estándar", "Premium", "Estudiante", "Docente"]
        if valor.strip().title() not in tipos_validos:
            raise ValidacionError(f"Tipo inválido. Opciones: {', '.join(tipos_validos)}")
        self.__tipo_membresia = valor.strip().title()

    # ==================== MÉTODOS DE NEGOCIO ====================

    def verificar_membresia(self):
        """Verifica si la membresía está vigente."""
        if datetime.now() > self.__fecha_expiracion:
            self.__activo = False
            raise MembresiaExpiradaError(
                f"La membresía de {self.__nombres} ha expirado. Renueve su membresía."
            )
        return True

    def agregar_prestamo(self, id_libro, titulo_libro, fecha_devolucion):
        """Registra un préstamo en el historial del miembro."""
        self.__libros_prestados.append(id_libro)
        prestamo = {
            "id_libro": id_libro,
            "titulo": titulo_libro,
            "fecha_prestamo": datetime.now().strftime("%Y-%m-%d"),
            "fecha_devolucion": fecha_devolucion,
            "estado": "Activo"
        }
        self.__historial_prestamos.append(prestamo)

    def registrar_devolucion(self, id_libro):
        """Registra la devolución de un libro."""
        if id_libro in self.__libros_prestados:
            self.__libros_prestados.remove(id_libro)
            for p in self.__historial_prestamos:
                if p["id_libro"] == id_libro and p["estado"] == "Activo":
                    p["estado"] = "Devuelto"
                    p["fecha_devolucion_real"] = datetime.now().strftime("%Y-%m-%d")
                    # Verificar retraso
                    fecha_esperada = datetime.strptime(p["fecha_devolucion"], "%Y-%m-%d")
                    if datetime.now() > fecha_esperada:
                        dias_retraso = (datetime.now() - fecha_esperada).days
                        self.__penalizaciones += dias_retraso
                        print(f"[!] Devolución con retraso de {dias_retraso} días. Penalización aplicada.")
                    return True
        return False

    def renovar_membresia(self, dias=365):
        """Renueva la membresía por un período adicional."""
        self.__fecha_expiracion = datetime.now() + timedelta(days=dias)
        self.__activo = True
        print(f"[+] Membresía renovada hasta: {self.__fecha_expiracion.strftime('%Y-%m-%d')}")

    def obtener_historial(self):
        """Retorna el historial de préstamos como tupla."""
        return tuple(self.__historial_prestamos)

    # ==================== MÉTODOS ABSTRACTOS ====================

    def obtener_id(self):
        return self.__id_miembro

    def mostrar_info(self):
        estado_membresia = "Activa" if self.__activo else "Expirada"
        print(f"\n{'='*50}")
        print(f"  👤 MIEMBRO: {self.__nombres} {self.__apellidos}")
        print(f"{'='*50}")
        print(f"  ID:              {self.__id_miembro}")
        print(f"  DNI:             {self.__dni}")
        print(f"  Email:           {self.__email}")
        print(f"  Teléfono:        {self.__telefono}")
        print(f"  Membresía:       {self.__tipo_membresia}")
        print(f"  Estado:          {estado_membresia}")
        print(f"  Expira:          {self.__fecha_expiracion.strftime('%Y-%m-%d')}")
        print(f"  Libros actuales: {len(self.__libros_prestados)}")
        print(f"  Penalizaciones:  {self.__penalizaciones} días")
        print(f"  Total préstamos: {len(self.__historial_prestamos)}")
        print(f"{'='*50}\n")

    def to_dict(self):
        return {
            "id_miembro": self.__id_miembro,
            "nombres": self.__nombres,
            "apellidos": self.__apellidos,
            "dni": self.__dni,
            "email": self.__email,
            "telefono": self.__telefono,
            "tipo_membresia": self.__tipo_membresia,
            "fecha_expiracion": self.__fecha_expiracion.strftime("%Y-%m-%d"),
            "libros_prestados": list(self.__libros_prestados),
            "historial_prestamos": list(self.__historial_prestamos),
            "penalizaciones": self.__penalizaciones,
            "activo": self.__activo
        }

    def __str__(self):
        return f"[{self.__id_miembro}] {self.__nombres} {self.__apellidos} - {self.__tipo_membresia}"


# ============================================================================
# CLASE PRESTAMO (POLIMORFISMO CON ENTIDAD BIBLIOTECA)
# ============================================================================

class Prestamo(EntidadBiblioteca):
    """
    Clase que representa un préstamo de libro.
    Demuestra POLIMORFISMO al implementar los métodos abstractos.
    """

    _contador_prestamos = 0

    def __init__(self, id_libro, id_miembro, titulo_libro, nombre_miembro, 
                 dias_prestamo=14):
        Prestamo._contador_prestamos += 1
        self.__id_prestamo = f"PRE-{Prestamo._contador_prestamos:04d}"
        self.__id_libro = id_libro
        self.__id_miembro = id_miembro
        self.__titulo_libro = titulo_libro
        self.__nombre_miembro = nombre_miembro
        self.__fecha_prestamo = datetime.now()
        self.__fecha_devolucion = self.__fecha_prestamo + timedelta(days=dias_prestamo)
        self.__estado = "Activo"
        self.__dias_prestamo = dias_prestamo

        print(f"[+] Préstamo registrado: {self.__id_prestamo}")

    @property
    def id_prestamo(self):
        return self.__id_prestamo

    @property
    def estado(self):
        return self.__estado

    def finalizar(self):
        """Finaliza el préstamo."""
        self.__estado = "Finalizado"
        self.__fecha_devolucion_real = datetime.now()
        print(f"[+] Préstamo {self.__id_prestamo} finalizado.")

    def obtener_id(self):
        return self.__id_prestamo

    def mostrar_info(self):
        print(f"\n{'='*50}")
        print(f"  📋 PRÉSTAMO: {self.__id_prestamo}")
        print(f"{'='*50}")
        print(f"  Libro:     {self.__titulo_libro} ({self.__id_libro})")
        print(f"  Miembro:   {self.__nombre_miembro} ({self.__id_miembro})")
        print(f"  Fecha préstamo:   {self.__fecha_prestamo.strftime('%Y-%m-%d')}")
        print(f"  Fecha devolución: {self.__fecha_devolucion.strftime('%Y-%m-%d')}")
        print(f"  Estado:    {self.__estado}")
        print(f"{'='*50}\n")

    def to_dict(self):
        return {
            "id_prestamo": self.__id_prestamo,
            "id_libro": self.__id_libro,
            "id_miembro": self.__id_miembro,
            "titulo_libro": self.__titulo_libro,
            "nombre_miembro": self.__nombre_miembro,
            "fecha_prestamo": self.__fecha_prestamo.strftime("%Y-%m-%d"),
            "fecha_devolucion": self.__fecha_devolucion.strftime("%Y-%m-%d"),
            "estado": self.__estado
        }


# ============================================================================
# CLASE BIBLIOTECA (GESTOR PRINCIPAL - MATRICES Y DICCIONARIOS)
# ============================================================================

class Biblioteca:
    """
    Clase principal que gestiona toda la biblioteca.
    Utiliza DICCIONARIOS para almacenamiento rápido y MATRICES para reportes.
    """

    def __init__(self, nombre="Biblioteca Universitaria IDAT"):
        self.__nombre = nombre
        # DICCIONARIOS para acceso O(1)
        self.__libros = {}       # {id_libro: objeto Libro}
        self.__miembros = {}     # {id_miembro: objeto Miembro}
        self.__prestamos = {}    # {id_prestamo: objeto Prestamo}

        # MATRIZ para reporte de disponibilidad [fila=categoría, col=estado]
        self.__matriz_disponibilidad = []

        print(f"\n{'='*60}")
        print(f"  📚 {self.__nombre.upper()}")
        print(f"{'='*60}\n")

    # ==================== GESTIÓN DE LIBROS ====================

    def registrar_libro(self, titulo, autor, isbn, anio, categoria, 
                        editorial="Desconocida", copias=1):
        """Registra un nuevo libro en el sistema."""
        try:
            # Validaciones
            if not titulo or not titulo.strip():
                raise ValidacionError("El título es obligatorio.")
            if not autor or not autor.strip():
                raise ValidacionError("El autor es obligatorio.")
            if not isinstance(anio, int) or anio < 1000:
                raise ValidacionError("El año de publicación es inválido.")

            libro = Libro(titulo, autor, isbn, anio, categoria, editorial, copias)
            self.__libros[libro.id_libro] = libro
            self._actualizar_matriz_disponibilidad()
            return libro.id_libro

        except ValidacionError as e:
            print(f"[!] Error de validación: {e}")
            return None
        except Exception as e:
            print(f"[!] Error inesperado: {e}")
            return None

    def actualizar_libro(self, id_libro, **kwargs):
        """
        Actualiza información de un libro existente.
        Uso: actualizar_libro("LIB-0001", titulo="Nuevo Título", copias_total=5)
        """
        try:
            if id_libro not in self.__libros:
                raise LibroNoEncontradoError(f"Libro {id_libro} no encontrado.")

            libro = self.__libros[id_libro]
            campos_validos = ["titulo", "autor", "isbn", "anio_publicacion", 
                             "categoria", "editorial", "copias_total"]

            for campo, valor in kwargs.items():
                if campo in campos_validos:
                    setattr(libro, campo, valor)
                    print(f"[+] {campo} actualizado a: {valor}")
                else:
                    print(f"[!] Campo '{campo}' no reconocido.")

            self._actualizar_matriz_disponibilidad()
            return True

        except (LibroNoEncontradoError, ValidacionError) as e:
            print(f"[!] Error: {e}")
            return False

    def eliminar_libro(self, id_libro):
        """Elimina un libro del sistema."""
        try:
            if id_libro not in self.__libros:
                raise LibroNoEncontradoError(f"Libro {id_libro} no encontrado.")

            libro = self.__libros[id_libro]
            if libro.copias_disponibles < libro.copias_total:
                print(f"[!] No se puede eliminar: hay copias prestadas.")
                return False

            del self.__libros[id_libro]
            self._actualizar_matriz_disponibilidad()
            print(f"[+] Libro {id_libro} eliminado correctamente.")
            return True

        except LibroNoEncontradoError as e:
            print(f"[!] Error: {e}")
            return False

    def buscar_libro(self, criterio, valor):
        """
        Busca libros por criterio.
        criterio: "titulo", "autor", "categoria", "isbn"
        """
        resultados = []
        criterio = criterio.lower()

        for libro in self.__libros.values():
            if criterio == "titulo" and valor.lower() in libro.titulo.lower():
                resultados.append(libro)
            elif criterio == "autor" and valor.lower() in libro.autor.lower():
                resultados.append(libro)
            elif criterio == "categoria" and valor.lower() in libro.categoria.lower():
                resultados.append(libro)
            elif criterio == "isbn" and valor in libro.isbn:
                resultados.append(libro)

        return resultados

    def listar_libros(self):
        """Muestra todos los libros registrados."""
        if not self.__libros:
            print("[!] No hay libros registrados.")
            return

        print(f"\n{'='*60}")
        print(f"  📚 LISTADO DE LIBROS ({len(self.__libros)} registros)")
        print(f"{'='*60}")

        for libro in self.__libros.values():
            print(f"  {libro}")
        print(f"{'='*60}\n")

    # ==================== GESTIÓN DE MIEMBROS ====================

    def registrar_miembro(self, nombres, apellidos, dni, email, 
                          telefono="", tipo_membresia="Estándar"):
        """Registra un nuevo miembro."""
        try:
            if not nombres or not apellidos:
                raise ValidacionError("Nombres y apellidos son obligatorios.")
            if "@" not in email:
                raise ValidacionError("Email inválido.")

            miembro = Miembro(nombres, apellidos, dni, email, telefono, tipo_membresia)
            self.__miembros[miembro.id_miembro] = miembro
            return miembro.id_miembro

        except ValidacionError as e:
            print(f"[!] Error: {e}")
            return None

    def actualizar_miembro(self, id_miembro, **kwargs):
        """Actualiza información de un miembro."""
        try:
            if id_miembro not in self.__miembros:
                raise UsuarioNoEncontradoError(f"Miembro {id_miembro} no encontrado.")

            miembro = self.__miembros[id_miembro]
            campos_validos = ["nombres", "apellidos", "email", "telefono", "tipo_membresia"]

            for campo, valor in kwargs.items():
                if campo in campos_validos:
                    setattr(miembro, campo, valor)
                    print(f"[+] {campo} actualizado.")
            return True

        except (UsuarioNoEncontradoError, ValidacionError) as e:
            print(f"[!] Error: {e}")
            return False

    def renovar_membresia(self, id_miembro, dias=365):
        """Renueva la membresía de un miembro."""
        try:
            if id_miembro not in self.__miembros:
                raise UsuarioNoEncontradoError("Miembro no encontrado.")
            self.__miembros[id_miembro].renovar_membresia(dias)
            return True
        except UsuarioNoEncontradoError as e:
            print(f"[!] Error: {e}")
            return False

    def listar_miembros(self):
        """Muestra todos los miembros registrados."""
        if not self.__miembros:
            print("[!] No hay miembros registrados.")
            return

        print(f"\n{'='*60}")
        print(f"  👤 LISTADO DE MIEMBROS ({len(self.__miembros)} registros)")
        print(f"{'='*60}")
        for miembro in self.__miembros.values():
            print(f"  {miembro}")
        print(f"{'='*60}\n")

    # ==================== PRÉSTAMOS Y DEVOLUCIONES ====================

    def realizar_prestamo(self, id_libro, id_miembro, dias=14):
        """Realiza un préstamo de libro a un miembro."""
        try:
            # Validar existencia
            if id_libro not in self.__libros:
                raise LibroNoEncontradoError(f"Libro {id_libro} no encontrado.")
            if id_miembro not in self.__miembros:
                raise UsuarioNoEncontradoError(f"Miembro {id_miembro} no encontrado.")

            libro = self.__libros[id_libro]
            miembro = self.__miembros[id_miembro]

            # Validar membresía
            miembro.verificar_membresia()

            # Validar disponibilidad
            libro.prestar()

            # Crear préstamo
            fecha_dev = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")
            miembro.agregar_prestamo(id_libro, libro.titulo, fecha_dev)

            prestamo = Prestamo(id_libro, id_miembro, libro.titulo, 
                               f"{miembro.nombres} {miembro.apellidos}", dias)
            self.__prestamos[prestamo.id_prestamo] = prestamo

            self._actualizar_matriz_disponibilidad()
            print(f"[+] Préstamo exitoso. Devolver antes del: {fecha_dev}")
            return prestamo.id_prestamo

        except (LibroNoDisponibleError, UsuarioNoEncontradoError, 
                LibroNoEncontradoError, MembresiaExpiradaError, ValidacionError) as e:
            print(f"[!] Error en préstamo: {e}")
            return None

    def realizar_devolucion(self, id_libro, id_miembro):
        """Procesa la devolución de un libro."""
        try:
            if id_libro not in self.__libros:
                raise LibroNoEncontradoError("Libro no encontrado.")
            if id_miembro not in self.__miembros:
                raise UsuarioNoEncontradoError("Miembro no encontrado.")

            libro = self.__libros[id_libro]
            miembro = self.__miembros[id_miembro]

            libro.devolver()
            miembro.registrar_devolucion(id_libro)

            # Finalizar préstamo activo
            for prestamo in self.__prestamos.values():
                if (prestamo.to_dict()["id_libro"] == id_libro and 
                    prestamo.to_dict()["id_miembro"] == id_miembro and
                    prestamo.estado == "Activo"):
                    prestamo.finalizar()
                    break

            self._actualizar_matriz_disponibilidad()
            print(f"[+] Devolución exitosa: {libro.titulo}")
            return True

        except (LibroNoEncontradoError, UsuarioNoEncontradoError, ValidacionError) as e:
            print(f"[!] Error en devolución: {e}")
            return False

    # ==================== MATRIZ DE DISPONIBILIDAD ====================

    def _actualizar_matriz_disponibilidad(self):
        """
        Actualiza la matriz de disponibilidad.
        Filas = Categorías, Columnas = [Total, Disponibles, Prestados]
        """
        categorias = {}
        for libro in self.__libros.values():
            cat = libro.categoria
            if cat not in categorias:
                categorias[cat] = [0, 0, 0]  # [total, disponibles, prestados]
            categorias[cat][0] += libro.copias_total
            categorias[cat][1] += libro.copias_disponibles
            categorias[cat][2] += (libro.copias_total - libro.copias_disponibles)

        self.__matriz_disponibilidad = []
        for cat, valores in categorias.items():
            self.__matriz_disponibilidad.append([cat] + valores)

    def mostrar_matriz_disponibilidad(self):
        """Muestra la matriz de disponibilidad por categoría."""
        if not self.__matriz_disponibilidad:
            print("[!] No hay datos para mostrar.")
            return

        print(f"\n{'='*60}")
        print(f"  📊 MATRIZ DE DISPONIBILIDAD POR CATEGORÍA")
        print(f"{'='*60}")
        print(f"  {'Categoría':<25} {'Total':<8} {'Disp.':<8} {'Prest.':<8}")
        print(f"  {'-'*50}")

        for fila in self.__matriz_disponibilidad:
            print(f"  {fila[0]:<25} {fila[1]:<8} {fila[2]:<8} {fila[3]:<8}")

        print(f"{'='*60}\n")

    # ==================== BÚSQUEDA RECURSIVA ====================

    def buscar_libro_recursivo(self, criterio, valor, lista_libros=None, index=0, resultados=None):
        """
        Búsqueda recursiva de libros por criterio.
        Demuestra el uso de RECURSIVIDAD.
        """
        if resultados is None:
            resultados = []
        if lista_libros is None:
            lista_libros = list(self.__libros.values())

        # Caso base: lista vacía o índice fuera de rango
        if index >= len(lista_libros):
            return resultados

        libro = lista_libros[index]
        criterio = criterio.lower()

        # Verificar coincidencia
        coincide = False
        if criterio == "titulo" and valor.lower() in libro.titulo.lower():
            coincide = True
        elif criterio == "autor" and valor.lower() in libro.autor.lower():
            coincide = True
        elif criterio == "categoria" and valor.lower() in libro.categoria.lower():
            coincide = True

        if coincide:
            resultados.append(libro)

        # Llamada recursiva
        return self.buscar_libro_recursivo(criterio, valor, lista_libros, index + 1, resultados)

    # ==================== REPORTES ====================

    def generar_reporte_prestamos_activos(self):
        """Genera reporte de préstamos activos."""
        activos = [p for p in self.__prestamos.values() if p.estado == "Activo"]

        print(f"\n{'='*60}")
        print(f"  📋 PRÉSTAMOS ACTIVOS ({len(activos)})")
        print(f"{'='*60}")

        if not activos:
            print("  No hay préstamos activos.")
        else:
            for prestamo in activos:
                prestamo.mostrar_info()
        print(f"{'='*60}\n")

    def generar_reporte_completo(self):
        """Genera un reporte completo de la biblioteca."""
        print(f"\n{'='*60}")
        print(f"  📊 REPORTE COMPLETO - {self.__nombre}")
        print(f"{'='*60}")
        print(f"  Total Libros:      {len(self.__libros)}")
        print(f"  Total Miembros:    {len(self.__miembros)}")
        print(f"  Total Préstamos:   {len(self.__prestamos)}")

        activos = sum(1 for p in self.__prestamos.values() if p.estado == "Activo")
        print(f"  Préstamos Activos: {activos}")
        print(f"  Préstamos Finalizados: {len(self.__prestamos) - activos}")
        print(f"{'='*60}\n")

    def mostrar_info_libro(self, id_libro):
        """Muestra información detallada de un libro."""
        if id_libro in self.__libros:
            self.__libros[id_libro].mostrar_info()
        else:
            print(f"[!] Libro {id_libro} no encontrado.")

    def mostrar_info_miembro(self, id_miembro):
        """Muestra información detallada de un miembro."""
        if id_miembro in self.__miembros:
            self.__miembros[id_miembro].mostrar_info()
        else:
            print(f"[!] Miembro {id_miembro} no encontrado.")

    # ==================== EXPORTAR A DICCIONARIO ====================

    def exportar_datos(self):
        """Exporta todos los datos a un diccionario estructurado."""
        return {
            "biblioteca": self.__nombre,
            "fecha_exportacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "libros": {k: v.to_dict() for k, v in self.__libros.items()},
            "miembros": {k: v.to_dict() for k, v in self.__miembros.items()},
            "prestamos": {k: v.to_dict() for k, v in self.__prestamos.items()},
            "matriz_disponibilidad": self.__matriz_disponibilidad
        }


# ============================================================================
# MENÚ INTERACTIVO DEL SISTEMA
# ============================================================================

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\n  Presione ENTER para continuar...")

def mostrar_menu():
    """Muestra el menú principal del sistema."""
    print(f"\n{'='*60}")
    print(f"  📚 MENÚ PRINCIPAL - BIBLIOTECA UNIVERSITARIA")
    print(f"{'='*60}")
    print("  [1]  📖 Registrar nuevo libro")
    print("  [2]  📋 Listar todos los libros")
    print("  [3]  🔍 Buscar libro")
    print("  [4]  ✏️  Actualizar información de libro")
    print("  [5]  🗑️  Eliminar libro")
    print("  [6]  👤 Registrar nuevo miembro")
    print("  [7]  📋 Listar todos los miembros")
    print("  [8]  🔄 Renovar membresía")
    print("  [9]  📤 Realizar préstamo")
    print("  [10] 📥 Realizar devolución")
    print("  [11] 📊 Matriz de disponibilidad")
    print("  [12] 📋 Reporte de préstamos activos")
    print("  [13] 📈 Reporte completo")
    print("  [14] ℹ️  Ver información detallada")
    print("  [15] 🔎 Búsqueda recursiva de libros")
    print("  [16] 🚪 Salir")
    print(f"{'='*60}")

def menu_registrar_libro(biblio):
    """Menú para registrar un nuevo libro."""
    print("\n  --- REGISTRAR NUEVO LIBRO ---")
    try:
        titulo = input("  Título: ").strip()
        autor = input("  Autor: ").strip()
        isbn = input("  ISBN (10 o 13 dígitos): ").strip()
        anio = int(input("  Año de publicación: "))
        categoria = input("  Categoría: ").strip()
        editorial = input("  Editorial (opcional): ").strip() or "Desconocida"
        copias = int(input("  Número de copias [1]: ") or "1")

        id_libro = biblio.registrar_libro(titulo, autor, isbn, anio, 
                                          categoria, editorial, copias)
        if id_libro:
            print(f"\n  ✅ Libro registrado con ID: {id_libro}")
    except ValueError:
        print("  [!] Error: El año y las copias deben ser números enteros.")
    except Exception as e:
        print(f"  [!] Error: {e}")

def menu_registrar_miembro(biblio):
    """Menú para registrar un nuevo miembro."""
    print("\n  --- REGISTRAR NUEVO MIEMBRO ---")
    try:
        nombres = input("  Nombres: ").strip()
        apellidos = input("  Apellidos: ").strip()
        dni = input("  DNI: ").strip()
        email = input("  Email: ").strip()
        telefono = input("  Teléfono (opcional): ").strip()

        print("  Tipos de membresía: Estándar, Premium, Estudiante, Docente")
        tipo = input("  Tipo [Estándar]: ").strip() or "Estándar"

        id_miembro = biblio.registrar_miembro(nombres, apellidos, dni, 
                                               email, telefono, tipo)
        if id_miembro:
            print(f"\n  ✅ Miembro registrado con ID: {id_miembro}")
    except Exception as e:
        print(f"  [!] Error: {e}")

def menu_buscar_libro(biblio):
    """Menú para buscar libros."""
    print("\n  --- BUSCAR LIBRO ---")
    print("  Criterios: titulo, autor, categoria, isbn")
    criterio = input("  Criterio: ").strip()
    valor = input("  Valor a buscar: ").strip()

    resultados = biblio.buscar_libro(criterio, valor)

    if resultados:
        print(f"\n  ✅ Se encontraron {len(resultados)} resultado(s):")
        for libro in resultados:
            print(f"    • {libro}")
    else:
        print("  [!] No se encontraron resultados.")

def menu_actualizar_libro(biblio):
    """Menú para actualizar un libro."""
    print("\n  --- ACTUALIZAR LIBRO ---")
    id_libro = input("  ID del libro: ").strip().upper()

    print("  Campos disponibles: titulo, autor, isbn, anio_publicacion,")
    print("                      categoria, editorial, copias_total")
    print("  Formato: campo=valor (ej: titulo=Nuevo Titulo)")
    print("  Ingrese campos (vacío para terminar):")

    kwargs = {}
    while True:
        entrada = input("  > ").strip()
        if not entrada:
            break
        if "=" in entrada:
            campo, valor = entrada.split("=", 1)
            campo = campo.strip()
            valor = valor.strip()
            # Convertir tipos si es necesario
            if campo == "anio_publicacion" or campo == "copias_total":
                valor = int(valor)
            kwargs[campo] = valor

    biblio.actualizar_libro(id_libro, **kwargs)

def menu_prestamo(biblio):
    """Menú para realizar un préstamo."""
    print("\n  --- REALIZAR PRÉSTAMO ---")
    id_libro = input("  ID del libro: ").strip().upper()
    id_miembro = input("  ID del miembro: ").strip().upper()
    dias = input("  Días de préstamo [14]: ").strip() or "14"

    biblio.realizar_prestamo(id_libro, id_miembro, int(dias))

def menu_devolucion(biblio):
    """Menú para realizar una devolución."""
    print("\n  --- REALIZAR DEVOLUCIÓN ---")
    id_libro = input("  ID del libro: ").strip().upper()
    id_miembro = input("  ID del miembro: ").strip().upper()

    biblio.realizar_devolucion(id_libro, id_miembro)

def menu_info_detallada(biblio):
    """Menú para ver información detallada."""
    print("\n  --- INFORMACIÓN DETALLADA ---")
    print("  [1] Libro")
    print("  [2] Miembro")
    opcion = input("  Seleccione: ").strip()

    if opcion == "1":
        id_libro = input("  ID del libro: ").strip().upper()
        biblio.mostrar_info_libro(id_libro)
    elif opcion == "2":
        id_miembro = input("  ID del miembro: ").strip().upper()
        biblio.mostrar_info_miembro(id_miembro)

def menu_busqueda_recursiva(biblio):
    """Menú para búsqueda recursiva."""
    print("\n  --- BÚSQUEDA RECURSIVA ---")
    print("  Criterios: titulo, autor, categoria")
    criterio = input("  Criterio: ").strip()
    valor = input("  Valor a buscar: ").strip()

    resultados = biblio.buscar_libro_recursivo(criterio, valor)

    if resultados:
        print(f"\n  ✅ Se encontraron {len(resultados)} resultado(s) [RECURSIVO]:")
        for libro in resultados:
            print(f"    • {libro}")
    else:
        print("  [!] No se encontraron resultados.")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta el sistema de biblioteca."""

    # Crear instancia de la biblioteca
    biblioteca = Biblioteca("Biblioteca Universitaria IDAT")

    # Cargar datos de ejemplo (opcional, para demostración)
    print("\n  Cargando datos de ejemplo...")
    biblioteca.registrar_libro("Python para Todos", "Charles Severance", 
                                "9781530051120", 2016, "Programación", 
                                "Amazon", 3)
    biblioteca.registrar_libro("Clean Code", "Robert C. Martin", 
                                "9780132350884", 2008, "Programación", 
                                "Prentice Hall", 2)
    biblioteca.registrar_libro("El Principito", "Antoine de Saint-Exupéry", 
                                "9780156012195", 1943, "Literatura", 
                                "Reynal & Hitchcock", 5)
    biblioteca.registrar_libro("Cálculo de una Variable", "James Stewart", 
                                "9786074817878", 2012, "Matemáticas", 
                                "Cengage", 4)
    biblioteca.registrar_libro("Inteligencia Artificial", "Stuart Russell", 
                                "9780136042594", 2020, "Tecnología", 
                                "Pearson", 2)

    biblioteca.registrar_miembro("Juan", "Pérez García", "12345678", 
                                  "juan.perez@idat.edu.pe", "987654321", "Estudiante")
    biblioteca.registrar_miembro("María", "López Torres", "87654321", 
                                  "maria.lopez@idat.edu.pe", "912345678", "Docente")
    biblioteca.registrar_miembro("Carlos", "Ruiz Díaz", "45678912", 
                                  "carlos.ruiz@idat.edu.pe", "", "Premium")

    print("  Datos de ejemplo cargados.\n")
    pausar()
    limpiar_pantalla()

    # Bucle principal del menú
    while True:
        mostrar_menu()

        try:
            opcion = input("  Seleccione una opción: ").strip()

            if opcion == "1":
                limpiar_pantalla()
                menu_registrar_libro(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "2":
                limpiar_pantalla()
                biblioteca.listar_libros()
                pausar()
                limpiar_pantalla()

            elif opcion == "3":
                limpiar_pantalla()
                menu_buscar_libro(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "4":
                limpiar_pantalla()
                menu_actualizar_libro(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "5":
                limpiar_pantalla()
                id_libro = input("  ID del libro a eliminar: ").strip().upper()
                biblioteca.eliminar_libro(id_libro)
                pausar()
                limpiar_pantalla()

            elif opcion == "6":
                limpiar_pantalla()
                menu_registrar_miembro(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "7":
                limpiar_pantalla()
                biblioteca.listar_miembros()
                pausar()
                limpiar_pantalla()

            elif opcion == "8":
                limpiar_pantalla()
                id_miembro = input("  ID del miembro: ").strip().upper()
                dias = input("  Días de renovación [365]: ").strip() or "365"
                biblioteca.renovar_membresia(id_miembro, int(dias))
                pausar()
                limpiar_pantalla()

            elif opcion == "9":
                limpiar_pantalla()
                menu_prestamo(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "10":
                limpiar_pantalla()
                menu_devolucion(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "11":
                limpiar_pantalla()
                biblioteca.mostrar_matriz_disponibilidad()
                pausar()
                limpiar_pantalla()

            elif opcion == "12":
                limpiar_pantalla()
                biblioteca.generar_reporte_prestamos_activos()
                pausar()
                limpiar_pantalla()

            elif opcion == "13":
                limpiar_pantalla()
                biblioteca.generar_reporte_completo()
                pausar()
                limpiar_pantalla()

            elif opcion == "14":
                limpiar_pantalla()
                menu_info_detallada(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "15":
                limpiar_pantalla()
                menu_busqueda_recursiva(biblioteca)
                pausar()
                limpiar_pantalla()

            elif opcion == "16":
                limpiar_pantalla()
                print("\n  👋 ¡Gracias por usar el Sistema de Biblioteca Universitaria!")
                print(f"  {'='*60}\n")
                break

            else:
                print("\n  [!] Opción no válida. Intente nuevamente.")
                pausar()
                limpiar_pantalla()

        except KeyboardInterrupt:
            print("\n\n  [!] Interrupción detectada. Saliendo...")
            break
        except Exception as e:
            print(f"\n  [!] Error inesperado: {e}")
            pausar()
            limpiar_pantalla()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
