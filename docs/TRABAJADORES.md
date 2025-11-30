# API de Trabajadores

## Endpoints

### Listar Trabajadores
- **GET /trabajadores/**
- **Permiso requerido**: `trabajadores.read`
- **Descripción**: Retorna una lista de todos los trabajadores.
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "rut": "12345678-9",
      "primer_nombre": "Juan",
      "primer_apellido": "Perez"
    },
    {
      "rut": "98765432-1",
      "primer_nombre": "Maria",
      "primer_apellido": "Gonzalez"
    }
  ]
  ```

### Obtener un Trabajador
- **GET /trabajadores/<rut>**
- **Permiso requerido**: `trabajadores.read`
- **Descripción**: Retorna un trabajador específico.
- **Parámetros de URL**:
  - `rut` (string, requerido): El RUT del trabajador.
- **Respuesta exitosa (200)**:
  ```json
  {
    "rut": "12345678-9",
    "primer_nombre": "Juan",
    "segundo_nombre": "Carlos",
    "primer_apellido": "Perez",
    "segundo_apellido": "Gomez",
    "email": "juan.perez@example.com",
    "cargo": "Desarrollador",
    "activo": true
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }
  ```

### Crear un Trabajador
- **POST /trabajadores/**
- **Permiso requerido**: `trabajadores.create`
- **Descripción**: Crea un nuevo trabajador.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "rut": "11223344-5",
    "primer_nombre": "Pedro",
    "segundo_nombre": "",
    "primer_apellido": "Soto",
    "segundo_apellido": "",
    "email": "pedro.soto@example.com",
    "cargo": "Diseñador",
    "activo": true
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "ok": true,
    "rut": "11223344-5"
  }
  ```
- **Respuesta de error (400)**:
  ```json
  {
    "error": "rut, primer_nombre y primer_apellido son requeridos"
  }
  ```

### Actualizar un Trabajador
- **PUT /trabajadores/<rut>**
- **Permiso requerido**: `trabajadores.update`
- **Descripción**: Actualiza un trabajador existente.
- **Parámetros de URL**:
  - `rut` (string, requerido): El RUT del trabajador.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "primer_nombre": "Peter",
    "email": "peter.soto@example.com",
    "activo": false
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "ok": true,
    "rut": "11223344-5"
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }