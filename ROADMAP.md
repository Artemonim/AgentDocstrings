## Changes Made
1. `pyproject.toml`
   • Заменён параметр `readme = "README.md"` на таблицу с указанием типа контента:  
     `readme = { file = "README.md", content-type = "text/markdown" }`  
   • Добавлен блок `[project.urls]` (Homepage / Source / Tracker) c шаблонными ссылками на GitHub.
2. `MANIFEST.in` – создан новый файл, чтобы README и LICENSE гарантированно попадали в sdist.

## Unfulfilled Tasks
• В `pyproject.toml` до сих пор стоят заглушки (`Your Name`, `your@email.com`, ссылки в [project.urls]).
• При необходимости следует добавить реальный список зависимостей в `[project] dependencies = [...]` (сейчас библиотека опирается только на stdlib, но если в будущем появятся сторонние пакеты — декларируйте их).

## Manual Changes Required
1. Заполнить поля автора, e-mail и ссылки на репозиторий.
2. При желании:
   • Добавить ключевые слова, дополнительную классификацию, краткое/длинное описание на русском и английском.  
   • Перевести дублирующуюся версию из `pyproject.toml` в код (или наоборот) – чтобы не поддерживать значение в двух местах (см. Rationale).

## Special Attention Required
• Убедитесь, что имя проекта (`agent-docstrings`) уникально на PyPI.  
• Если хотите, чтобы инструмент вызывался также командой `python -m agent_docstrings`, можно добавить файл `agent_docstrings/__main__.py`, вызывающий `cli.main()`.

# Доработки
## Идеи
- [ ] режим чёрного списка (по умолчанию)
- [ ] режим белого списка (отключает чёрный список)
- [ ] проверить поддержку Python 3.8, Python 3.11, Python 3.13

## Шаги для публикации
1. Настройка окружения публикации  
   ```
   python -m pip install --upgrade build twine
   ```
2. Локальная сборка пакета  
   ```
   python -m build    # создаст dist/*.whl и dist/*.tar.gz
   ```
3. Проверка готового артефакта  
   ```
   python -m pip install dist/agent_docstrings-0.1.0-py3-none-any.whl
   agent-docstrings --help               # CLI должна отработать
   ```
4. Регистрация/вход на TestPyPI (https://test.pypi.org)  
   ```
   twine upload --repository testpypi dist/*
   python -m pip install --index-url https://test.pypi.org/simple --no-deps agent-docstrings
   agent-docstrings path/to/code
   ```
5. Если всё корректно – публикация в основное хранилище  
   ```
   twine upload dist/*
   ```
6. Обновите README: замените блок «=== TODO: Replace this with the actual package name once published. ===» на актуальную команду `pip install agent-docstrings`.
