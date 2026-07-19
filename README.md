# Mini gestor de incidencias

API en Django + DRF y una vista en Nuxt 4 que la consume.

## Arranque

Requisito único: Docker y Docker Compose.

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- API: http://localhost:8000/api/tickets/
- Admin de Django (opcional, sin superusuario creado por defecto): http://localhost:8000/admin/

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/tickets/` | Listado, ordenado por `created_at` descendente. Filtros: `?status=` y `?priority=` |
| POST | `/api/tickets/` | Creación. Rechaza `status=closed` en la creación |
| PATCH | `/api/tickets/<id>/` | Actualización parcial. Rechaza `closed -> open` directo |
| GET | `/api/tickets/stats/` | Recuento de tickets agrupado por `status` |

## Decisiones técnicas

**Django 5.1 en vez de 6.0.** Poetry resolvió por defecto Django 6.0, que exige Python ≥3.12 para *runtime* pero además rompía la resolución de dependencias en el entorno de desarrollo (Python 3.14 con constraint `^3.11`). Django 5.1 es la última LTS estable y evita arrastrar una versión mayor recién salida sin necesidad real para este ejercicio.

**App organizada en `models/`, `serializers/`, `selectors/`, `services/`, `viewsets/` y `tests/` (estilo "selectors + services" de HackSoft).** `selectors` concentra las queries de lectura, `services` la escritura y las reglas de negocio, y el serializer queda "tonto" (solo forma y tipos). El viewset no llama a `serializer.save()`: valida con el serializer y delega en el service, traduciendo el `ValidationError` de Django a un 400 de DRF.

**`ModelViewSet` con métodos HTTP restringidos.** El enunciado solo pide `GET`, `POST` y `PATCH`; `http_method_names` en el viewset excluye `PUT` y `DELETE` explícitamente en vez de dejarlos disponibles "por si acaso" con `ModelViewSet` por defecto.

**Nuxt en modo SPA (`ssr: false`).** Es una vista interna sin necesidad de SEO ni de contenido indexable. Desactivar SSR evita el problema clásico en Docker de tener que resolver dos URLs distintas para la misma API (una interna entre contenedores para el render en servidor, otra pública para el navegador): con SPA, todas las llamadas salen siempre del navegador contra la URL pública.

**`NUXT_PUBLIC_API_BASE` resuelto en tiempo de arranque del contenedor, no en build.** El `runtimeConfig.public` de Nuxt se inyecta en el HTML servido por Nitro en cada arranque, así que la URL de la API se configura vía variable de entorno en `docker-compose.yml` sin necesidad de reconstruir la imagen del frontend si cambia el puerto o el host publicado.

**Cada `TicketItem` gestiona su propia transición de estado.** El `<select>` de estado llama a la API directamente desde el componente de fila, revierte visualmente si el backend rechaza la transición y muestra el mensaje de error devuelto por DRF junto a esa fila.

## Tests

```bash
cd backend
poetry install
poetry run python manage.py test tickets
```

O contra el contenedor ya construido:

```bash
docker compose run --rm backend python manage.py test tickets
```

Hay 7 tests en `tickets/tests/test_ticket.py` (todos los tests de un mismo modelo van en un único fichero, con una clase `TestCase` por comportamiento: creación, transiciones de estado, listado/filtros, stats). Los dos que considero más valiosos son los que cubren la regla de negocio pedida explícitamente en el enunciado:

- `test_closed_ticket_cannot_go_back_to_open_directly`: un PATCH de `closed` a `open` debe devolver 400 y no modificar el ticket.
- `test_closed_ticket_can_go_to_in_progress`: confirma que la regla no bloquea el camino válido (`closed -> in_progress`), evitando que una validación demasiado agresiva rompa transiciones legítimas.

El resto (creación con `status=closed` rechazada, filtros combinados, orden descendente, `stats/`) cubren el resto de requisitos explícitos del enunciado con un test por comportamiento.

## Qué dejaría para una segunda iteración

- **PostgreSQL en Docker.** Es el cambio más obvio de cara a producción; no lo hice porque el enunciado lo marca como plus y prefería invertir el tiempo en la regla de negocio, los tests y que el `docker compose up` fuera robusto.
- **Paginación en `GET /api/tickets/`.** Con un volumen de datos real, devolver la lista completa no escala; no la añadí porque no estaba pedida y complica el contrato del frontend sin necesidad para este ejercicio.
- **Autenticación/autorización.** Explícitamente fuera de alcance según el enunciado. De implementarse, contemplaría tres roles: `admin` (gestiona el sistema), `agent` (resuelve tickets de su departamento) y `customer` (reporta tickets; asociado a un departamento, ligado al punto de departamentos y clasificación automática).
- **Departamentos y clasificación automática.** Añadir un campo `department` al ticket y clasificar cada ticket entrante en su departamento correspondiente mediante IA (a partir del título/descripción), en vez de asignarlo a mano. Es una funcionalidad nueva, no una decisión de este ejercicio, así que la dejo fuera de alcance.


## Estructura

```
backend/               Django + DRF (Poetry, pyproject.toml)
  tickets/
    models/ticket.py              Ticket
    serializers/serializer_ticket.py   forma/tipos de los campos, sin reglas de negocio
    selectors/selector_ticket.py       queries de lectura (list, stats)
    services/service_ticket.py         escritura + reglas de negocio (create, update)
    viewsets/viewset_ticket.py         orquesta serializer + selector/service
    tests/test_ticket.py               todos los tests del modelo Ticket
frontend/              Nuxt 4 (pnpm, pnpm-lock.yaml)
docker-compose.yml
```
