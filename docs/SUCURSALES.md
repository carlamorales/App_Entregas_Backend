# API de Sucursales

## Endpoints

### Listar Sucursales
- **GET /sucursales/**
- **Permiso requerido**: `sucursales.read`
- **Descripción**: Retorna una lista de todas las sucursales.
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "codigo": "SUC001",
      "nombre_sucursal": "Sucursal Principal"
    },
    {
      "codigo": "SUC002",
      "nombre_sucursal": "Sucursal Secundaria"
    }
  ]
  ```

### Obtener una Sucursal
- **GET /sucursales/<codigo>**
- **Permiso requerido**: `sucursales.read`
- **Descripción**: Retorna una sucursal específica.
- **Parámetros de URL**:
  - `codigo` (string, requerido): El código de la sucursal.
- **Respuesta exitosa (200)**:
  ```json
  {
    "codigo": "SUC001",
    "nombre_sucursal": "Sucursal Principal",
    "direccion": "Calle Falsa 123",
    "telefono": "123456789"
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }
  ```

### Crear una Sucursal
- **POST /sucursales/**
- **Permiso requerido**: `sucursales.create`
- **Descripción**: Crea una nueva sucursal.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "codigo": "SUC003",
    "nombre_sucursal": "Nueva Sucursal",
    "direccion": "Avenida Siempre Viva 742",
    "telefono": "987654321"
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "ok": true,
    "codigo": "SUC003"
  }
  ```
- **Respuesta de error (400)**:
  ```json
  {
    "error": "codigo y nombre_sucursal requeridos"
  }
  ```

### Actualizar una Sucursal
- **PUT /sucursales/<codigo>**
- **Permiso requerido**: `sucursales.update`
- **Descripción**: Actualiza una sucursal existente.
- **Parámetros de URL**:
  - `codigo` (string, requerido): El código de la sucursal.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre_sucursal": "Nuevo Nombre Sucursal",
    "direccion": "Nueva Direccion",
    "telefono": "111222333"
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "ok": true,
    "codigo": "SUC001"
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }