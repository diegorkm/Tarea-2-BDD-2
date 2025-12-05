# Tarea-2-BDD-2

## Descripción general de los cambios

### 1. Categorías (Category)
- Se creó el modelo `Category` y la tabla intermedia `BookCategory` para la relación many-to-many con `Book`.
- Se implementó `CategoryController` con operaciones CRUD.
- Se agregaron sus respectivos DTOs y repositorio.
- Se requirió asistencia de chatgpt para aprender a manejarme con el orden de las carpetas.
- Se requirió asistencia de chatgpt para solucionar problemas de ultimo momento al intentar realizar requerimiento 8 (se solventó pero ahora no puedo crear libros con categorías, por lo cual se modifica tabla para dejar en parcial)

### 2. Reseñas (Review)
- Se creó el modelo `Review` con relaciones hacia `User` y `Book`.
- Se agregaron DTOs y un controlador CRUD.
- Se valida que el `rating` esté entre 1 y 5 al crear una reseña.

### 3. Libros (Book) — Inventario y datos extra
- Se añadieron los campos `stock`, `description`, `language` y `publisher`.
- Validaciones:
  - `stock > 0` al crear.
  - `stock` no puede quedar negativo al actualizar.
  - `language` debe ser un código de 2 letras.
- Se agregaron métodos avanzados en el repositorio y endpoints.

### 4. Usuarios (User)
- Se añadieron los campos `email` (único), `phone`, `address` e `is_active`.
- `UserReadDTO` oculta la contraseña y préstamos.
- `is_active` está protegido y no puede ser modificado desde los DTOs.
- Se valida el formato del correo en creación y actualización.

### 5. Préstamos (Loan)
- Se añadieron `due_date`, `fine_amount` y `status`.
- Se creó un enum `LoanStatus` con: `ACTIVE`, `RETURNED`, `OVERDUE`.
- `status` tiene valor por defecto `ACTIVE`.
- `due_date` se calcula automáticamente como 14 días después de `loan_dt`.
- Los DTOs fueron ajustados para permitir sólo la actualización del `status`.
- Se requirió asistencia de chatgpt con las cosas necesarias que habían que importar y como se utilizaban, ya que tenia problemas y me daba error cuando intentaba hacer upgrade.

### 6. Consultas avanzadas — BookRepository
Se implementaron nuevos métodos:
- `get_available_books()`
- `find_by_category()`
- `get_most_reviewed_books()`
- `update_stock()`
- `search_by_author()`

Y se agregaron sus endpoints correspondientes en `BookController`.

## Tabla de cumplimiento de requerimientos

| # | Requerimiento                                                                                         | Estado    |
|---|--------------------------------------------------------------------------------------------------------|-----------|
| 1 | Category + tabla intermedia + CRUD + DTOs                                                             | Parcial  |
| 2 | Review + relaciones + CRUD + validación rating                                                        | Cumplido creo  |
| 3 | Nuevos campos en Book + validaciones + migración                                                      | Cumplido  |
| 4 | Nuevos campos en User + email validado + is_active protegido                                          | Cumplido  |
| 5 | Nuevos campos en Loan + enum + due_date automático + DTOs                                             | Cumplido  |
| 6 | Nuevos métodos en BookRepository + endpoints en BookController                                        | Cumplido  |
| 7 | Implementación de métodos en LoanRepository                                                        | No cumplido  |
| 8 | Creación de cosas en la base de datos                                                               | No cumplido  |
