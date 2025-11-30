# API de Usuarios

## Endpoints

### Listar Usuarios
- **GET /usuarios/**
- **Permiso requerido**: `usuarios.read`
- **Descripción**: Retorna una lista de todos los usuarios.
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "ID": 1,
      "usuario": "admin",
      "rol": "admin"
    },
    {
      "ID": 2,
      "usuario": "operador1",
      "rol": "operador"
    }
  ]
  ```

### Obtener un Usuario
- **GET /usuarios/<id>**
- **Permiso requerido**: `usuarios.read`
- **Descripción**: Retorna un usuario específico.
- **Parámetros de URL**:
  - `id` (integer, requerido): El ID del usuario.
- **Respuesta exitosa (200)**:
  ```json
  {
    "ID": 1,
    "usuario": "admin",
    "rol": "admin",
    "email": "admin@example.com",
    "activo": true
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }
  ```

### Crear un Usuario
- **POST /usuarios/**
- **Permiso requerido**: `usuarios.create`
- **Descripción**: Crea un nuevo usuario.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "usuario": "nuevo_usuario",
    "contrasena": "password123",
    "rol": "operador",
    "email": "nuevo@example.com",
    "activo": true
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "ok": true,
    "id": 3
  }
  ```
- **Respuesta de error (400)**:
  ```json
  {
    "error": "usuario y contrasena requeridos"
  }
  ```

### Actualizar un Usuario
- **PUT /usuarios/<id>**
- **Permiso requerido**: `usuarios.update`
- **Descripción**: Actualiza un usuario existente.
- **Parámetros de URL**:
  - `id` (integer, requerido): El ID del usuario.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "usuario": "usuario_actualizado",
    "rol": "supervisor",
    "email": "actualizado@example.com",
    "activo": false,
    "contrasena": "nuevacontrasena"
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "ok": true,
    "ID": 1
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }