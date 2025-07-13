from flask import Flask, request, Response
from prometheus_client import Counter, Sumary ,generate_lastest, CONTENT_TYPE_LASTET

app = Flask(__name__)

REQUEST_COUNT = Counter('app_request_total','total number of requests',['method','endpoint'])
EXCEPTION = Counter('app_exception_total','total number of unhandled exceptions',['endpoint','exception_typer'])
PRINT_NUMBER = Sumary('app_print_number_summary','Sumarização das informações sobre os números que foram passados')

@app.errohandler(Exception)
def catch_all(e):
    EXCEPTION.labels(endpoint=request.path,exception_type=type(e).__name__).inc()

@app.before_request
def count_resquests():
    REQUEST_COUNT.labels(method=request.method,endpoint = request.path).inc()

@app.route('/hello')
def hello():
    return 'Hello Word!'

@app.route('/print_number')
def print_number():
    num_str = request.args.get('number',None)

    if num_str is None:
        return 'Numero que precisa',400
    num =float(num_str)

    PRINT_NUMBER.observe(num)
    return f"Numero: {num}"

@app.route('/crash')
def crash():
    raise KeyError

@app.route('/metrics')
def metrics():
    return Response(generate_lastest(),mimetype=CONTENT_TYPE_LASTET)

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5000)
