import concurrent.futures
import time

import opentracing


# Replace with an Opentracing compatible tracer.
tracer = opentracing.tracer

def task_func(name, wait_time, return_value, parent_span):
    '''
    Simulate a task that takes `wait_time` and returns `return_value`
    and `parent_span` as a reference when creating ours. As long
    as the Tracer/Span uses `basictracer` as its base package/implementation,
    such Span object will be thread-safe.
    '''

    with tracer.start_span('task-%s' % name, child_of=parent_span) as span:
        time.sleep(wait_time)
    
    return return_value


if __name__ == '__main__':

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        with tracer.start_span('main') as span:
            f1 = executor.submit(task_func, 'A', .3, 7, span)
            f2 = executor.submit(task_func, 'B', .2, 8, span)
            f3 = executor.submit(task_func, 'C', .7, 1, span)
            f4 = executor.submit(task_func, 'D', .4, 5, span)

            for f in concurrent.futures.as_completed([f1, f2, f3, f4]):
                print(f.result())
