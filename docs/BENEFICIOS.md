# API de Beneficios

## Endpoints

### Listar Beneficios
- **GET /beneficios/**
- **Permiso requerido**: `beneficios.read`
- **Descripción**: Retorna una lista de todos los beneficios.
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "codigo": "BEN001",
      "nombre_beneficio": "Seguro de Salud"
    },
    {
      "codigo": "BEN002",
      "nombre_beneficio": "Vales de Comida"
    }
  ]
  ```

### Obtener un Beneficio
- **GET /beneficios/<codigo>**
- **Permiso requerido**: `beneficios.read`
- **Descripción**: Retorna un beneficio específico.
- **Parámetros de URL**:
  - `codigo` (string, requerido): El código del beneficio.
- **Respuesta exitosa (200)**:
  ```json
  {
    "codigo": "BEN001",
    "nombre_beneficio": "Seguro de Salud",
    "descripcion": "Seguro de salud complementario.",
    "activo": true
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }
  ```

### Crear un Beneficio
- **POST /beneficios/**
- **Permiso requerido**: `beneficios.create`
- **Descripción**: Crea un nuevo beneficio.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "codigo": "BEN003",
    "nombre_beneficio": "Bono de Transporte",
    "descripcion": "Bono mensual para transporte.",
    "activo": true
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "ok": true,
    "codigo": "BEN003"
  }
  ```
- **Respuesta de error (400)**:
  ```json
  {
    "error": "codigo y nombre_beneficio requeridos"
  }
  ```

### Actualizar un Beneficio
- **PUT /beneficios/<codigo>**
- **Permiso requerido**: `beneficios.update`
- **Descripción**: Actualiza un beneficio existente.
- **Parámetros de URL**:
  - `codigo` (string, requerido): El código del beneficio.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "nombre_beneficio": "Nuevo Nombre",
    "descripcion": "Nueva descripción.",
    "activo": false
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "ok": true,
    "codigo": "BEN001"
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }
  ```
