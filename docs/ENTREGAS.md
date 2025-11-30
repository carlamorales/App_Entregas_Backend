# API de Entregas

## Endpoints

### Listar Entregas
- **GET /entregas/**
- **Permiso requerido**: `entregas.read`
- **Descripción**: Retorna una lista de todas las entregas.
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "ID": 1,
      "Trabajador_Rut": "12345678-9",
      "Beneficio_cod": "BEN001",
      "Estado": "PENDIENTE"
    },
    {
      "ID": 2,
      "Trabajador_Rut": "98765432-1",
      "Beneficio_cod": "BEN002",
      "Estado": "ENTREGADO"
    }
  ]
  ```

### Obtener una Entrega
- **GET /entregas/<id>**
- **Permiso requerido**: `entregas.read`
- **Descripción**: Retorna una entrega específica.
- **Parámetros de URL**:
  - `id` (integer, requerido): El ID de la entrega.
- **Respuesta exitosa (200)**:
  ```json
  {
    "ID": 1,
    "Trabajador_Rut": "12345678-9",
    "Beneficio_cod": "BEN001",
    "Estado": "PENDIENTE",
    "Periodo_cod": "PER2023-01",
    "CodSucursal": "SUC001",
    "TipoContrato": "INDEFINIDO"
  }
  ```
- **Respuesta de error (404)**:
  ```json
  {
    "error": "Not Found"
  }
  ```

### Crear una Entrega
- **POST /entregas/**
- **Permiso requerido**: `entregas.create`
- **Descripción**: Crea una nueva entrega.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "Trabajador_Rut": "11223344-5",
    "Beneficio_cod": "BEN003",
    "Estado": "PENDIENTE",
    "Periodo_cod": "PER2023-03",
    "CodSucursal": "SUC002",
    "TipoContrato": "PLAZO FIJO",
    "Usuario_creador": "admin",
    "FechaEntrega": "2023-03-20T10:00:00"
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "ok": true,
    "ID": 3
  }
  ```
- **Respuesta de error (400)**:
  ```json
  {
    "error": "Rut y Beneficio_cod son requeridos"
  }
  ```
- **Respuesta de error (400)**:
    ```json
    {
        "error": "FechaEntrega en formato ISO requerido"
    }
    ```

### Actualizar una Entrega
- **PUT /entregas/<id>**
- **Permiso requerido**: `entregas.update`
- **Descripción**: Actualiza una entrega existente.
- **Parámetros de URL**:
  - `id` (integer, requerido): El ID de la entrega.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "Estado": "ENTREGADO",
    "Periodo_cod": "PER2023-04"
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