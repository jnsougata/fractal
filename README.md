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
    posts = db.collection(
        "posts",
        schema=driz.Schema(
            driz.Field("user_id", str, ref_collection="users", ref_field="key"),
            driz.Field("content", str, nullable=False))
    )
    user_id = users.insert(
        name="Sougata Jana",
        age=25,
        email="abc@xyz.com",
        active=True,
    )
    print(f"Inserted user with ID: {user_id}")
    posts.insert(
        user_id=user_id,
        content="This is a test post.",
    )


if __name__ == "__main__":
    main()
```

## Documentation
Coming soon! For now, refer to the code comments and examples or source dive.
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
