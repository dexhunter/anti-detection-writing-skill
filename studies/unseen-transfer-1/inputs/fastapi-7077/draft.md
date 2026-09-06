Set the cookie on the `RedirectResponse` that the endpoint returns. The injected `Response` is a different object. FastAPI copies its headers when constructing a response from ordinary returned data, but returning a response instance bypasses that construction.

```python
@app.get("/cookiefail")
def cookie_fail():
    response = RedirectResponse("/")
    response.set_cookie(key="works", value="here is your data")
    return response
```

The [documented direct-response approach](https://fastapi.tiangolo.com/advanced/response-cookies/#return-a-response-directly) does not require `response_class=RedirectResponse` or a hard-coded cookie domain. Omitting the domain avoids tying the example to `127.0.0.1`; normal cookie matching rules still apply. Cookies are separate from localStorage.

The newer `/authorize` example already sets the cookie on the returned redirect, so this fix does not explain that failure. Check the redirect's `Set-Cookie` header, the next request's `Cookie` header, and the actual hosts and test client's cookie handling before assigning a cause. The browser behavior has not been reproduced here.
