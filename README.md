![driz](https://github.com/user-attachments/assets/75f99420-b480-4199-987d-8542e6236507)

# Driz - Pseudo K-V Database

A lightweight, efficient SQLite wrapper for Python that makes SQLite3 feel like NoSQL, while retaining SQL’s filtering and sorting power.
## Features
- **NoSQL-like Experience** – Work with database records as Python dictionaries.
- **Simplified Access** – Retrieve data without remembering column names or indices.
- **SQL Power** – Use SQL queries for filtering and sorting.
- **Lightweight & Fast** – Minimal overhead with SQLite’s reliability.

## Installation
```sh
pip install git+https://github.com/jnsougata/driz.git
```

## Example Usage
```python
import driz

db = driz.DB("example.db")
users = db.collection(
    "users", 
    schema=driz.Schema(
    driz.Column("id", int, "PRIMARY KEY"),
    driz.Column("name", str, "NOT NULL"),
    driz.Column("age", int, "NOT NULL"),
    driz.Column("email", str, "UNIQUE"),
    driz.Column("is_active", bool, "DEFAULT 1"),
))
users.insert(
    id=1,
    name="John Doe",
    age=30,
    email="doe@example.com",
    is_active=True,
)
for user in users.all():
    print(user)
users.delete(1)
```

## Documentation
Coming soon! For now, refer to the code comments and examples or source dive.

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
