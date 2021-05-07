Error codes the API returns:
- 400 : bad request
- 404 : resource not found
- 422 : unprocessable
- 405 : method not allowed
- 500 : internal server error

## Testing
To run the tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```