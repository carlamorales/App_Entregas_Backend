# API de Períodos

## Endpoints

### Listar Períodos
- **GET /periodos/**
- **Permiso requerido**: `periodos.read`
- **Descripción**: Retorna una lista de todos los períodos.
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "codigo": "PER2023-01",
      "nombre_periodo": "Enero 2023"
    },
    {
      "codigo": "PER2023-02",
      "nombre_periodo": "Febrero 2023"
    }
  ]
  ```

### Obtener un Período
- **GET /periodos/<codigo>**
- **Permiso requerido**: `periodos.read`
- **Descripción**: Retorna un período específico.
- **Parámetros de URL**:
  - `codigo` (string, requerido): El código del período.
- **Respuesta exitosa (200)**:
  ```json
  {
    "codigo": "PER2023-01",
    "nombre_periodo": "Enero 2023",
    "fecha_inicio": "2023-01-01",
    "fecha_final": "2023-01-31"
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }
  ```

### Crear un Período
- **POST /periodos/**
- **Permiso requerido**: `periodos.create`
- **Descripción**: Crea un nuevo período.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "codigo": "PER2023-03",
    "nombre_periodo": "Marzo 2023",
    "fecha_inicio": "2023-03-01",
    "fecha_final": "2023-03-31"
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "ok": true,
    "codigo": "PER2023-03"
  }
  ```
- **Respuesta de error (400)**:
  ```json
  {
    "error": "codigo, nombre_periodo, fecha_inicio y fecha_final son requeridos"
  }
  ```
- **Respuesta de error (400)**:
    ```json
    {
        "error": "fechas deben estar en formato YYYY-MM-DD"
    }
    ```

### Actualizar un Período
- **PUT /periodos/<codigo>**
- **Permiso requerido**: `periodos.update`
- **Descripción**: Actualiza un período existente.
- **Parámetros de URL**:
  - `codigo` (string, requerido): El código del período.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre_periodo": "Nuevo Nombre",
    "fecha_inicio": "2023-03-02",
    "fecha_final": "2023-04-01"
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "ok": true,
    "codigo": "PER2023-03"
  }
  ```
- **Respuesta de error (400)**:
    ```json
    {
        "error": "fecha_inicio formato inválido"
    }
    ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }