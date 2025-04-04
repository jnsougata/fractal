![driz](https://github.com/user-attachments/assets/75f99420-b480-4199-987d-8542e6236507)
# Driz - KV Store
A fast, lightweight key-value store designed for hobbyists, combining the simplicity of NoSQL with SQLite3's robust filtering and sorting capabilities.
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


def main():
    db = driz.DB("example.db")
    users = db.collection(
        "users",
        schema=driz.Schema(
                driz.Field("name", str, nullable=False),
                driz.Field("age", int, nullable=False),
                driz.Field("email", str),
                driz.Field("active", bool, default=True),
        )
    )
    success = users.insert(
        {
            "name": "Sougata Jana",
            "age": 25,
            "email": "abc@xyz.com",
            "active": True,
        },
        {
            "name": "Rajibul Molla",
            "age": 22,
            "email": "abc@xyz.com",
            "active": True,
        }
        
    )
    print(success)
    
    query = users.query("active").startswith("name", "R").lt("age", 30)
    print(query.exec())

if __name__ == "__main__":
    main()
```

## Documentation
Half-baked docs [here.](https://driz.readthedocs.io/en/latest/)

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
