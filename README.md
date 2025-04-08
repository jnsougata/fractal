![fractal](https://github.com/user-attachments/assets/2048c2df-7f48-4ecf-b469-4ad5ee46e91f)

# FractalDB - KV Store
A fast, lightweight key-value store designed for hobbyists, combining the simplicity of NoSQL with SQLite3's robust filtering and sorting capabilities.
## Features
- **NoSQL-like Experience** – Work with database records as Python dictionaries.
- **Simplified Access** – Retrieve data without remembering column names or indices.
- **SQL Power** – Use SQL queries for filtering and sorting.
- **Lightweight & Fast** – Minimal overhead with SQLite’s reliability.

## Installation
```sh
pip install git+https://github.com/jnsougata/fractal.git
```

## Example Usage

```python
from fractal import cond, DB, Schema, Field


if __name__ == "__main__":
    
    db = DB("example.db")
    
    users = db.collection(
        name="users",
        schema=Schema(Field("name", str), Field("age", int))
    )
    
    inserted = users.insert(
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 35},
        {"name": "David", "age": 40},
    )
    
    c1 = cond("name").anyof("Alice", "Bob") and cond("age").between(20, 40)
    c2 = cond("age").between(20, 30) and cond("name").substring("li")

    users = users.query().where(c1 or c2)
    for user in users:
        print(user)
```

#### Sample Output:
```
{'key': '379b87afd3d74f49bc1c59b8185bb534', 'timestamp': '2025-04-08 16:25:13.012322', 'name': 'Alice', 'age': 25}
{'key': '15676bf56c524e5b87db4ee0a659efc7', 'timestamp': '2025-04-08 16:25:13.012322', 'name': 'Bob', 'age': 30}
```

## Documentation
Half-baked docs [here.](https://fractal.readthedocs.io/en/latest/)

## TODO
- Add more SQL features (e.g., `JOIN`, `GROUP BY`).
- Add more complex `queries` and `filtering` options.
- Implement `view` handling.
- Better error handling.
- Composite column support (no flattening).
- Hierarchical column search.
- More examples and documentation.
- Unit tests.
- Performance benchmarks.
