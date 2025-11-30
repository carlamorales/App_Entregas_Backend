# API de Autenticación

## Endpoints

### Iniciar Sesión
- **POST /auth/login**
- **Descripción**: Autentica a un usuario y retorna un token de acceso y un token de refresco.
- **Cuerpo de la solicitud (JSON)**:
  ```json
  {
    "usuario": "nombre_de_usuario",
    "contrasena": "tu_contrasena"
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "access_token": "ey...",
    "refresh_token": "ey..."
  }
  ```
- **Respuesta de error (400)**:
  ```json
  {
    "error": "usuario y contrasena son requeridos"
  }
  ```
- **Respuesta de error (401)**:
  ```json
  {
    "error": "credenciales inválidas"
  }
  ```

### Refrescar Token
- **POST /auth/refresh**
- **Descripción**: Retorna un nuevo token de acceso y un nuevo token de refresco. El token de refresco anterior es invalidado.
- **Encabezados**:
  - `Authorization`: `Bearer <refresh_token>`
- **Respuesta exitosa (200)**:
  ```json
  {
    "access_token": "ey...",
    "refresh_token": "ey..."
  }
  ```
- **Respuesta de error (401)**:
  ```json
  {
    "msg": "Token has expired"
  }
  ```

### Cerrar Sesión
- **POST /auth/logout**
- **Descripción**: Invalida el token de refresco.
- **Encabezados**:
  - `Authorization`: `Bearer <refresh_token>`
- **Respuesta exitosa (200)**:
  ```json
  {
    "ok": true
  }