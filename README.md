# Proxy - Proxy server!
This is a Proxy Server, makes bearer authentication to nothing by securely hiding your API key!

# How to use?
Click use this template above or `git clone https://github.com/Ericwasepic127/proxy.git`

Then, edit env.example file, rename to .env and follow instructions (like set API_KEY)

After that, do
```shell
pip install -r requirements.txt
gunicorn app:app
```
**OR**

Host on platform like [Render](https://render.com/)

and get your URL so
