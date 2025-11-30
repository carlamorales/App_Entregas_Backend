# API de Reportes

## Endpoints

### Reporte de Entregas por Beneficio
- **GET /reportes/entregas-por-beneficio**
- **Permiso requerido**: `reportes.read`
- **Descripción**: Retorna un reporte de entregas agrupadas por beneficio para un período específico.
- **Parámetros de Query**:
  - `periodo` (string, requerido): El código del período para el cual se desea generar el reporte.
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "periodo": "PER2023-01",
      "beneficio_cod": "BEN001",
      "total": 10,
      "entregados": 5,
      "pendientes": 4,
      "rechazados": 1
    },
    {
      "periodo": "PER2023-01",
      "beneficio_cod": "BEN002",
      "total": 15,
      "entregados": 10,
      "pendientes": 5,
      "rechazados": 0
    }
  ]
  ```
- **Respuesta de error (400)**:
    ```json
    {
        "error": "Debe indicar ?periodo=CODIGO"
    }