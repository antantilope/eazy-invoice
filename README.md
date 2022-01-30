# Eazy Invoice

### Minimal Web Application for Creating Invoices

![](https://media.giphy.com/media/UDVTRm69LC3sc/giphy.gif)

<hr>

### Installation

```bash
# create locals file
$ touch eazyinvoice/eazyinvoice/secrets.py
```

```python
# Example secrets.py (don't commit this file)
SECRET_KEY = "SECRET"
IS_PROD = False
ALLOWED_HOSTS = ["*"]

def get_auth_code():
    return 42
```

```bash
$ pip install -r requirements.txt
$ cd eazyinvoice
$ ./manage.py migrate

# install wkhtmltopdf
# Debian
$ sudo apt install wkhtmltopdf
```

```bash
# Start development server
$ ./manage.py runserver
```

### Run Tests
```bash
$ ./test
```
