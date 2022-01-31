# Eazy Invoice

### Minimal Web Application for Creating Invoices

![](https://media.giphy.com/media/UDVTRm69LC3sc/giphy.gif)

<hr>

### Screenshots

Generated Invoice

![Screenshot_20220130_202621](https://user-images.githubusercontent.com/20848221/151727250-3a9bf0c4-2854-4793-933f-2df7cda00100.png)


Org Interface

![Screenshot_20220130_202356](https://user-images.githubusercontent.com/20848221/151727299-630b522a-ae09-4293-a734-0fee08d9cb7e.png)

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
