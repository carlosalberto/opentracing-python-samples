import concurrent.futures
import time

import opentracing


def create_tracer():
    '''
    Returns a new Tracer object. For cleaness purposes,
    a new one should be created for each process.
    '''

    # Replace with an Opentracing compatible tracer.
    return opentracing.tracer


def task_func(name, wait_time, return_value, carrier):
    '''
    Simulate a task that takes `wait_time` and returns `return_value`
    with the given context contained in the carrier using the TEXT_MAP
    format.
    '''

    tracer = create_tracer()
    ctx = tracer.extract(opentracing.Format.TEXT_MAP, carrier)

    with tracer.start_span('task-%s' % name, child_of=ctx) as span:
        time.sleep(wait_time)

    tracer.flush()
    return return_value


if __name__ == '__main__':
    tracer = create_tracer()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        with tracer.start_span('main') as span:
            carrier = {}
            tracer.inject(span.context, opentracing.Format.TEXT_MAP, carrier)

            f1 = executor.submit(task_func, 'A', .3, 7, carrier)
            f2 = executor.submit(task_func, 'B', .2, 8, carrier)
            f3 = executor.submit(task_func, 'C', .7, 1, carrier)
            f4 = executor.submit(task_func, 'D', .4, 5, carrier)

            for f in concurrent.futures.as_completed([f1, f2, f3, f4]):
                print(f.result())
