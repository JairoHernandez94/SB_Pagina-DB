# Sabores de Babilonia — Front + Registro/Ingreso (Flask + MySQL)

## Puesta en marcha
1. Crear la base de datos: `mysql -u root -p < database/schema.sql`
   (descomenta las líneas de `CREATE USER`/`GRANT` y cambia la contraseña).
2. `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. Copiar `.env.example` a `.env` y completar los datos.
5. `python app.py` → http://127.0.0.1:5000

## Estructura
- `app.py` rutas: `/`, `/registro`, `/ingreso`, `/panel`, `/salir`
- `templates/` vistas Jinja2 · `static/` CSS, JS e imagen del logo
- `database/schema.sql` tabla `usuarios` (contraseñas con hash, nunca en texto plano)

## Paleta (tomada del logo)
Crema #FBF3DC · Oro #B37A11 · Verde hoja #3F5B3A · Lavanda #5B3F7A · Fresa #C8372D · Canela #8B4A1F
